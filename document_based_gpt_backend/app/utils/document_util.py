# Import necessary classes from LangChain community modules for document processing
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def load_new_documents(directory_path: str):
    """
    Load, split, and format documents from the specified directory.

    This function reads all text files from the given directory, splits their content into smaller chunks
    while preserving some overlap for context, and returns a list of documents in a structured format with metadata.

    Args:
        directory_path (str): Path to the directory containing documents to be loaded.

    Returns:
        list: A list of `Document` objects, each containing content chunks and associated metadata.
    """

    # Initialize the DirectoryLoader to read text files from the specified directory.
    # The `glob` parameter specifies that only `.txt` files will be read.
    loader = DirectoryLoader(directory_path, glob="*.txt")

    # Load the documents from the specified directory path.
    documents = loader.load()

    # Create a text splitter to divide the content into chunks.
    # `chunk_size` specifies the maximum size of each chunk (in characters).
    # `chunk_overlap` specifies the overlap (in characters) between consecutive chunks.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # Initialize a list to store split documents with metadata.
    split_docs_with_metadata = []

    # Loop over each document and split its content.
    for doc in documents:
        # Split the content of the document into chunks.
        chunks = text_splitter.split_text(doc.page_content)

        # Enumerate over each chunk and associate metadata such as source file and chunk index.
        for i, chunk in enumerate(chunks):
            # Create a `Document` object for each chunk and append it to the list.
            split_docs_with_metadata.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": doc.metadata["source"],  # Original source file of the document
                        "chunk_index": i  # Index of the chunk within the source file
                    }
                )
            )

    # Return the list of structured documents with content chunks and metadata.
    return split_docs_with_metadata
