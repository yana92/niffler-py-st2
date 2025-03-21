from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool


class AddCategory(BaseModel):
    id: str | None = None
    name: str
    username: str | None = None
    archived: bool | None = None


class Spend(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category_id: str
    spend_date: datetime
    currency: str


class SpendResponse(BaseModel):
    id: str
    amount: float
    description: str
    category: AddCategory
    spendDate: datetime
    currency: str


class AddSpend(BaseModel):
    id: str | None = None
    amount: float
    description: str
    category: AddCategory
    spendDate: str
    currency: Literal["RUB", "EUR", "USD", "KZT"]
