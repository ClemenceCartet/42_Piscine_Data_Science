import configparser
import psycopg2
from psycopg2 import OperationalError

config = configparser.ConfigParser()
config.read('ex03/config.ini')

def create_connection():
    connection = psycopg2.connect(
        database=config['Postgres']['database'],
        user=config['Postgres']['user'],
        password=config['Postgres']['password'],
        host=config['Postgres']['host'],
        port=config['Postgres']['port']
    )
    print("Connection to PostgreSQL DB successful")

    return connection

def main():
    """Main function"""
    try:
        connect = create_connection()
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS customers.customersV3 AS\
            SELECT c.event_time, c.event_type, c.user_id, c.user_session, c.price,\
					COALESCE (c.product_id, i.product_id) AS product_id,\
						i.category_id, i.category_code, i.brand\
							FROM customers.customersV2 as c\
								LEFT OUTER JOIN public.item AS i\
									ON c.product_id = i.product_id ORDER BY c.event_time""")
        cursor.close()
        connect.close()

    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()

# USING (product_id);
