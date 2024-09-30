# Import necessary modules from LangChain for vector storage and QA chain creation
from langchain.chains import RetrievalQA  # For building QA chains from vector stores
from langchain_openai import OpenAI  # OpenAI integration for LLM-based operations
from langchain_community.document_loaders import DirectoryLoader  # For loading documents from a directory
from langchain_community.vectorstores import FAISS  # FAISS vector store for storing document embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into manageable chunks
from langchain.schema import Document  # Schema for representing documents
from langchain_openai import OpenAIEmbeddings  # For generating OpenAI-based embeddings
import os  # Standard library for OS-level file operations

# Import configurations and constants
from app.core import config

# Import vector store-related functions from the FAISS store module
from app.db.faiss_store import (
    update_vector_store as update_faiss_vector_store,  # For updating vector store
    reload_vector_store as reload_faiss_vector_store,  # For reloading vector store from disk
    custom_get_relevant_documents_with_scores  # For custom document retrieval based on query
)

# Import utility function to load and split new documents
from app.utils.document_util import load_new_documents


def create_vector_store():
    """
    Initialize the vector store by loading documents, generating embeddings,
    and saving them to the FAISS vector store.

    Returns:
        FAISS: The FAISS vector store object created.
    """
    # Generate embeddings using OpenAI
    openai_embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    # Load documents from the specified directory
    loader = DirectoryLoader(config.DOCUMENT_DIRECTORY_PATH, glob="*.txt")

    # Load and split documents into smaller chunks
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # Add metadata (document name and chunk index) to each split document
    split_docs_with_metadata = []
    for doc in documents:
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            split_docs_with_metadata.append(
                Document(page_content=chunk, metadata={"source": doc.metadata["source"], "chunk_index": i})
            )

    # Create a FAISS vector store with generated embeddings
    faiss_index = FAISS.from_documents(split_docs_with_metadata, openai_embeddings)

    # Save the updated vector store to disk
    faiss_index.save_local(f"{config.VECTOR_STORE_PATH}faiss_index")
    print("FAISS index created successfully:", faiss_index)
    return faiss_index


class VectorStoreService:
    """
    A singleton service layer for handling vector store operations, like adding new documents,
    updating the vector store, and retrieving relevant documents based on queries.
    """

    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        """
        Ensure VectorStoreService follows a singleton pattern, ensuring only one instance is created.
        """
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
            cls._instance.__initialize_service(*args, **kwargs)
        return cls._instance

    def __initialize_service(self):
        """
        Initialize the VectorStoreService, setting up the LLM and vector store paths,
        and loading the QA chain if a vector store already exists.
        """
        self.llm = OpenAI(api_key=config.OPENAI_API_KEY)
        self.vector_store_path = f"{config.VECTOR_STORE_PATH}/faiss_index"

        # Check if the FAISS index exists and create it if necessary
        if not self._faiss_index_exists():
            create_vector_store()

        # Initialize the QA chain for query-answering
        self.qa_chain = self._initialize_qa_chain()

    def _faiss_index_exists(self):
        """
        Check if the FAISS index files exist.

        Returns:
            bool: True if the index files exist, otherwise False.
        """
        return os.path.exists(f"{self.vector_store_path}/index.faiss")

    def _initialize_qa_chain(self):
        """
        Initialize the QA chain from the vector store using FAISS.

        Returns:
            RetrievalQA: The QA chain initialized with vector store retriever.
        """
        faiss_index = reload_faiss_vector_store(self.vector_store_path)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=faiss_index.as_retriever()
        )
        return self.qa_chain

    async def reload_qa_chain(self):
        """
        Reload the QA chain to reflect vector store updates, ensuring the latest data is used.
        """
        return self._initialize_qa_chain()

    async def add_document_to_vector_store(self, file):
        """
        Add a new document to the vector store and update the QA chain.

        Args:
            file (UploadFile): The file to be uploaded.

        Returns:
            str: A message indicating the document was added successfully.
        """
        # Save the uploaded file to the document directory
        file_path = f"{config.DOCUMENT_DIRECTORY_PATH}/new_docs/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Load and split new documents
        new_docs = load_new_documents(f"{config.DOCUMENT_DIRECTORY_PATH}/new_docs/")

        # Update the FAISS vector store with the new documents
        await update_faiss_vector_store(new_docs, vector_store_path=self.vector_store_path)

        # Reload the QA chain to reflect the updated vector store
        await self.reload_qa_chain()

        return f"Document '{file.filename}' added and vector store updated successfully."

    def get_relevant_documents(self, query: str, top_k: int = 5):
        """
        Retrieve relevant documents based on a query using the vector store.

        Args:
            query (str): The user query.
            top_k (int): Number of top relevant documents to retrieve.

        Returns:
            list: A list of tuples containing relevant documents and their scores.
        """
        return custom_get_relevant_documents_with_scores(query, self.qa_chain.retriever, top_k)
