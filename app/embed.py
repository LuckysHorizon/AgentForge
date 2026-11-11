from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2" 
        )
    def embed_text(self, text: str):

        vector = self.model.encode(
            text,
            normalize_embeddings=True 
        )

        return vector.tolist()

    def embed_documents(self, documents: list[str]):

        vectors = self.model.encode(
            documents,
            normalize_embeddings=True  
        )

        return vectors.tolist()

embedding_service = EmbeddingService() 