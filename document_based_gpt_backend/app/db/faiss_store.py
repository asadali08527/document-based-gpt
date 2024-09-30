# FAISS vector store handling - This module handles the creation, update, and retrieval of documents from the FAISS
# vector store.

# Provides functions to interact with the operating system, used here for file path checks.
import os
# import FAISS: A library for efficient similarity search and clustering of dense vectors.
from langchain_community.vectorstores import FAISS
# import OpenAIEmbeddings, provides a way to generate text embeddings using OpenAI models.
from langchain_openai import OpenAIEmbeddings
# Imports configuration values like paths and API keys from the app's config module.
from app.core import config

# Initialize OpenAI embeddings using the provided API key from configuration
openai_embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)


async def update_vector_store(new_docs, vector_store_path: str):
    """
    Update the FAISS vector store with new documents.

    This function checks if a vector store already exists at the specified path.
    If it does, it loads the existing store and adds new documents to it.
    If not, it creates a new vector store using the provided documents.

    Args:
        new_docs (list): A list of documents to be added to the vector store.
        vector_store_path (str): The path to save the FAISS vector store.

    Returns:
        None

    Raises:
        Exception: If the vector store cannot be loaded or updated.
    """
    # Check if vector store already exists at the given path
    if os.path.exists(vector_store_path):
        # Load existing FAISS vector store if the index file is found
        faiss_index = FAISS.load_local(vector_store_path, openai_embeddings, allow_dangerous_deserialization=True)
    else:
        # Create a new FAISS vector store from the documents if the index file doesn't exist
        faiss_index = FAISS.from_documents(new_docs, openai_embeddings)

    # Add new documents to the vector store
    faiss_index.add_documents(new_docs)

    # Save the updated vector store back to disk at the specified path
    faiss_index.save_local(vector_store_path)


def reload_vector_store(vector_store_path: str):
    """
    Reload the FAISS vector store from disk.

    This function loads an existing FAISS vector store from the specified path using
    OpenAI embeddings. It is useful when you need to refresh or access the vector store
    after adding new documents.

    Args:
        vector_store_path (str): The path from where to load the FAISS vector store.

    Returns:
        FAISS: An instance of the loaded FAISS vector store.

    Raises:
        FileNotFoundError: If the vector store file is not found at the specified path.
    """
    # Load existing FAISS vector store from the given path using OpenAI embeddings
    faiss_index = FAISS.load_local(vector_store_path, openai_embeddings, allow_dangerous_deserialization=True)
    return faiss_index


def custom_get_relevant_documents_with_scores(query, retriever, top_k=5):
    """
    Retrieve documents based on query relevance scores using a vector store retriever.

    This function uses a vector store retriever to find documents relevant to the given query
    and returns the top results with their corresponding similarity scores.

    Args:
        query (str): The query for which relevant documents are to be retrieved.
        retriever: The retriever instance that interacts with the vector store.
        top_k (int): The number of top relevant documents to retrieve. Default is 5.

    Returns:
        list of tuples: A list of tuples containing documents and their similarity scores.
    """
    # Use the retriever to perform similarity search on the vector store
    # and get the top `k` documents along with their relevance scores.
    results = retriever.vectorstore.similarity_search_with_score(query, k=top_k)
    return results
