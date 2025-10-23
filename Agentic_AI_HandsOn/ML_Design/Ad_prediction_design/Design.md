Step 1 : Problem Formulation
    Clarifying questions :
    a. primary objective
    b. what type of ads are we predicting clicks for
    c. what type of user interaction data can we able to access
    d. are there any user segments or context we consider
    e. do we need continual training
    
    Use case and Business goal:
    use case: predict which ads a user is likely to click on when presented with multiple ad options.
    business obj: maximize ad revenue delivering relevant ads
    
    requirements:
    a. Real-time prediction capabilities to serve ads dynamically.
    b. scalability to handle large number of ad impressions
    c. continual learning
    d. integration with ad serving platforms and sources
    
    constraints:
    a. Privacy and compliance with data protection regulations.
    b. data regulation
    c. limited user attention
    
    datasources and availability:
    a. user interaction logs, ad content data, user profiles, contextual info
    b. historical click impressions
    c. labeled data for supervised learning
    
    assumptions:
    a. Users' click behavior is influenced by factors that can be learned from historical data.
    b. Ad content and relevance play a significant role in click predictions.
    c. The click behavior can be modeled as a classification problem.
    
    ML formulation : Ad click prediction is a ranking problem

STEP 2 : METRICS
---------------
    Offline metrics : CE (Cross Entropy as binary classification) - how far  models loss is from actual
    NCE (Normalized over baseline)  -     NCE - It divides the standard cross-entropy loss by an average log loss that would be achieved if the model predicted a baseline click-through rate (CTR) for all impressions.
    Online Metrics :
    CTR
    Conversion rate
    Revenue lift
    Hide rate

STEP 3 : ARCHITECTURAL COMPONENTS
---------------------------------
    a. Can use point wise learning rank (LTR)
    b. ML models such as gradient boosting, NN, logistic regression, decision trees can be used for prediction

STEP 4 : Data collection and Preparation
----------------------------------------
    Data Sources
    Users,
    Ads,
    User-ad interaction
    ML Data types
    Labelling

STEP 5 : Feature Engineering
----------------------------------------
    a. Feature Selection
    Ads:
        IDs
        categories
        Image/videos
        No of impressions / clicks (ad, adv, campaign)
    User:
        ID, username
        Demographics (Age, gender, location)
        Context (device, time of day, etc)
        Interaction history (e.g. user ad click rate, total clicks, etc)
    User-Ad interaction:
        IDs(user, Ad), interaction type, time, location, dwell time
     
    b. Feature preparation:
    Sparse Features :
     IDs: embedding layer (each ID type its own embedding layer)
    Dense features:
    Engagement feats: No of clicks, impressions, etc
    use directly
    Image/video :
    Use SIMCLR to embed video to feature vector
    Texttual dataa:
    normalize, tokenize and encode

STEP 6 : Model development

Model Selection : LR
Feature crossing + LR
feature crossing: combine 2/more features into new feats (e.g. sum, product)
pros: capture nonlin interactions b/w feats
cons: manual process, and domain knowledge needed

GBDT + LR:
pros: interpretable
cons: inefficient for continual training, can't train embedding layers

NN:  two tower network (user tower, ad tower)
Cons for ads prediction:
sparsity of features, huge number of them
hard to capture pairwise interactions (large no of them)

Deep and cross network :
finds feature interactions automatically
two parallel networks: deep network (learns complex features) and cross network (learns interactions)
two types: stacked, and parallel

Factorization Machine:
embedding based model, improves LR by automatically learning feature interactions (by learning embeddings for features)
w0 + \sum (w_i.x_i) + \sum\sum <v_i, v_j> x_i.x_j
cons: can't learn higher order interactions from features unlike NN

Deep factorization machine (DFM) :
combines a NN (for complex features) and a FM (for pairwise interactions)

start with LR to form a baseline, then experiment with DCN & DeepFM



STEP 7 : Prediction Service
    Data Prep Pipeline:
        a. static features (e.g. ad img, category) -> batch feature compute (daily, weekly) -> feature store
        b. dynamic features: # of ad impressions, clicks.
    Prediction Pipeline:
        2 stage:
        candidate generation:
        use ad targeting criteria by advertiser (age, gender, location, etc)
    ranking :
        features -> model -> click prob. -> sort
        re-ranking: business logic (e.g. diversity)
    Continual learning pipeline:
        fine tune on new data, eval, and deploy if improves metrics
STEP 8 : Online testing and deployment
A/B Testing
Deployment and release

STEP 9 : Scaling and monit
Scaling (SW and ML systems)
Monitoring
Updates



        


