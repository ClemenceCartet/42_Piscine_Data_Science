import os
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from io import StringIO


def load(path: str):
    """Load a data file using pandas library"""
    assert isinstance(path, str), "your path is not valid."
    assert os.path.exists(path), "your file doesn't exist."
    assert os.path.isfile(path), "your 'file' is not a file."
    assert path.lower().endswith(".csv"), "file format is not .csv."
    data = pd.read_csv(path, dtype=str)
    print(f"Loading dataset of dimensions {data.shape}")

    return data


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
    directory_path = "subject/item/"
    try:
        assert isinstance(directory_path, str), "your path is not valid."
        assert os.path.exists(directory_path), "this folder doesn't exist."
        assert os.path.isdir(directory_path), "your 'folder' is not a folder."
        connect = create_connection(
            "piscineds", "ccartet", "mysecretpassword", "localhost", "5432"
        )
        connect.autocommit = True
        cursor = connect.cursor()

        for file in os.listdir(directory_path):
            table_name = os.path.splitext(file)[0]
            create_table = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                product_id INTEGER PRIMARY KEY,
                category_id BIGINT,
                category_code VARCHAR,
                brand VARCHAR
                )
                """
            cursor.execute(create_table)
            # cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
            data = load(directory_path + file)
            data.drop_duplicates(
                subset="product_id", keep="first", inplace=True
            )
            buffer = StringIO()
            data.to_csv(buffer, index=None, header=None)
            buffer.seek(0)  # rewind the buffer
            cursor.copy_expert(
                sql=f"""COPY {table_name} FROM STDIN WITH CSV""", file=buffer
            )
            buffer.truncate(0)
            buffer.seek(0)
        cursor.close()
        connect.close()
    except AssertionError as msg:
        print(f"{msg.__class__.__name__}: {msg}")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
