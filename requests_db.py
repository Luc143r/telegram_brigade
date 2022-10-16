from mysql.connector import connect, Error
from config import data_db
from nums_from_string import get_nums


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
                tag_telegram VARCHAR(120) NOT NULL UNIQUE,
                visible BOOLEAN NOT NULL
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
                name_brigade VARCHAR(120) NOT NULL UNIQUE,
                responsible_employer VARCHAR(120) NOT NULL
            )
        """
        cursor = connection.cursor()
        cursor.execute(create_table)
        connection.commit()


def create_project_table():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        create_table = """
            CREATE TABLE IF NOT EXISTS project(
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
                name_project VARCHAR(120) NOT NULL UNIQUE,
                employers VARCHAR(255) NOT NULL,
                brigade VARCHAR(255) NOT NULL
            )
        """
        cursor = connection.cursor()
        cursor.execute(create_table)
        connection.commit()


def create_task_table():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        create_table = """
            CREATE TABLE IF NOT EXISTS tasks(
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
                type_task VARCHAR(60) NOT NULL,
                name_task VARCHAR(120) NOT NULL UNIQUE,
                description VARCHAR(255),
                deadline VARCHAR(60) NOT NULL,
                owner_task VARCHAR(80) NOT NULL,
                executor VARCHAR(120),
                status BOOLEAN NOT NULL
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
            INSERT IGNORE INTO users (role_users, name, tag_telegram, visible)
            VALUES (%s, %s, %s, %s)
        """
        cursor = connection.cursor()
        info_user = (role_user, name, tag_telegram, True)
        cursor.execute(insert_user, info_user)
        connection.commit()


def add_brigade_task(type_task, executor, name_task, description, deadline, owner_task):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        insert_task = """
            INSERT IGNORE INTO tasks (type_task, name_task, description, deadline, owner_task, executor, status)
            VALUES (%s, %s, %s, %s, %s, %s, 0)
        """
        cursor = connection.cursor()
        info_task = (type_task, name_task, description,
                     deadline, owner_task, executor)
        cursor.execute(insert_task, info_task)
        connection.commit()


def add_empl_task(executor, name_task, deadline, owner_task):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        insert_task = """
            INSERT IGNORE INTO tasks (type_task, name_task, deadline, owner_task, executor, status)
            VALUES ('mini', %s, %s, %s, %s, 0)
        """
        cursor = connection.cursor()
        info_task = (name_task, deadline, owner_task, executor)
        cursor.execute(insert_task, info_task)
        connection.commit()


def add_brigade(name_brigade, responsible_employer):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        insert_brigade = """
            INSERT IGNORE INTO brigade (name_brigade, responsible_employer)
            VALUES (%s, %s)
        """
        cursor = connection.cursor()
        info_user = (name_brigade, responsible_employer)
        cursor.execute(insert_brigade, info_user)
        connection.commit()


def add_project(name_project, employers, brigade):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        insert_project = """
            INSERT IGNORE INTO project (name_project, employers, brigade)
            VALUES (%s, %s, %s)
        """
        cursor = connection.cursor()
        info_project = (name_project, employers, brigade)
        cursor.execute(insert_project, info_project)
        connection.commit()


def select_all_user():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_user = """
            SELECT * FROM users WHERE visible=1
        """
        cursor = connection.cursor()
        cursor.execute(select_user)
        users = cursor.fetchall()
        return users


def select_employer():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_employer = """SELECT * FROM users WHERE role_users='user'"""
        cursor = connection.cursor()
        cursor.execute(select_employer)
        users = cursor.fetchall()
        return users


def select_one_user(tag_telegram):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_user = """SELECT * FROM users WHERE tag_telegram=%s"""
        cursor = connection.cursor()
        cursor.execute(select_user, (tag_telegram,))
        user = cursor.fetchone()
        return user


def get_tag_user(id_user):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_tag_user = """SELECT tag_telegram FROM users WHERE id=%s"""
        cursor = connection.cursor()
        cursor.execute(select_tag_user, (id_user,))
        tag_user = cursor.fetchone()
        return tag_user[0]


def select_all_project():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_project = """
            SELECT * FROM project
        """
        cursor = connection.cursor()
        cursor.execute(select_project)
        project = cursor.fetchall()
        return project


def select_one_project(name_project):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_project = """SELECT employers FROM project WHERE name_project=%s"""
        cursor = connection.cursor()
        cursor.execute(select_project, (name_project,))
        id_users = cursor.fetchall()
        return get_nums(id_users[0][0])


def select_id_user(tag):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_user = """
            SELECT * FROM users WHERE tag_telegram=%s
        """
        cursor = connection.cursor()
        cursor.execute(select_user, (tag,))
        users = cursor.fetchone()
        return users


def select_all_brigade():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_brigade = """SELECT * FROM brigade"""
        cursor = connection.cursor()
        cursor.execute(select_brigade)
        brigade = cursor.fetchall()
        return brigade


def select_one_brigade(name_brigade):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_brigade = """SELECT * FROM brigade WHERE name_brigade=%s"""
        cursor = connection.cursor()
        cursor.execute(select_brigade, (name_brigade,))
        brigade = cursor.fetchone()
        return brigade


def select_global_task():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_task = """SELECT * FROM tasks WHERE type_task='global'"""
        cursor = connection.cursor()
        cursor.execute(select_task)
        global_task = cursor.fetchall()
        return global_task


def select_project_task():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_task = """SELECT * FROM tasks WHERE type_task='project'"""
        cursor = connection.cursor()
        cursor.execute(select_task)
        project_task = cursor.fetchall()
        return project_task


def select_mini_task():
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        select_task = """SELECT * FROM tasks WHERE type_task='mini'"""
        cursor = connection.cursor()
        cursor.execute(select_task)
        mini_task = cursor.fetchall()
        return mini_task


def del_brig(name_brigade):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        delete_brigade = """DELETE FROM brigade WHERE name_brigade=%s"""
        cursor = connection.cursor()
        cursor.execute(delete_brigade, (name_brigade,))
        connection.commit()


def del_proj(name_project):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        delete_project = """DELETE FROM project WHERE name_project=%s"""
        cursor = connection.cursor()
        cursor.execute(delete_project, (name_project,))
        connection.commit()


def change_role_user(role, tag):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        cursor = connection.cursor()
        change_role = """UPDATE users SET role_users=%s WHERE tag_telegram=%s"""
        info_user = (role, tag)
        cursor.execute(change_role, info_user)
        connection.commit()


def change_visible(visible, tag):
    with connect(
        host=data_db['host'],
        user=data_db['user'],
        password=data_db['password'],
        database=data_db['database'],
    ) as connection:
        cursor = connection.cursor()
        change_visible = """UPDATE users SET visible=%s WHERE tag_telegram=%s"""
        info_user = (visible, tag)
        cursor.execute(change_visible, info_user)
        connection.commit()
