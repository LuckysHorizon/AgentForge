from app.embed import embedding_service

text = "I love Programming"

vector = embedding_service.embed_text(text)

print("Vector: ", vector)
print("Dimensions: ", len(vector))