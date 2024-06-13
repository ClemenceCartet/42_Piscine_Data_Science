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

        cursor.execute(
            """SELECT COUNT(price) FROM customers.customersv3 \
            WHERE event_type = 'purchase' \
            GROUP BY user_id HAVING COUNT(price) < 40"""
        )
        data = cursor.fetchall()
        frequency = [item[0] for item in data]
        plt.hist(frequency, bins=5)
        plt.xlabel("frequency")
        plt.ylabel("customers")
        plt.show()

        cursor.execute(
            """SELECT SUM(price) FROM customers.customersv3 \
            WHERE event_type = 'purchase' \
            GROUP BY user_id HAVING SUM(price) < 225"""
        )
        data = cursor.fetchall()
        money = [item[0] for item in data]
        plt.hist(money, bins=5)
        plt.xlabel("monetary value")
        plt.ylabel("customers")
        plt.show()

        cursor.close()
        connect.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
