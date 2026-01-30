from pydantic import BaseModel


class SaleCreate(BaseModel):
    title: str
    amount: float
    user_id: str


class SaleUpdate(BaseModel):
    title: str
    amount: float