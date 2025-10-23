STEP 1 : Problem Formulation -
    Clarifying questions :
    Use case?
    event recommendation system similar to eventbrite's.
    What is the main Business objective?
    Increase ticket sales
    Does it need to be personalized for the user? Personalized for the user
    User locations? Worldwide (multiple languages)
    User’s age group:
    How many users? 100 million DAU
    How many events? 1M events / month
    Latency requirements - 200msec?
    Data access
    Do we log and have access to any data? Can we build a dataset using user interactions ?
    Do we have textual description of items?
    Can we use location data (e.g. 3rd party API)? (events are location based)
    Can users become friends on the platform? Do we wanna use friendships?
    Can users invite friends?
    Can users RSVP or just register?
    Free or Paid? Both
 
STEP 2 : ML Formulation
    ML Objective: Recommend most relevant (define) events to the users to maximize the number of registered events
    ML category: Recommendation system (ranking approach)
    rule based system
    embedding based (CF and content based)
    Ranking problem (LTR)
    pointwise, pairwise, listwise
    we choose pointwise LTR ranking formulation
    I/O: In: user_id, Out: ranked list of events + relevance score
    Pointwise LTR classifier I/O: I: <user_id, event_id>, O: P(event register) (Binary classification)

STEP 3 : Metrics
    Offline : precision @k, recall @ k (not consider ranking quality)
    MRR, mAP, nDCG (good, focus on first element, binary relevance, non-binary relevance) -> here event register binary relevance so use mAP
    Online : CTR, Conversion rate, revenue lift

STEP 4 : Architectural components
    Funnel architecture
    We two stage (funnel) architecture for
    candidate generation
    rule based event filtering (e.g. location, etc)
    ranking formulation (pointwise LTR) binary classifier

STEP 5 : Data Preparation
    Data Sources :
    a. Users (user profile, historical interactions)
    b. Events
    c. User friendships
    d. User-event interactions
    e. Context

STEP 6 : Feature Engineering
    Features :
    a. User Features - age, gender, event history
    b. Event Features - 
        1. price, No of registered,
        2. time (event time, length, remained time)
        3. location (city, country, accessibility)
        4. description
        5. host (& popularity)
    c. User Event Features
        event price similarity
        event description similarity
        no. registered similarity
        same city, state, country
        distance
        time similarity (event length, day, time of day)
    d. Social features
       No./ ratio of friends going
       invited by friends (No)
       hosted by friend (similarity)
    e. Context
       Location, time
    Feature Processing :
    One hot (gender), bucketize + one hot 
    Feature PreProcessing :
    Batch (for static) vs Online (streaming, for dynamic) processing
    efficient feature computation (e.g. for location, distance)
    improve: embedding learning - for users and events

STEP 7 - Model development and Offline Evaluation
     Model Selection :
     Binary Classification Problem :
     a. LR  (nonlinear interactions)
     b. GBDT  (good for structured, not for continual learning)
     c. NN (continual learning, expressive, nonlinear rels)
    Dataset
    for each user and event pair, compute features, and label 1 if registered, 0 if not
    class imbalance
    resampling
    use focal loss or class-balanced loss

STEP 8 - Prediction Service
    Candidate generation
    event filtering (millions to hundreds)
    rule based (given a user, e.g. location, type, etc filters)
    Ranking
    compute scores for <usr, event> pairs, and sort
   