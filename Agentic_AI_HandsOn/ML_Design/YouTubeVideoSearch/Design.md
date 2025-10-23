STEP 1 : Problem formulation
    What is the primary (business) objective of the search system?
    What are the specific use cases and scenarios where it will be applied?
    What are the system requirements (such as response time, accuracy, scalability, and integration with existing systems or platforms)?
    What is the expected scale of the system in terms of data and user interactions?
    Is their any data available? What format?
    Can we use video metadata? Yes
    Personalized? not required
    How many languages needs to be supported?

    A. Use case(s) and business goal:
    Use case: user enters text query into search box, system shows the most relevant videos
    business goal: increase click through rate, watch time, etc.

    B. Requirements and Constraints
    Response time, Accuracy, Scalability (50M DAU)
    Constraints : budget limitations, hardware limitations, or legal and privacy constraints

    C. Data Sources and Availability
    Sources: videos (1B), text
    10M pairs of <video, text_query>. Videos have metadata (title, description, tags) in text format

    D. ML Formulation
    ML Objective: retrieve videos that are relevant to a text query
    ML I/O: I: text query from a user, O: ranked list of relevant videos on a video sharing platform
    ML category: Visual search + Text Search systems
   
    

STEP 2 : METRICS
    A. OFFLINE METRICS
        Precision @k, mAP, Recall@k, MRR
        we choose MRR (avg rank of first relevant element in results) due to the format of our eval data <video, text> pair
    B. ONLINE METRICS
        CTR: problem: doesn't track relevancy, click baits
        video completion rate: partially watched videos might still found relevant by user
        total watch time
        we choose total watch time: good indicator of relevance

STEP 3 : ARCH. COMPONENTS
   A. VISUAL SEARCH SYSTEM
       1. Text query -> videos (based on similarity of text and visual content)
       2. Two tower embedding architecture (video and text_query encoders)
   B. TEXTUAL SEARCH SYSTEM
       1. search for most similar titles, descs, and tags w/ text query
       2. we can use Inverted Index (e.g. elastic search) for efficient full text search
        An inverted index is a data structure that maps terms (words) to the documents or locations where they appear, enabling efficient text-based document retrieval, commonly used in search engines.

STEP 4 : DATA COLLECTION AND PREPARATION
       1. Text Preprocessing - normalize and tokenize the text, token to id's
       2. Video pre-processing - decode to frames, sample, resize, normalize

STEP 5 : MODEL DEVELOPMENT AND EVALUATION
       1. Model Selection
          Text to vector encodings :
          Statistical approach : TF-IDF, BOW 
          tf-idf - create a matrix of tf-idf scores for each word in the doc creating TF-IDF matrix
          ML encoder : BERT, word2vec
          BERT is beneficial here because it takes the context of left and right word - 
          BERT embeddings are the contextualized word representations learned during the pre-training phase
          bert is resource intensive, requires pretrained models, needs fine tuning, token limits of 512, quadratic complexity for attention
        
       2. Video encoding
         Video level : Vivit expensive but has temporal understanding
         Frame level : from sample frames and aggregate. example : Vit

STEP 6 : PREDICTION SERVICE
       A. Visual search from text query
        text -> preprocess -> encoder -> embedding
        videos are indexed by their encoded embeddings
        search: using approximate nearest neighbor search (ANN) such FAISS. Use tree based ANN, LSH and clustering based
        Approximate Nearest Neighbor techniques speed up the search by preprocessing the data into an efficient index using techniques such as vector transformation
       B. Textual search using Elastic Search
       C. Ranking re-rank based on weighted sum of rel scores