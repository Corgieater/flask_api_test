from ..models.database_class import pool


# 檢查是否有該order_id
def check_if_order(customer_id, order_id):
    try:
        connect = pool.get_connection()
        cursor = connect.cursor()
        sql = '''SELECT * FROM `order` WHERE customer_id = %s 
        AND order_id = %s'''
        data = (customer_id, order_id)
        cursor.execute(sql, data)
        order = cursor.fetchone()

    except Exception as e:
        print(e)
        return False
    else:
        if order:
            return True
    finally:
        cursor.close()
        connect.close()
