from uuid import uuid4
from fastapi import Response


def generate_user_id():
    return str(uuid4())


def initialize_user(response: Response):
    """Helper function to initialize a user and set the user_id cookie."""
    user_id = generate_user_id()
    response.set_cookie(key="user_id", value=user_id)
    return user_id
