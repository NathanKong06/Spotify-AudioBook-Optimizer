import json
from models.audiobook import Audiobook

def save_books(books):
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

def load_books(uploaded_file):
    payload = json.load(uploaded_file)
    return [
        Audiobook(
            title=item["title"],
            minutes=item["minutes"]
        )
        for item in payload
    ]