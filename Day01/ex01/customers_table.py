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


def main():
    """Main function"""
    try:
        connect = create_connection(
            "piscineds", "ccartet", "mysecretpassword", "localhost", "5432"
        )
        connect.autocommit = True
        cursor = connect.cursor()
        cursor2 = connect.cursor()
        # query0 = """SELECT * FROM pg_tables WHERE schemaname='customers'"""
        cursor.execute(
            """SELECT * FROM information_schema.tables
        WHERE table_name like 'data_202%'"""
        )
        table_infos = cursor.fetchone()
        cursor2.execute(
            f"""CREATE TABLE IF NOT EXISTS customers.customers\
                AS TABLE customers.{table_infos[2]}"""
        )
        table_infos = cursor.fetchone()
        while table_infos is not None:
            cursor2.execute(
                f"""INSERT INTO customers.customers\
                    SELECT * FROM customers.{table_infos[2]}"""
            )
            table_infos = cursor.fetchone()
        cursor.close()
        cursor2.close()
        connect.close()

    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
