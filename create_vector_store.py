from config import load_db_url
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain.docstore.document import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

from config import load_google_api_key
from crud.model import Base, Info

load_google_api_key()
all_docs: list[Document] = []

# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".pdf": PyPDFLoader,
    ".html": UnstructuredHTMLLoader,
}

DATASOURCE_DIR = os.environ.get("DATASOURCE_DIR", "data_sources")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


def create_vector_store():
    engine = create_engine(load_db_url())
    Base.metadata.create_all(engine)

    for root, _, files in os.walk(DATASOURCE_DIR):
        for file in files:
            _, extension = os.path.splitext(file)
            loader = LOADER_MAPPING.get(extension)
            if loader:
                print(f"Loading {file} to vector store")
                loader = loader(os.path.join(root, file))
                data = loader.load()
                all_docs.extend(data)

    text_splitter = SemanticChunker(
        embeddings=embeddings, breakpoint_threshold_type="gradient"
    )
    docs = text_splitter.create_documents([doc.page_content for doc in all_docs])
    with Session(engine) as session:
        for doc in docs:
            embedding = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004"
            ).embed_query(doc.page_content)
            info = Info(text=doc.page_content, embedding=embedding)
            session.add(info)
        session.commit()
        print("Vector store created successfully")


if __name__ == "__main__":
    create_vector_store()
