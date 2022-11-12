import mysql.connector
import mysql.connector.pooling


db_config = {
    "host": "db",
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