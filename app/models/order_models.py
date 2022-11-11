import mysql.connector
import mysql.connector.pooling
import datetime

db_config = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "PASSWORD",
    "database": "smarter",
}

pool = mysql.connector.pooling.MySQLConnectionPool \
    (pool_name="pool",
     pool_size=5,
     auth_plugin='mysql_native_password',
     **db_config)


# 先建立ORDER和算出多少錢建檔
def add_new_order_func(customer_id, product_id, amount):
    try:
        connect = pool.get_connection()
        cursor = connect.cursor()
        current_time = datetime.datetime.now()
        total_price = calculate_money(cursor, product_id, amount)
        sql = 'INSERT INTO `Order` (order_id, customer_id, purchase_time, total) ' \
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

        return {'ok': False,
                'message': 'Something went wrong'}
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


def modify_order_func(order_id, product_id, amount, customer_id):
    try:
        connect = pool.get_connection()
        cursor = connect.cursor()
        modify_time = datetime.datetime.now()

        # 修改order_item訂單
        for i in range(len(product_id)):
            sql = 'UPDATE `Order_item` SET amount = %s ' \
                  'WHERE order_id = %s AND product_id = %s'

            data = (amount[i], order_id, product_id[i])
            cursor.execute(sql, data)

        sql = 'SELECT product_id, amount FROM `Order_item` WHERE order_id = %s'
        data = (order_id,)
        cursor.execute(sql, data)
        products = cursor.fetchall()
        new_total_price = 0
        for i in range(len(products)):
            price = get_product_price(cursor, products[i][0])[0]
            new_total_price += price*products[i][1]
        sql = 'UPDATE `Order` SET total = %s, purchase_time = %s ' \
              'WHERE order_id = %s AND customer_id = %s'
        data = (new_total_price, modify_time, order_id, customer_id)
        cursor.execute(sql, data)

    except Exception as e:
        connect.rollback()
        print(e)
        return {'ok': False,
                'message': 'Something went wrong'}
    else:
        connect.commit()
        return {'ok': True,
                'order_id': order_id,
                }
    finally:
        cursor.close()
        connect.close()


def get_product_price(cursor, product_index):
    sql = 'SELECT price FROM Products where product_id = %s'
    cursor.execute(sql, (product_index,))
    data = cursor.fetchone()
    return data


def calculate_money(cursor, product_id, amount):
    total_price = 0
    for i in range(len(product_id)):
        price = get_product_price(cursor, product_id[i])
        total_price += price[0] * amount[i]
    return total_price


# 把使用者買的東西記錄在order_item
def connect_order_with_order_item(cursor, order_id, product_id, amount):
    sql = 'INSERT INTO `Order_item` (order_id, product_id, amount) ' \
          'VALUES (%s, %s, %s)'
    data = (order_id, product_id, amount)
    cursor.execute(sql, data)

