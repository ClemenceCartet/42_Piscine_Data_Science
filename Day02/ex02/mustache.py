import configparser
import psycopg2
from psycopg2 import OperationalError
import matplotlib.pyplot as plt


config = configparser.ConfigParser()
config.read("config.ini")


def create_connection():
    connection = psycopg2.connect(
        database=config["Postgres"]["database"],
        user=config["Postgres"]["user"],
        password=config["Postgres"]["password"],
        host=config["Postgres"]["host"],
        port=config["Postgres"]["port"],
    )
    print("Connection to PostgreSQL DB successful")

    return connection


def main():
    """Main function"""
    try:
        connect = create_connection()
        connect.autocommit = True
        cursor = connect.cursor()

        with open("ex02/mustache.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        column_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        to_print = [(col, nb) for col, nb in zip(column_names, data[0])]
        print("\n".join([f"{col}: {nb}" for col, nb in to_print]))

        cursor.execute(
            """SELECT price FROM customers.customersv3 \
        WHERE event_type = 'purchase'"""
        )
        data = cursor.fetchall()
        prices = [item[0] for item in data]
        plt.boxplot(prices, vert=False)
        plt.ylim(0.9, 1.1)
        plt.xlabel("price")
        plt.show()

        plt.boxplot(prices, sym="", vert=False, patch_artist=True)
        plt.ylim(0.9, 1.1)
        plt.xlabel("price")
        plt.show()

        cursor.execute(
            """SELECT SUM(price) FROM customers.customersv3 \
            WHERE event_type = 'cart' GROUP BY user_id"""
        )
        data = cursor.fetchall()
        prices = [item[0] for item in data]
        plt.boxplot(prices, vert=False)
        plt.ylim(0.9, 1.1)
        plt.xlim(-10, 200)
        plt.show()

        cursor.close()
        connect.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
