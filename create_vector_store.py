from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain.docstore.document import Document

from langchain_ollama import OllamaEmbeddings
import os

all_docs: list[Document] = []

# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".pdf": PyPDFLoader,
    ".html": UnstructuredHTMLLoader,
}

DATASOURCE_DIR = os.environ.get("DATASOURCE_DIR", "data_sources")


def create_vector_store():
    for root, _, files in os.walk(DATASOURCE_DIR):
        for file in files:
            _, extension = os.path.splitext(file)
            loader = LOADER_MAPPING.get(extension)
            if loader:
                print(f"Loading {file} to vector store")
                loader = loader(os.path.join(root, file))
                data = loader.load()
                all_docs.extend(data)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_splits = text_splitter.split_documents(all_docs)
    persist_dir = "vector_store_dir"

    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=OllamaEmbeddings(model="llama3.2"),
        persist_directory=persist_dir,
    )


if __name__ == "__main__":
    create_vector_store()
