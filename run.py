from fastapi import FastAPI
from pydantic import BaseModel
from app.models import order_models
from typing import List


app = FastAPI()


class Order_item(BaseModel):
    customer_id: int
    product_id: List[int]
    amount: List[int]


class Order(BaseModel):
    order_id: int
    customer_id: int
    product_id: List[int]
    amount: List[int]


@app.get('/')
def index():
    return "hey"


# 類似購物車的概念，尚未有order_id
@app.post('/order')
def add_item_to_order(order_item: Order_item):
    return order_models.add_new_order_func\
        (order_item.customer_id, order_item.product_id,
         order_item.amount)


@app.patch('/order')
def modify_order(order: Order):
    return order_models.modify_order_func(order.order_id,
                                          order.product_id,order.amount,
                                          order.customer_id)
