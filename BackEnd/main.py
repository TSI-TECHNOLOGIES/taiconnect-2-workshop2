from fastapi import FastAPI
from src.models.models import Item , Embedding
from src.controller.patient_controller import PatientFlow
from src.utils.chunk_embedder import chunkEmbedder

app = FastAPI()

@app.post("/chatbot/")
def create_item(item: Item):
    if item.userType == "patient":
        response =  PatientFlow(item.userType, item.provider, item.userQuery, item.conversationHistory).main()
        return response['response']
    return {"message": "Item received", "data": item}

@app.post("/embedding/")
def create_embedding():
    chunks = chunkEmbedder().main()
    return "success"
