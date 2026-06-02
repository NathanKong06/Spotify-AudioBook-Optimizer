import json
from models.audiobook import Audiobook

def save_books(books: list) -> str:
    """
    Serializes a list of Audiobook objects into a JSON string.
    Args:
        books (list): List of Audiobook objects to serialize.
    Returns:
        str: A JSON-formatted string representing the list of books.
    """
    return json.dumps(
        [
            {
                "title": b.title,
                "minutes": b.minutes
            }
            for b in books
        ],
        indent = 4
    )

def load_books(uploaded_file: json) -> list:
    """
    Deserializes a JSON file into a list of Audiobook objects.
    Args: 
        uploaded_file (json): A JSON file containing an array of book objects.
    Returns: 
        list: A list of Audiobook objects created from the JSON data.
    """
    payload = json.load(uploaded_file)
    return [
        Audiobook(
            title=item["title"],
            minutes=item["minutes"]
        )
        for item in payload
    ]