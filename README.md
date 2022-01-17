# Challenge Kaggle Movies
This challenge was developed for Kueski, focusing on feature engineering rather than modeling.

Files structure:
* raw_data: folder with kaggle movies data 
* model_input: folder with data input for model, it is the output of etl.ipynb
* model: model files that include the LightGBM trained classificator, and the pipeline. Also an excel with records of the hyperparameters optimization
* outputs: csv file with the required structure (userId, movieId, features, target, and binary predictions)
* etl.ipynb: ETL process to build features
* utils.py: useful functions to be used in modeling.ipynb
* modeling.ipynb: Feature Engineering + modeling 

# My work: 
- I have built an ETL process to create basic features
- Performed feature-engineering to help the model to do better predictions
- Split the data so the model can be tested in terms of both generalization and temporal stability
- Designed the preprocessing pipeline (without testing alternatives on it's configuration)
- Optimized hyper-parameters
- Tested performance on different samples
- Understood feature importances and value impacts on the output
- Calibrated the predictor to optimize F1 score 
- Predicted the target for each user-movie 
- Export predictions, model, pipeline, and useful files

# Features design
WIP
