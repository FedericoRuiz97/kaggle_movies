
# Liberías para el tratamiento de los datos
import feature_engine
from feature_engine.imputation import AddMissingIndicator, CategoricalImputer, MeanMedianImputer, ArbitraryNumberImputer
from feature_engine.encoding import RareLabelEncoder
from feature_engine.outliers import Winsorizer
from feature_engine.selection import DropConstantFeatures, DropCorrelatedFeatures, SmartCorrelatedSelection
import category_encoders as ce
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.utils.validation import check_is_fitted

# Librerías para modelado
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from imblearn.pipeline import Pipeline
from copy import deepcopy
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import roc_auc_score, mean_squared_error, mean_absolute_error
from math import sqrt
import skopt
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize, forest_minimize, dump



def find_numerical_vars(X, variables=None):
    """
    Función que devolverá las variables numéricas si no se ingresaron variables. 
    Tira error si no hay variables numéricas, o si las que se ingresaron no lo son realmente.
    """
    if not variables:
        # si no se ingresaron variables, entonces selecciona los tipos de datos numéricos
        variables = list(X.select_dtypes(include='number').columns)
        if len(variables)==0:
            # si haciéndolo no queda ninguna, es porque no hay variables numéricas
            raise ValueError("No numerical variables in this dataframe. Please check variable format with dtypes")
    else:
        # en caso de haber ingresado variables, se verifica que sean numpericas
        if len(X[variables].select_dtypes(exclude='number').columns)!=0:
            # si alguna no lo es, se eleva un error
            raise TypeError("Some of the variables are not numerical. Please cast them as numerical")
    # se devuelven las variables
    return variables

class BaseImputer(BaseEstimator, TransformerMixin):
    """Procedimiento de transfformación común a la mayoría de imputers"""
    def transform(self, X):
        """
        Reemplaza missings con los parametros aprendidos
        Parámetros
        ----------
        X: pandas dataframe de dimensiones = [n_samples, n_features]
           Muestras de input
        
        Returns
        ----------
        X_transformed: pandas dataframe de dimensiones = [n_samples, n_features]
                       Dataframe sin missing values en las variables seleccionadas   
        
        """
        # Chequea si el método ya fue fitteado
        check_is_fitted(self)
        
        # Chequea que el input sea un dataframe
        if not isinstance(X, pd.DataFrame):
            raise TypeError("The data set should be a pandas dataframe")
        
        # Reemplaza los missings con los parametros aprendidos
        for variable in self.imputer_dict_:
            X[variable].fillna(self.imputer_dict_[variable], inplace=True)
        
        return X
        


class LinearModelImputer(BaseImputer):
    """ 
    Reemplaza missings en variables numéricas utilizando una regresión lineal simple (variable vs target)
    """
    def __init__(self, variables=None):
        """run = False to passthrough"""
        if not variables or isinstance(variables,list):
            self._variables = variables
        else:
            self._variables = [variables]
    def fit(self, X, y):
        # Verificamos que el X ingresado sea dataframe
        if not isinstance(X, pd.DataFrame):
            raise TypeError("The data set should be a pandas dataframe")
        
        # Buscamos las variables numéricas
        self._variables = find_numerical_vars(X, self._variables)
        
        # Verificamos que se haya ingresado un "y"
        if y is None:
            raise ValueError("Please provide a target y for thins encoding method")
            
        # Con todo listo, se procede a calcular el valor de imputación 
        self.imputer_dict_ = {}
        
        # Recorremos cada variable entre las ingresadas (o todas las numéricas halladas)
        for var in self._variables:
            # Creamos, ajustamos, y utilizamos para predecir un modelo lineal simple (variable "i" vs target), obviamente donde X no sea nulo
            model = linear_model.LinearRegression()
            model.fit(X = pd.DataFrame(X[~X[var].isnull()])[var].values.reshape(-1,1), y = pd.DataFrame(y[~X[var].isnull()]))
            model.score(X = pd.DataFrame(X[~X[var].isnull()])[var].values.reshape(-1,1), y = pd.DataFrame(y[~X[var].isnull()]))
            # Obtenemos el coeficiente de la variable 
            coef = float(model.coef_)
            # Obtenemos el intercepto del modelo
            intercept = float(model.intercept_)
            # Vemos cual es el target promedio para los missings
            y_missings = pd.DataFrame(y[X[var].isnull()]).mean()
            # Vemos el valor de "X" que correspondería a ese target promedio ("y")
            value_for_missings = float((y_missings - intercept)/ coef)
            # Guardamos ese valor como nuestra imputación
            self.imputer_dict_[var] = value_for_missings
            
        self.input_shape_ = X.shape
        return self
    def transform(self, X):
        """
        Escribir definiciones de nuevas variables
        Dropear variables que no se van a usar más
        """
        X = super().transform(X)
        return X
    
class FeatureSelector(BaseEstimator, TransformerMixin):
    """
    Selecciona features por su nombre. Servirá para aplicar pipelines a distintos datasets
    """
    def __init__(self, columns):
        """columns = lista de column names"""
        self.columns = columns
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return X[self.columns]