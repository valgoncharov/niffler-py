from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class UserName(BaseModel):
    username: str


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool


class Spend(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    amount: float = Field(index=True)
    description: str = Field(index=True)
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime = Field(index=True)
    username: str = Field(index=True)
    currency: str


class SpendAdd(BaseModel):
    id: Optional[str] = None
    spendDate: str
    category: Category
    currency: str = 'RUB'
    amount: float
    description: str = ''
    username: str
