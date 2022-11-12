from ..models.database_class import pool


def check_user_name(name):
    connect = pool.get_connection()
    cursor = connect.cursor()
    try:
        sql = "SELECT customer_id FROM Customer WHERE customer_name = %s"
        data = (name,)
        cursor.execute(sql, data)
        customer_id = cursor.fetchone()
        if customer_id is None:
            return {'ok': False,
                    'message': 'No such user'}
    except Exception as e:
        print("something wrong in check_user_name")
        print(e)
        return {'ok': False,
                'message': 'Something went wrong'}
    else:
        return {'customer_id': customer_id[0]}
    finally:
        cursor.close()
        connect.close()
