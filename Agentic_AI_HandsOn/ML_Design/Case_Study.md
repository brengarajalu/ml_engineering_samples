https://www.hubnx.com/nodes/9fffa434-b4d0-47d2-9e66-1db513b1fb97


1. GEN AI
2. MULTI-TASK
3. ADV RANKING
4. INFRA
5. LLM


1. LLM
a. Query LLM to find initial data
b. In parallel query search backends for substitute info
c. The initial plan, substitute activities, and grounding data are then fed into an optimization algorithm
to find a trip plan similar to the initial plan that also ensures feasibility.
2. While LLMs contain parametric knowledge learned during training, this knowledge is fixed once the model is trained, making it less adaptable to new, unseen information
Processing and indexing flow:
a. Info is retrieved from KB, CRM tools. Text files are converted to chunks and converted to embeddings
b. Embeddings are generated using BERT, T5 or api models such as text-embedding-ada-002
c. These embeddings are stored in dense retrieval systems such as Vector DB

Retrieval flow:
Dense retrieval system :
a. Documents are encoded to dense vectors forming an embedding space
b. Semantic similarity can be measure using cosine similarity or euclidean distance

Seq to Seq model :
The most relevant data fetched from the dense retrieval system is fed into a seq-to-seq model which is usually an LLM


AI assisted Verification :
Inference can be first done by a model and critic can be done by a seperate LLM model