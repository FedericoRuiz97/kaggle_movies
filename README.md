# Challenge Kaggle Movies
This challenge was developed for Kueski, focusing on feature engineering. More details on feature designing at the end of this file!

## Comments on the result:
The challenge was completed, although: the model performance is just ok (wouldn't say nice), and in the feature engineering part there is still plenty work to be done. 
I've made a decent MVP and I'll explain here not only what was done, but also what could be done to improve the model. 
Specially in the features that could have been generated.

## Files structure:
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
I've organized the design in 3 different feature families: Movie features, user features, and environment features.
## 1) Movie features: 
### This are general descriptions of the movie. These are low-complexity features because there is no temporality issues involved, and the information consists only on the movie itself. Here is the list of features with the hypothesis I had to explain behaviour.
- Movie year (extracted from the title): Useful for years (or decades) with great movies. Also useful to build other features
- Flag for each genre: Some genres consistently have bad rates (e.g.: horror movies are usually bad)
- Tag relevance information:
1. Top 5 tags of the movie (string): Useful tags were relevant (e.g.: oscar(best supporting actor) , surprise ending, etc)
2. Relevance of the top 5 most relevant tags of all movies (doesnt qualify as data leakage): Some tags are consistently relevant, such as "great ending" which suggest a big impact on the rating 
3. Relevance of the top 5 most discriminant tags of all movies: If the tag has very different relevances, it should mean it is important to describe a movie ("tense" is not a tag for every movie). Not so promising for predictions, but insightful for movie description. 
- IMDB average ratings (External): If IMDB applied a high rate to the movie, most users should do so (even if they dislike the movie, they might be biased)
- IMDB votes quantity: Gives a sense of how many people saw the movie (and how reliable is the average rating)
- Movie recency: years between the movie creation and the rating. I think people watch old movies only if these have nice references (useful for other features like "avg. recency of movies watched for each user)
- Hour of the rating (WIP): Judges are more strict before lunch and dinner. This indicates that the hour of the rating may be relevant to predict it. This feauture probably won't explain a lot by itself, but it captures information that no one else can (it shouldn't be correlated with other features)
- Time from the last high (WIP): If a movie just blown the user's mind an she rated it as high, maybe for the next movie she will have a higher standard or comparison and will be more strict.

## 2) User features:
### These features can be tricky due to the temporality issues. We should not use data behaviour that occurred after each rating (this would lead to DATA LEAKAGE). 
- Average rate of the user (past 20 movies) --> In my experience the strongest predictor ALWAYS is the history of the target. In this case we see the "long term" (20 movies)
- Average rate of the user (past 5 movies) --> We'll also see the short term (sometimes is nice to make this difference)
- Trend of rating (past_20 vs past_5) --> The user may be choosing better the movies, or following some special trend, and that is what I try to capture with this feature. 
- Amount of movies rated by the user: Experience can tell a lot about how judgy you may be.
- Rate of highs --> This is another perspective on the target history (maybe even more accurate because it's calculated in the same binary way)
- Amount of highs --> This gives a dimention of how reliable is the former feature
- Years from the first rated movie --> It's another perspective for the experience that the user has. Tries to capture something about her age.

# Features yet to build:
## 3) Environment features:
### These features can be even trickier. The idea is to get features from the rest of the users before each rating. This information would help when we have only a small amount of data for each user, and therefore is not entirely reliable. We can calculate a weighted mean between the user feature and the environment feature, based on the amount of data we have. This features would be:
- The same list of "2) User features" but for the environment, and adding the amount of data in each case.

