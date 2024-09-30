import logging


# Log the query and the response
def log_query_response(query: str, response: str):
    logging.info(f"Query: {query}\nResponse: {response}\n---")
