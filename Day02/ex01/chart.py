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

        with open("ex01/chart1.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        data = cursor.fetchall()
        date, nb_customer = zip(*data)
        plt.plot(date, nb_customer)
        plt.xticks(date[::31], labels=["Oct", "Nov", "Dec", "Jan", "Fev"])
        plt.ylabel("Number of customers")
        plt.show()

        with open("ex01/chart2.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        data = cursor.fetchall()
        _, sales = zip(*data)
        plt.bar(["Oct", "Nov", "Dec", "Jan", "Fev"], sales)
        plt.xlabel("Month")
        plt.ylabel("Total sales in million")
        plt.show()

        with open("ex01/chart3.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        data = cursor.fetchall()
        date, sales = zip(*data)
        plt.fill_between(date, 0, sales)
        plt.xticks(date[::31], labels=["Oct", "Nov", "Dec", "Jan", "Fev"])
        plt.ylabel("Average spend/customer")
        plt.show()

        cursor.close()
        connect.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
