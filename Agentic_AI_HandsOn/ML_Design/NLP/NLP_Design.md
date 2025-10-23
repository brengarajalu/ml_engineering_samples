1. Google Translate
  a. Architecture
    Encoder -> Input Seq -> Text embedding -> Positional Encoding -> Transformer ([Self Attention (MHA), Normalization, Feed Forward, Normalization] * N) -> Output Sequence
    Decoder -> Previously generated tokens -> Positional Encoding -> Transformer ([Self Attention (MHA), Normalization, Cross Attention (MHA), Feed Forward, Normalization] * N) -> Prediction head (linear layer + softmax to convert Transformer's output to probabilities over vocabulary) -> Predicted next token
    Difference: Encoder, Decoder
    Cross-attention layer: Each token in decoder can attend to all embeddings in encoder, can integrate info from input sequence during output.
    Self-attention: Encoder, each token attends to all other tokens, to understand entire sequence. Decoder, each token is restricted to only tokens come before.
  b. Training
     Using encoder decoder is not optimal as it is supervised. So use Masked Language model (MLM) 
     Randomly select a subset of tokens in input, and mask them.
     Randomly select a subset of tokens in input, and mask them.
     Feed masked sequence to encoder to understand context
     Feed decoder with the same input, but none of tokens are mased and sequence has been shift one position to the right by insertion of a start token.
     Decoder predicts next token for each position in sequence. Each prediction uses all previous input tokens from encoder.
     Calculate cross-entropy loss over predicted probabilities.
   
  c. Evaluation
    Offline evaluation metrics :
    BLEU (BiLingual Evaluation Understudy) :  count the ratio of matches, with brevity penalty, n-grams precision, weight for different n-gram precisions
    ROUGE (Recall-Oriented Understudy for Gisting Evaluation): recall = # matching n-grams / total # n-grams in reference. Lack of contextual understanding.
  
2. Google smart compose
   Input -> Triggering Service -> Phrase Generator (Beam Search, Long/Low-confidence Filtering) -> Post-processing -> Output.
   Models:
    Sin-cosine positional encoding
    Pros: Fixed encoding don't add extra trainable parameters to the model, computationally efficient. Support for long sequences, as fixed methods can map any position into a representation, such flexibility can handle longer sequences beyond model's training data.
    Cons: Predefined limits to their applicability to sequences below that maximum. Suboptimal performance, as fixed encodings may not capture positional relationships effectively.
    Learned positional encoding: Positional representations are learned during training process.
    Pros: Optimal performance
    Cons: Inefficiency, as it requires additional parameters to be learned during training. Lack of generalization, may overfit.
    
    Recommended :
    Transformer architecture consists of a stack of blocks. Each block contains:
    Multi-head/Self attention: updates each embedding by using the attention mechanism, capturing relationships in sequence by allowing each embedding to attend to its preceding embeddings.
    Feed forward: 2 linear transformations, with ReLU activation in between, to each embedding in sequence independently.
    Pretraining: Cross-entropy loss as loss function for next-token prediction, it measures difference between predicted probabilities and the correct token.  
    
    Metrics:
    Offline - Perplexity - how accurately the model predicts exact sequence of tokens in data, ExactMatch@N
    Online - Based on specific requirements: user engagement metrics, effectiveness metrics, latency, quality.
