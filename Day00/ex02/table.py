import os
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    print("Connection to PostgreSQL DB successful")

    return connection


def execute_query(connection, query):
    connection.autocommit = True
    cursor = (
        connection.cursor()
    )  # open a cursor to perform database operations
    cursor.execute(query)  # execute Python SQL queries on database
    print("Query executed successfully")
    cursor.close()


def main():
    """Main function"""
    try:
        connect = create_connection(
            "piscineds", "ccartet", "mysecretpassword", "localhost", "5432"
        )
        create_users_table = """
            CREATE TABLE IF NOT EXISTS data_2022_oct (
            event_time TIMESTAMPTZ,
            event_type VARCHAR,
            product_id INTEGER,
            price FLOAT,
            user_id BIGINT,
            user_session UUID
            )
            """
        execute_query(connect, create_users_table)
        connect.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
