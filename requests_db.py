from mysql.connector import connect, Error
from config import data_db


def create_database():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
    ) as connection:
        create_database_query = "CREATE DATABASE IF NOT EXISTS building_bot"
        cursor = connection.cursor()
        cursor.execute(create_database_query)


def create_users_table():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        create_table = """
            CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
                role_users VARCHAR(45) NOT NULL,
                name VARCHAR(120) NOT NULL UNIQUE,
                tag_telegram VARCHAR(120) NOT NULL UNIQUE
            )
        """
        cursor = connection.cursor()
        cursor.execute(create_table)
        connection.commit()


def create_brigade_table():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        create_table = """
            CREATE TABLE IF NOT EXISTS brigade(
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
                name_brigade VARCHAR(45) NOT NULL UNIQUE,
                responsible_employer VARCHAR(120) NOT NULL,
                employers VARCHAR(120) NOT NULL
            )
        """
        cursor = connection.cursor()
        cursor.execute(create_table)
        connection.commit()


def add_user(role_user, name, tag_telegram):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        insert_user = """
            INSERT IGNORE INTO users (role_users, name, tag_telegram)
            VALUES (%s, %s, %s)
        """
        cursor = connection.cursor()
        info_user = (role_user, name, tag_telegram)
        cursor.execute(insert_user, info_user)
        connection.commit()


def select_all_user():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_user = """
            SELECT name FROM users
        """
        cursor = connection.cursor()
        cursor.execute(select_user)
        users = cursor.fetchall()
        return users

