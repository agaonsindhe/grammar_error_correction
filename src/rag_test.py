from transformers import RagTokenizer, RagRetriever

tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq")

query = "What is the capital of France?"
input_ids = tokenizer(query, return_tensors="pt")["input_ids"]
retrieved_docs = retriever(input_ids.numpy())

print(len(retrieved_docs["docs"]))