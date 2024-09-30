# Import profanity checking module
from better_profanity import profanity


# Check for profanity in the query
def is_safe_content(text: str) -> bool:
    """
    Checks if the provided text contains any profane or inappropriate content.

    Uses the `better_profanity` library to filter out queries with inappropriate content,
    ensuring that the system only processes "safe" and clean queries.

    Args:
        text (str): The text to be checked for profanity.

    Returns:
        bool: `True` if the text does not contain profanity, otherwise `False`.
    """
    # Check if the text contains any profane words or phrases.
    # Returns `True` if clean; otherwise, `False`.
    return not profanity.contains_profanity(text)


# Check if the response is a negative answer
def is_negative_response(result: str) -> bool:
    """
    Determines if the given response contains a negative or "no information found" type of answer.

    This function is used to identify if the QA system's answer suggests a lack of relevant information,
    such as "I don't know", "not found", or similar phrases that imply the query could not be answered satisfactorily.

    Args:
        result (str): The result or response text to be analyzed.

    Returns:
        bool: `True` if the response contains any negative indicators, otherwise `False`.
    """
    # Keywords or phrases indicating a negative or "no information" answer.
    negative_keywords = [
        "i don't", "i do not", "i'm sorry", "no mention", "not mention", "not found",
        "no information", "cannot find", "does not exist", "not specified", "not mentioned",
        "not available", "no details", "not provided"
    ]

    # Check if any of the negative keywords are present in the response (case insensitive).
    return any(keyword in result.lower() for keyword in negative_keywords)
