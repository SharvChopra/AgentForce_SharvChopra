# vector_operations.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os


def create_vector_db(text: str, persist_directory: str = "./chroma_db"):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", ""]
    )
    chunks = text_splitter.split_text(text)
    print(f"Split document into {len(chunks)} chunks.")
    os.makedirs(persist_directory, exist_ok=True)
    # embedding_model = SentenceTransformerEmbeddings(model_name = "all-Mini-LM-L6-v2")
    embedding_model = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    vector_db.persist()
    print(f"Vector database created and persisted at {persist_directory}.")
    return vector_db


def load_vector_db(persist_directory: str = "./chroma_db"):
    if not os.path.exists(persist_directory):
        print(
            f"Persisit directory {persist_directory} does not exist. Please create it first.")
        return None
    embedding_model = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=persist_directory,
                       embedding_function=embedding_model)
    print(f"Vector database loaded.")
    return vector_db
