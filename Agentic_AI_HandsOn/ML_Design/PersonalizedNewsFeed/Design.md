Problem :
show feed (recent posts and activities from other users) on a social network platform

1. Clarifying questions
    a. What is the primary business objective of the system
    b. Do we show only posts or also activities from other users
    c. What types of engagement are available?
    d. Do we display ads as well
    e. What types of data do the posts include?
    f. Are there specific user segments or contexts we should consider
    g. What type of user-ad interaction data do we have access to can we use it for training our models
    h. Do we need continual training?
    g. How fast the system needs to be?
    
    Business goal :
    a. use case: show friends most engaging (and unseen) posts and activities on a social network platform app (personalized to user)
    b. business objective: Maximize user engagement (as a set of interactions)
    
    Requirements;
    Latency: 200 msec of newsfeed refreshed results after user opens/refreshes the app
    Scalability: 5 B total users, 2 B DAU, refresh app twice
    Constraints:
    Privacy and compliance with data protection regulations.
    Data: Sources and Availability:
    Data sources include user interaction logs, ad content data, user profiles, and contextual information.
    Historical click and impression data for model training and evaluation.
    
    ML Formulation:
    Objective:
    maximize number of explicit, implicit, or both type of reactions (weighted)
    implicit: more data, explicit: stronger signal, but less data -> weighted score of different interactions: share > comment > like > click etc
    I/O: I: user_id, O: ranked list of unseen posts sorted by engagement score (wighted sum)
    Category: Ranking problem: can be solved as pointwise LTR with multi/label (multi-task) classification

2. Metrics :
    a. Offline :
        ROC AUC (trade-off b/w TPR and FPR)
    b. Online :
        CTR,
        Reactions rate (like rate, comment rate, etc)
        Time spent
        User satisfaction (survey)

3. Architectural Components
    i. We can use point-wise learning to rank (LTR) formulation
     The pointwise ranking is finding the ranking function that returns each document’s relevance given a query.
    Created 1:1 mapping between query and document pair sample 1 : d1,q1; label :1 sample 2 : d2,q1; label :1 sample 3 : d3,q1; label :1 sample 4 : d4,q2; label :1 sample 5: d5,q2; label :1 sample 6: d6,q2; label :1
    Drawbacks with point wise ranking :
    a. Each instance is treated as an isolated point.
    b. Explicit pointwise labels are required to create the training dataset.

   ii. Pair wise ranking :
   a. Use pairs for ranking for example :
      Example : d1,d2, and d3 are relevant to q1 then all below are relevant
     sample 1: q1, (d1,d2) sample 2: q1, (d1,d3) sample 3: q1, (d2,d3)
     Unlike point wise, pair wise considers ranking position
     Drawbacks:
     training can be very costly when the dataset contains large document and query pairs.
    iii. List wise ranking
    the list of ranked documents is taken into account, along with their relevance labels.
   
   Classification:
   N independent classifiers (expensive to maintain)
   Use multi-task classifier :
   learn multi tasks simultaneously
   single shared layers (learns similarities between tasks) -> transformed features
   task specific layers: classification heads
   pros: single model, shared layers prevent redundancy, train data for each task can be used for others as well (limited data)

    

4. Data Collection and Preparation
      Data Sources :
        Users
        Posts
        User Post interaction
        User-User

5. Feature Engineering
    a. Feature selection
    Posts:
    Text
    Image/videos
    No of reactions (likes, shares, replies, etc)
    Age
    Hashtags
    User:
    ID, username
    Demographics (Age, gender, location)
    Context (device, time of day, etc)
    Interaction history (e.g. user click rate, total clicks, likes, et )
    User-Post interaction:
    IDs(user, Ad), interaction type, time, location
    User-user(post author) affinities
    connection type
    reaction history (No liked/commented/etc posts from author)

    b. Feature Preparation 
     Text : use BERT here (posts are in phrases usually, context aware helps)
     Image/Video :
     PreProcess and use SimCLR / CLIP to convert -> feature vector
     Dense numerical features:
     Engagement feats (No of clicks, etc)
     use directly + scale the range
     Discrete numerical:
     Age: bucketize into categorical then one hot
     Hashtags:
     tokenize, simple vectorization (TF-IDF or word2vec)
6. Model Development/Evaluation
   Model Selection -
   Use NN. Unstructured data
   Multi-labels : click, share, like
   Multi-task NN :
   a. Shared Layers
   b. Classification heads
   
   Model Training -
   Loss function for binary classification : Cross Entrophy
   Regression : Mean Squared Error, 

7. Prediction
   a. Data Prep Pipeline -
   static features -> batch feature compute (daily, weekly) -> feature store
   dynamic features: # of post clicks, etc _> streaming
   b. Prediction pipeline
    two stage (funnel) architecture
    candidate generation / retrieval service
    rule based
    filter and fetch unseen posts by users under certain criteria
    Ranking
    features -> model -> engagement prob. -> sort
    re-ranking: business logic, additional logic and filters (e.g. user interest category)
  c. Continual learning pipeline
      fine tune on new data, eval, and deploy if improves metrics

8.  Online Testing and Deployment
   a. A/B Test, 

   
 