Feature Engineering :
Feature engineering is the process of turning raw data into useful features that help improve the performance of machine learning models
Steps :
1.Feature Creation - Generate new features
2.Transformation
    a. Normalization and Scaling - Adjust the range of features for consistency.
    b. Encoding - Converts categorical data to numerical form i.e one-hot encoding.
    c. Mathematical transformations
3.Extraction 
    a. Dimensionality reduction - Techniques like PCA reduce features
    b. Aggregation & Combination - Summing or averaging features to simplify the model.
4.Feature Selection
    a. Filter - Based on statistical measures like correlation
    b. Wrapper - Select based on model performance
5.Scaling 
   Scaling ensures that all features contribute equally to the model
  a. Min-Max Scaling - Rescales values to a fixed range like 0 to 1.
  b. Standard Scaling -  Normalizes to have a mean of 0 and variance of 1.

Common Techniques :
1. OHE - One-Hot Encoding converts categorical variables into binary indicators
2. Binning - Binning transforms continuous variables into discrete bins
3. Text Data Preprocessing -  vectorizing

Supervised Learning
--------------------
1. Linear Regression - works on continuous 
2. Logestic Regression
3. Decision Tree

Unsupervised Learning
---------------------
1. PCA



PCA
====
PCA (Principal Component Analysis) is a dimensionality reduction technique used in data analysis and machine learning. It helps you to reduce the number of features in a dataset while keeping the most important information. It changes your original features into new features these new features don’t overlap with each other and the first few keep most o

Model Evaluation and Tuning
---------------------------
1. Regularization  -
Regularization is a technique used in machine learning to prevent overfitting and performs poorly on unseen data. By adding a penalty for complexity, regularization encourages simpler, more generalizable models.
2. Cross-validation is a technique used to check how well a machine learning model performs on unseen data while preventing overfitting. It works by:
    Splitting the dataset into several parts.
    Training the model on some parts and testing it on the remaining part.
    Repeating this resampling process multiple times by choosing different parts of the dataset.
    Averaging the results from each validation step to get the final performance.
3. Hyperparameter Tuning
    A high learning rate can cause the model to converge too quickly possibly skipping over the optimal solution.
    A low learning rate might lead to slower convergence and require more time and computational resources.
    Bayesian optimization - 
    Build a probabilistic model (surrogate function) that predicts performance based on hyperparameters.
    Update this model after each evaluation.
    Use the model to choose the next best set to try.
    Repeat until the optimal combination is found. The surrogate function models:
4. OverFitting
   a. OverFitting - Overfitting happens when a model learns too much from the training data, including details that don’t matter (like noise or outliers).
   b. High variance and low bias, model too complex
   c. To remove overfitting - improve quality of training data, reduce model complexity, regularization, increase training data
5. UnderFitting -  It happens when a model is too simple to capture what’s going on in the data.
   a. High bias and low variance
   b. Model is too simple, size of training data is low
   c. To fix underfitting : increase model complexity, increase features, remove noise, increase epochs
6. Bias Variance tradeoff
   a. 

7. Loss functions - They provide a measure of how well the model's predictions align with the actual data
   Refer : https://builtin.com/machine-learning/common-loss-functions
   a. Regression Models 
       i.  Mean Squared Error - average of squared differences between the actual value (Y) and the predicted value (Ŷ). 
       ii. Mean Absolute Error - calculates the mean of the absolute values of the residuals for all datapoints in the dataset
       iii. Mean Bias Error - it can help in determining whether the model has a positive bias or negative bias
       iv. Huber Loss - The Huber loss function uses a quadratic penalty (like MSE) for errors smaller than δ (delta), and a linear penalty (like MAE) for errors larger than δ.
  b. Classification 
       i. Cross-Entropy Loss - This loss function measures how well the predicted probabilities match the actual labels.
       ii. Kullback-Leibler Divergence - a widely used loss function in machine learning(NN) that measures how one probability distribution differs from a reference probability distribution.
       iii. Hinge Loss - Used in SVM - Hinge loss penalizes the wrong predictions and the right predictions that are not confident.

Gradient Boosting
----------------
1. Gradient boosting works by building simpler (weak) prediction models sequentially where each model tries to predict the error left over by the previous model. 
