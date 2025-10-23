Video Recommendation
-------------------

1. Metrics :
 Offline - Use precision, recall, ranking loss, and logloss.
 Online - Use A/B testing to compare Click Through Rates, watch time, and Conversion rates
Retraining - Train many times during the day to capture temporal changes.

2. Data
videos data
User historic data
Recommendations data
Reviews

3. Clarifying questions
Use case? Homepage?
Does user sends a text query as well?
Business objective?
Increase user engagement (play, like, click, share), purchase?, create a better ultimate gaming experience
Similar to previously played, or personalized for the user? Personalized for the user
User locations? Worldwide (multiple languages)
User’s age group:
Do users have any favorite lists, play later, etc?
How many videos? 100 million
How many users? 100 million DAU
Latency requirements - 200msec?
Data access
Do we log and have access to any data? Can we build a dataset using user interactions ?
Do we have textual description of items?
can users become friends on the platform and do we wanna take that into account?
Free or Paid?

4. ML Objective
Recommend most engaging (define) videos
Max. No. of clicks (clickbait)
Max. No. completed videos/sessions/levels (bias to shorter)
Max. total hours played ()
Max. No. of relevant items (proxy by user implicit/explicit reactions) -> more control over signals, not the above shortcomings
Define relevance: e.g. like is relevant, or playing half of it is, …
ML Objective: build dataset and model to predict the relevance score b/w user and a video
I/O: I: user_id, O: ranked list of videos + relevance score
ML category: Recommendation System

5. Metrics (Offline and Online)
Offline:
precision @k, mAP (mean avg precision), and diversity
Online:
CTR, # of completed, # of purchased, total play time, total purchase, user feedback

6. Architecture :
a. Content-based filtering: suggest items similar to those user found relevant (e.g. liked)
No need for interaction data, recommends new items to users (no item cold start)
Capture unique interests of users
New user cold start
Needs domain knowledge
CF: Using user-user (user based CF) or item-item similarities (item based CF)
Pros
No domain knowledge
Capture new areas of interest
Faster than content (no content info needed)
Cons:
Cold start problem (both user and item)
No niche interest
Hybrid
Parallel hybrid: combine(CF results, content based)
Sequential: [CF based] -> Content based

7. Data Preparation
Users (user profile, historical interactions):
User profile
User_id, username, age, gender, location (city, country), lang, timezone

videos (structures, metadata, video content - what is it?)
video_id, title, date, rating, expected_length?, #reviews, language, tags, description, price, developer, publisher, level, #levels

User-video interactions:
Historical interactions: Play, purchase, like, and search history, etc
User_id, video_id, timestamp, interaction_type(purchase, play, like, impression, search), interaction_val, location
Context: time of the day, day of the week, device, OS

8. Feature Engg
    video metadata features:
    video ID, Duration, Language, Title, Description, Genre/Category, Tags,
    Publisher(popularity, reviews), Release date, Ratings, Reviews, (video content ?) video titles, genres, platforms, release dates, user ratings, and user reviews.
    
    User profile:
    User ID, Age, Gender, Language, City, Country
    
    User-item historical features:
    User-item interactions
    Played, liked, impressions
    purchase history (avg. price)
    User search history
    Context
9. Model Development and Offline Eval
 a. Candidate Generation -
    Matrix Factorization
    Pros: Training speed (only two matrices to learn), Serving speed (static learned embeddings)
    Cons: only relies on user-item interactions (No user profile info e.g. language is used); new-user cold start problem
    Two tower neural network: User Tower, Item Tower Ref: https://www.shaped.ai/blog/the-two-tower-model-for-recommendation-systems-a-deep-dive
    u = Tower_User(User_Features) v = Tower_Item(Item_Features)
    Dot Product: Score(u, v) = u ⋅ v (Most common)
    Cosine Similarity: Score(u, v) = (u ⋅ v) / (||u|| ||v||)
    For Online model we can use Approximate Nearest Neighbor (ANN) search techniques (e.g., Faiss, ScaNN, HNSW). ANN allows us to efficiently find the items whose embeddings v have the highest dot product (or cosine similarity) with the user embedding u, retrieving the top-K candidates in milliseconds.
    Pros: Accepts user features (user profile + user search history) -> better quality recommendation; handles new users, scalable
    Cons: Expensive training, serving speed, cold start, simple scoring
    Loss function : Minimize cross entropy for each positive label and sampled negative examples
 b.  Ranking
    Model Options:
    FF NN (e.g. similar tower network to a tower network) + logistic regression
    Deep Cross Network (DCN)
    Features :
    Video ID embeddings (watched video embedding avg, impression video embedding),
    Video historic
    No. of previous impressions, reviews, likes, etc
    Time features (e.g. time since last play),
    Language embedding (user, item),
    User profile
    User Historic (e.g. search history)
 
 c. Re-Ranking (second level filter):
    Re-ranks items by additional business criteria (filter, promote)
    We can use ML models for clickbait, harmful content, etc or use heuristics
    Examples:
    
    Age restriction filter
    Region restriction filter
    Video freshness (promote fresh content)
    Deduplication
    Fairness, bias, etc

 c. Predicion Service - use approximate nearest neighbor (ANN) algorithms
    two-tower network inference: find the k-top most relevant items given a user ->
    It's a classic nearest neighbor problem -> use approximate nearest neighbor (ANN) algorithms

10. Scaling
    The three stage candidate generation - ranking - re-ranking can be scaled well as described earlier. 
    It also meets the requirements of speed (funnel architecture), precision(ranking component), and diversity (multiple candid generation). 

