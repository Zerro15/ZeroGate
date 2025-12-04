"""Auth schema for token response."""
from pydantic import BaseModel


class Token(BaseModel):
    """Token response DTO."""

    access_token: str
    token_type: str = "bearer"
