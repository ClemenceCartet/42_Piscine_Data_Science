import configparser
import psycopg2
from psycopg2 import OperationalError
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


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
            """SELECT SUM(price) FROM customers.customersv3 \
            WHERE event_type = 'purchase' GROUP BY user_id"""
        )
        data = cursor.fetchall()
        cursor.close()
        connect.close()
        kmeans_kwargs = {
            "init": "k-means++",
            "n_init": 10,
            "max_iter": 300,
            "random_state": 42,
        }
        sse = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            kmeans.fit(data)
            sse.append(kmeans.inertia_)
        plt.plot(range(1, 11), sse)
        plt.xlabel("Number of clusters")
        plt.title("The Elbow Method")
        plt.grid()
        plt.show()

    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
