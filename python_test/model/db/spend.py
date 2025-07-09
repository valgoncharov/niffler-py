from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field
from datetime import datetime


class UserName(BaseModel):
    username: str


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    category: str = Field(index=True)
    username: str = Field(index=True)


class Spend(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    amount: float = Field(index=True)
    description: str = Field(index=True)
    category: str = Field(index=True)
    spendDate: datetime = Field(index=True)
    username: str = Field(index=True)
