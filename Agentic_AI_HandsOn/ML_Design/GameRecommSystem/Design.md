STEP 1 - Problem formulation
    Some existing data examples:
    
    Games data
    
    app_id, title, date_release, win, mac, linux, rating, positive_ratio, user_reviews, price_final, price_original, discount, steam_deck,
    User historic data
    
    user_id, products, reviews,
    Recommendations data
    
    app_id, helpful, funny, date, is_recommended, hours, user_id, review_id,
    Reviews
    
    Example Open Source Data: Steam games complete dataset (CF and content based github)
    
    Game features include:
    Url, types name, desc_snippet, recent_reviews, all_reviews, release_date, developer, publisher, popular_tag,


STEP 2 - Clarifying questions
    Clarifying questions
    Use case? Homepage?
    Does user sends a text query as well?
    Business objective?
    Increase user engagement (play, like, click, share), purchase?, create a better ultimate gaming experience
    Similar to previously played, or personalized for the user? Personalized for the user
    User locations? Worldwide (multiple languages)
    User’s age group:
    Do users have any favorite lists, play later, etc?
    How many games? 100 million
    How many users? 100 million DAU
    Latency requirements - 200msec?
    Data access
    Do we log and have access to any data? Can we build a dataset using user interactions ?
    Do we have textual description of items?
    can users become friends on the platform and do we wanna take that into account?
    Free or Paid?

STEP 3 - ML Objective
    Recommend most engaging (define) games
    Max. No. of clicks (clickbait)
    Max. No. completed games/sessions/levels (bias to shorter)
    Max. total hours played ()
    Max. No. of relevant items (proxy by user implicit/explicit reactions) -> more control over signals, not the above shortcomings
    Define relevance: e.g. like is relevant, or playing half of it is, …
    ML Objective: build dataset and model to predict the relevance score b/w user and a game
    I/O: I: user_id, O: ranked list of games + relevance score
    ML category: Recommendation System

STEP 4  - Metrics
    Offline:
    precision @k, mAP, and diversity
    Online:
    CTR, # of completed, # of purchased, total play time, total purchase, user feedback

STEP 5 - ARCH COMPONENTS
    Candidate generation -
    Candidate generation 1 (Relevance based)
    Candidate generation 2 (Popularity)
    Candidate generation 3 (Trending)
    a. Content based filters
    No need for interaction data, recommends new items to users (no item cold start)
    Capture unique interests of users
    New user cold start
    Needs domain knowledge
    b. User or Item based CF. Using user-user (user based CF) or item-item similarities (item based CF)
    c. hybrid : Parallel hybrid: combine(CF results, content based) Sequential: [CF based] -> Content based

STEP 5 - Data Prep
    Data Sources:
    Users (user profile, historical interactions):
    
    User profile:
    User_id, username, age, gender, location (city, country), lang, timezone
    Games (structures, metadata, game content - what is it?)
    Game_id, title, date, rating, expected_length?, #reviews, language, tags, description, price, developer, publisher, level, #levels
    User-Game interactions:
    Historical interactions: Play, purchase, like, and search history, etc
    
    User_id, game_id, timestamp, interaction_type(purchase, play, like, impression, search), interaction_val, location
    Context: time of the day, day of the week, device, OS
    
    Preprocessing Type :
    Removing duplicates
    filling missing values
    normalizing data.
    Labeling:
    For features in the form of <user, video> pairs -> labeling strategy based on explicit or implicit feedback e.g. "positive" if user liked the item explicitly or interacted (e.g. watched/played) at least for X (e.g. half of it).
    negative samples: sample from background distribution -> correct via importance smapling

STEP 6 - Feature engineering
    A. Selected features :
    Game metadata features:
    Game ID, Duration, Language, Title, Description, Genre/Category, Tags,
    Publisher(popularity, reviews), Release date, Ratings, Reviews, (Game content ?) game titles, genres, platforms, release dates, user ratings, and user reviews.
    
    User profile:
    User ID, Age, Gender, Language, City, Country
    
    User-item historical features:
    User-item interactions
    Played, liked, impressions
    purchase history (avg. price)
    User search history
    Context
    B. Feature representation :
    a. Categorical data (game_id, user_id, language, city): Use embedding layers, learned during training
    b. Categorical_data(gender, age): one_hot
    c. Continuous variables: normalize, or bucketize and one-hot (e.g. price)
    d. Text:(title, desc, tags): title/description use embeddings, pre-trained BERT, fine tune on game language?, tags: CBOW
    Game content embeddings?

STEP 7 : Model development and Evaluation
    A. Candidate generation
    Options :
    Matrix Factorization
    Pros: Training speed (only two matrices to learn), Serving speed (static learned embeddings)
    Cons: only relies on user-item interactions (No user profile info e.g. language is used); new-user cold start problem
    Two tower neural network:
    Pros: Accepts user features (user profile + user search history) -> better quality recommendation; handles new users
    Cons: Expensive training, serving speed
    Two-tower network
    two encoder towers (user tower + encoder tower)
    user tower encodes user features into user embeddings
    item tower encodes item features into item embeddings 
    similarity ui * vi is considered as a relevance score (ranking as classification problem)
    
    B. RANKING
    For Ranking stage, we prioritize precision over efficiency. We choose content based filtering. Choose a model that relies in item features.
    ML Obj options:
    
    max P(watch| U, C)
    max expected total watch time
    multi-objective (multi-task learning: add corresponding losses)
    Model Options:
    
    FF NN (e.g. similar tower network to a tower network) + logistic regression
    Deep Cross Network (DCN)
    Features
    
    Video ID embeddings (watched video embedding avg, impression video embedding),
    Video historic
    No. of previous impressions, reviews, likes, etc
    Time features (e.g. time since last play),
    Language embedding (user, item),
    User profile
    User Historic (e.g. search history)

C. Re-Ranking
    Re-ranks items by additional business criteria (filter, promote)
    We can use ML models for clickbait, harmful content, etc or use heuristics
    Examples:
    
    Age restriction filter
    Region restriction filter
    Video freshness (promote fresh content)
    Deduplication
    Fairness, bias, etc

STEP 8 - Prediction Service
   two-tower network inference: find the k-top most relevant items given a user ->
   It's a classic nearest neighbor problem -> use approximate nearest neighbor (ANN) algorithms

STEP 9 - Scaling
The three stage candidate generation - ranking - re-ranking can be scaled well as described earlier. It also meets the requirements of speed (funnel architecture), precision(ranking component), and diversity (multiple candid generation).
Cold start problem:
new users: two tower architectures accepts new users and we can still use user profile info even with no interaction
new items: recommend to random users and collect some data - then fine tune the model using new data
Training:
We need to be able to fine tune the model

Exploration exploitation trade-off :
Multi-armed bandit (an agent repeatedly selects an option and receives a reward/cost. The goal of to maximize its cumulative reward over time, while simultaneously learning which options are most valuable.)

