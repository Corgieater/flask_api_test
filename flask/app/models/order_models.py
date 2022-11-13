from datetime import datetime
from ..models.database_class import pool


# 拿訂單資訊
def get_order_details(customer_id, order_id):
    try:
        connect = pool.get_connection()
        cursor = connect.cursor()
        sql = '''SELECT `order`.order_id,`products`.product_name, `products`.price,
        `order_item`.amount, `order`.purchase_time, `order`.total  
        FROM `order` 
        INNER JOIN `order_item` ON `order`.order_id = `order_item`.order_id 
        INNER JOIN `customer` ON `order`.customer_id = `customer`.customer_id 
        INNER JOIN `products` ON `order_item`.product_id = `products`.product_id 
        WHERE `order`.customer_id =%s AND `order`.order_id = %s'''

        data = (customer_id, order_id)
        cursor.execute(sql, data)
        order_details = cursor.fetchall()

        data = {'order_id': order_id,
               'total_price': 0,
               'purchase_time': '',
               'customer_id': customer_id,
               'product': [],
                'product_price':[],
               'amount':[]
                }
        for i in range(len(order_details)):
            data['total_price'] = order_details[i][5]
            data['purchase_time'] = order_details[i][4]
            data['product'].append(order_details[i][1])
            data['amount'].append(order_details[i][3])
            data['product_price'].append(order_details[i][2])

    except Exception as e:
        print(e)

        return False
    else:
        connect.commit()
        return data
    finally:
        cursor.close()
        connect.close()


# 先建立ORDER和算出多少錢建檔
def add_new_order_func(customer_id, product_id, amount):
    try:
        connect = pool.get_connection()
        cursor = connect.cursor()
        current_time = datetime.now()
        # 這邊會先做一次檢查 product_id僅有1和2，亂打會跳出去
        total_price = calculate_money(cursor, product_id, amount)
        if total_price is False:
            return False
        else:
            sql = 'INSERT INTO `order` (order_id, customer_id, purchase_time, total) ' \
                  'VALUES (DEFAULT, %s, %s, %s)'
            data = (customer_id, current_time, total_price)
            cursor.execute(sql, data)
            cursor.execute('SELECT LAST_INSERT_ID()')
            order_id = cursor.fetchone()[0]
            for i in range(len(product_id)):
                connect_order_with_order_item(cursor, order_id, product_id[i], amount[i])
    except Exception as e:
        connect.rollback()
        print(e)
        return False
    else:
        connect.commit()
        return {'ok': True,
                'order_id': order_id,
                'total_price': total_price,
                'purchase_time': current_time,
                'customer_id': customer_id}
    finally:
        cursor.close()
        connect.close()


# 修改訂單
def modify_order_func(order_id, product_id, amount, customer_id):
    try:
        connect = pool.get_connection()
        cursor = connect.cursor()
        modify_time = datetime.now()

        for i in range(len(product_id)):
            sql = 'UPDATE `order_item` SET amount = %s ' \
                  'WHERE order_id = %s AND product_id = %s'

            data = (amount[i], order_id, product_id[i])
            cursor.execute(sql, data)

        sql = 'SELECT product_id, amount FROM `order_item` WHERE order_id = %s'
        data = (order_id,)
        cursor.execute(sql, data)
        products = cursor.fetchall()
        new_data = {'ok': True,
                'order_id': order_id,
                'modified_time': modify_time,
                'product': [],
                'price': [],
                'amount': [],
                'total': 0
                }
        for i in range(len(products)):
            price = get_product_price(cursor, products[i][0])[0]
            new_data['product'].append(products[i][0])
            new_data['price'].append(price)
            new_data['amount'].append(products[i][1])
            new_data['total'] += price*products[i][1]
        sql = 'UPDATE `order` SET total = %s, purchase_time = %s ' \
              'WHERE order_id = %s AND customer_id = %s'
        data = (new_data['total'], modify_time, order_id, customer_id)
        cursor.execute(sql, data)

    except Exception as e:
        connect.rollback()
        print(e)
        return False
    else:
        connect.commit()
        return new_data
    finally:
        cursor.close()
        connect.close()


# 拿product價格，同時檢查是否有該product
def get_product_price(cursor, product_index):
    sql = 'SELECT price FROM `products` where product_id = %s'
    cursor.execute(sql, (product_index,))
    data = cursor.fetchone()
    if data is None:
        return False
    return data


# 算錢
def calculate_money(cursor, product_id, amount):
    total_price = 0
    for i in range(len(product_id)):
        price = get_product_price(cursor, product_id[i])
        total_price += price[0] * amount[i]
    return total_price


# 把使用者買的東西記錄在order_item
def connect_order_with_order_item(cursor, order_id, product_id, amount):
    sql = 'INSERT INTO `order_item` (order_id, product_id, amount) ' \
          'VALUES (%s, %s, %s)'
    data = (order_id, product_id, amount)
    cursor.execute(sql, data)

