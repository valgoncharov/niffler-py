from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class UserName(BaseModel):
    username: str

