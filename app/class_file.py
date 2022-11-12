from pydantic import BaseModel
from typing import List


class Order_item(BaseModel):
    customer_id: int
    product_id: List[int]
    amount: List[int]


class Order(BaseModel):
    order_id: int
    customer_id: int
    product_id: List[int]
    amount: List[int]


class User(BaseModel):
    user_name: str