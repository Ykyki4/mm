from datetime import datetime
from decimal import Decimal
from typing import List

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field()
    first_name: str
    last_name: str
    password: str
    sales: List["Sale"] = Relationship(back_populates="user")


class Sale(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(nullable=True)
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="sales")
    created_at: datetime = Field(default_factory=datetime.now)
    invoices: List["Invoice"] = Relationship(back_populates="sale")


class Invoice(SQLModel, table=True):
    id: int = Field(primary_key=True)
    sale_id: int = Field(foreign_key="sale.id")
    sale: Sale = Relationship(back_populates="invoices")
    created_at: datetime = Field(default_factory=datetime.now)
