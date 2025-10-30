1. Classification -

    a. Logistic regression eg : customer churn prediction

        Pros :
        Simple
        Good for smaller datasets
        Logistic regression is lightning-fast
        Cons :
        Have to do lot of upfront work
        Scale numerical features
        Encode categorical one
        logistic regression can only handle linear relationships
        Use only L1 and L2 regularization
        clear, interpretable coefficients.
        
        b. Gradient Boosting (XG Boost)
        Pros :
        can pick non linear relationships
        Supports lambda and alpha, giving you more control.
        Can handle missing values
        Cons:
        Computation cost is high
        Low interpretability
    
    
    b. Losses
      Cross Entrophy Loss
      Normalized Cross Entrophy loss
      


2. Regression -

  a. Linear Regression eg : Goal: Predict house prices based on features like size, bedrooms, and location.
  b. Decision tree
  c. NN
  d. KNN

3. Deep Learning (Continual learning)
   a. CNN for  Image Classification eg : ResNet
   b. RNN  (EG: LSTM) predicting stock prices based on historical data.  they remember previous inputs for better predictions. 
   c. Transformers such as BERT, T5 for chatbots etc
   d. FNN - The simplest type, where data flows straight through from input to output. Ideal for general-purpose predictions.

  Classification :  Cross Entrophy
  Activation : Binary :  Relu Multi-label/multi-class : 
  Regression : 
   Loss : MSE, MAE
   hidden layerActivation : Relu 
  output layer activation : logistic, sigmoid (for multi-class)
        

4. Recommendation Systems
Product recommendations (e-commerce), movie recommendations, content suggestions.
Algorithms: Collaborative Filtering, Content-Based Filtering, Matrix Factorization.

5. Ranking Systems
    i. LR 
           Point wise ranking
           Pair wise ranking
           List wise ranking
6. Unsupervised
   a. Clustering K-means, ANN
   b. Dimensionality reduction by PCA

7. Semi Supervised
 Random forest classifier
 Re-inforcment learning

8. Prediction alg eg - stock price prediction
1. Linear regression
2. 