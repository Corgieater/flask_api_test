from fastapi import HTTPException
from fastapi import APIRouter
from . import class_file
from .models import order_models
from .models import check_models

router = APIRouter(tags=['order'])


# 用order_id跟customer_id拿訂單資料
@router.post('/order_details')
def get_order_by_order_id_and_customer_id\
                (order_id_customer_id: class_file.Order_id_customer_id):
    # 如果根本沒填值也不用看了
    if order_id_customer_id.order_id is None or \
            order_id_customer_id.customer_id is None:
        raise HTTPException(status_code=400, detail="no customer id or order id")

    # 如果可以透過customer_id和order_id找到，就繼續
    if check_models.check_if_order(order_id_customer_id.customer_id,
                                   order_id_customer_id.order_id):
        result = order_models.get_order_details(
            order_id_customer_id.customer_id, order_id_customer_id.order_id)
        return result
    else:
        raise HTTPException(status_code=400,
                            detail="something went wrong, please check again")


# 下訂單
@router.post('/order')
def place_order(order_item: class_file.Order_item):
    # 沒有customer_id和product_id和amount就不用做了
    if order_item.customer_id is None or len(order_item.product_id) == 0 \
            or len(order_item.amount) == 0:
        raise HTTPException(status_code=400, detail="no product or amount")

    result = order_models.add_new_order_func\
        (order_item.customer_id, order_item.product_id,
         order_item.amount)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="product doesn't exist")


# 修改訂單
@router.patch('/order')
def modify_order(order: class_file.Order):
    # 如果沒有order_id, customer_id或product和amount都是0 就不用管了
    if order.order_id is None or order.customer_id is None \
            or len(order.product_id) == 0 or len(order.amount) == 0:
        raise HTTPException(status_code=400, detail="Please check details again")
    # 檢查是否真的有該使用者下的訂單
    if check_models.check_if_order(order.customer_id, order.order_id):
        return order_models.modify_order_func(order.order_id,
                                              order.product_id, order.amount,
                                              order.customer_id)
    else:
        raise HTTPException(status_code=400,
                            detail="No such order or customer id is wrong")
