import numpy as np

from app.embed import embedding_service
from app.llm import call_llm 

class BasicRAG:

    def __init__(self, documents: list[str]):

        self.documents = documents 

        self.vectors = (
            embedding_service.embed_documents(
                documents
            )
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 3
    ):
        query_vector = np.array(
            embedding_service.embed_text(question)
        )

        document_vectors = np.array(
            self.vectors
        )

        scores = document_vectors @ query_vector

        ranked_indices = np.argsort(scores)[::-1]

        results = []

        for index in ranked_indices[:top_k]:
            results.append({
                "document": self.documents[index],
                "score": float(scores[index])
            })

        return results 

    def ask(self, question: str):
        results = self.retrieve(
            question,
            top_k=3
        )

        context = "\n".join(
            result["document"]
            for result in results
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "Answer only using the supplied context. "
                    "If the answer is not present, say "
                    "'I don't know based on the provided documents'. "
                    "Do not invent information."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question: {question}"
                )
            }
        ]

        response = call_llm(messages)

        return{
            "question" : question,
            "answer": response.choices[0].message.content,
            "sources": results
        }
