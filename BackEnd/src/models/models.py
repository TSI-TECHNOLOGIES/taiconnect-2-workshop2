from pydantic import BaseModel

# Define the payload model
class Item(BaseModel):
    userQuery: str
    userType: str
    provider: str
    conversationHistory: list

class Embedding(BaseModel):
    pass