import os
import pandas as pd
import psycopg2
from psycopg2 import OperationalError


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL, 
  age INTEGER,
  gender TEXT,
  nationality TEXT
)
"""


def load(path: str):
    """Load a data file using pandas library"""
    assert isinstance(path, str), "your path is not valid."
    assert os.path.exists(path), "your file doesn't exist."
    assert os.path.isfile(path), "your 'file' is not a file."
    assert path.lower().endswith('.csv'), "file format is not .csv."
    data = pd.read_csv(path)
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


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor() # open a cursor to perform database operations
    cursor.execute(query) # execute Python SQL queries on database
	# connection.commit() # make the changes to the database persistent
	# cursor.close() # Close cursor and communication with the database
	# connection.close()
    print("Query executed successfully")


def main():
    """Main function, load a csv file and display data for my country with matplotlib"""
    try:
        data = load("../subject/customer/data_2022_oct.csv")
        print(data.dtypes)
        data_types: dict = {}
        for info in data.columns:
            data_types[info] = "blop"
            
        # data_types = {
        #         "event_time": sqlalchemy.DateTime(),
        #         "event_type": sqlalchemy.types.String(length=255),
        #         "product_id": sqlalchemy.types.Integer(),
        #         "price": sqlalchemy.types.Float(),
        #         "user_id": sqlalchemy.types.BigInteger(),
        #         "user_session": sqlalchemy.types.UUID(as_uuid=True)  # Corrected the data type
        #     }
        # data.to_sql(table_name, engine, if_exists='replace', index=False)
        connect = create_connection("piscineds", "ccartet", "mysecretpassword", "localhost", "5432")
        # execute_query(connect)
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    except Exception as msg:
        print(f"{msg.__class__.__name__}: {msg}")
        

if __name__ == "__main__":
    main()
