import mysql.connector
import mysql.connector.pooling

# works for local
# "host": "localhost",
#     "port": "3306",

# works for compose
# "host": "db",
# "port": "3306",

db_config = {
    "host": "localhost",
    "port": "3306",
    # "host": "localhost",
    # "port": "3307",
    # "host": "db",
    # "port": "3306",
    "user": "root",
    "password": "PASSWORD",
    "database": "smarter",
}

pool = mysql.connector.pooling.MySQLConnectionPool \
    (pool_name="pool",
     pool_size=5,
     auth_plugin='mysql_native_password',
     **db_config)