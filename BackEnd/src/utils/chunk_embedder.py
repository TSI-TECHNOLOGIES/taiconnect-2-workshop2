import os
import json
from src import embedding
from src import configData
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class chunkEmbedder:
    def __init__(self):
        self.configData = configData
        self.pdfPath =  self.configData["pdfPath"]
        self.model_name = self.configData["modelName"]
        self.model_kwargs = {'device': 'cpu'}
        self.encode_kwargs = {'normalize_embeddings': False}
        self.embedding =  embedding
        self.vectorDBPath = self.configData["vectorDBPath"]
    
    def pdfLoader(self):
        all_documents = []
    
        for file in os.listdir(self.pdfPath):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(self.pdfPath, file)
                loader = PyPDFLoader(pdf_path)
                documents = loader.load()
                all_documents.extend(documents)

        return all_documents
    
    def document_splitter(self):
        document_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,
                                          chunk_overlap=150)
        chunks = document_splitter.split_documents(self.pdfLoader())
        return chunks
    
    def save_to_chroma(self , chunks):
        dummy = False
        if dummy:
            if os.path.exists(self.chroma_path+f"/{self.file_name}"):
                pass
        else:
            db = Chroma.from_documents(
            chunks,
            self.embedding,
            persist_directory= self.vectorDBPath
                )
            db.persist()

    def main(self):
        chunks = self.document_splitter()
        self.save_to_chroma(chunks)
        return self.pdfPath
        