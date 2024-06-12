import configparser
import psycopg2
from psycopg2 import OperationalError
import matplotlib.pyplot as plt


config = configparser.ConfigParser()
config.read('config.ini')


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
        with open("ex00/pie.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        data = cursor.fetchall()
        cursor.close()
        connect.close()
        event_type, count = zip(*data)
        # total_count = sum(count)
        # pourcent = lambda x : round((x * 100) / total_count, 1)
        # pourcent_list = [pourcent(x) for x in count]
        plt.pie(count, labels=event_type, autopct='%1.1f%%')
        plt.show()

    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
