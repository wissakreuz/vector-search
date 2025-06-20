from fastapi import FastAPI
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, PointStruct
from qdrant_client.http.models import VectorParams, Distance
import uuid

app = FastAPI()

# Connexion à Qdrant via le nom du service docker "qdrant"
client = QdrantClient(host="qdrant", port=6333)

# Crée une collection si elle n'existe pas déjà
collection_name = "your_collection"
vector_dim = 4

try:
    client.get_collection(collection_name)
except:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE)
    )
    # Insertion de points d'exemple
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"label": "A"}),
            PointStruct(id=2, vector=[0.4, 0.3, 0.2, 0.1], payload={"label": "B"}),
            PointStruct(id=3, vector=[0.2, 0.1, 0.4, 0.3], payload={"label": "C"})
        ]
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI with Qdrant is running!"}

@app.get("/search")
def search():
    query_vector = [0.1, 0.2, 0.3, 0.4]  # Ex. fixe pour la démo
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5
    )
    return {
        "results": [
            {"id": r.id, "score": r.score, "payload": r.payload}
            for r in results
        ]
    }
