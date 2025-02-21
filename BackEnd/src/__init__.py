import json
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

with open('config.json') as config_file:
    configData = json.load(config_file)

model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embedding =  HuggingFaceEmbeddings(
    model_name=configData["modelName"],
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)