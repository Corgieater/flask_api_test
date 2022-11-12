from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from .class_file import *
from .models import auth
from .models import order_models

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post('/user_logIn')
async def logIn(user:User):
    customer_id = auth.check_user_name(user.user_name)
    if customer_id is None:
        raise HTTPException(status_code=400, detail="no such user")

    return customer_id


@router.post('/order')
def add_item_to_order(order_item: Order_item):
    if order_item.customer_id is None or len(order_item.product_id) == 0 \
            or len(order_item.amount) == 0:
        raise HTTPException(status_code=400, detail="no product or amount")

    return order_models.add_new_order_func\
        (order_item.customer_id, order_item.product_id,
         order_item.amount)


@router.patch('/order')
def modify_order(order: Order):
    if order.order_id is None or len(order.product_id) == 0 or len(order.amount) == 0 \
            or order.customer_id is None:
        raise HTTPException(status_code=400, detail="Please check details again")
    return order_models.modify_order_func(order.order_id,
                                          order.product_id,order.amount,
                                          order.customer_id)