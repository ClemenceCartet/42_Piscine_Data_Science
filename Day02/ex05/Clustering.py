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
        with open("ex05/Clustering.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        datas = cursor.fetchall()
        cursor.close()
        connect.close()

        c_groups = {
            "new": [],
            "inactive": [],
            "gold": [],
            "silver": [],
            "platinum": [],
        }
        for data in datas:
            # print(data)
            if data[1] == 1 and data[2] == 2:
                c_groups["new"].append(data[0])
            elif (
                data[1] == 1
                and data[2] == 10
                or data[1] == 2
                and data[2] == 11
            ):
                c_groups["inactive"].append(data[0])
            elif data[1] == 5:
                c_groups["gold"].append(data[0])
            elif data[1] == 4:
                c_groups["silver"].append(data[0])
            elif data[1] == 3:
                c_groups["platinum"].append(data[0])
        new = len(c_groups["new"])
        inactive = len(c_groups["inactive"])
        gold = len(c_groups["gold"])
        silver = len(c_groups["silver"])
        platinum = len(c_groups["platinum"])
        print(
            f"new customers: {new}\ninactive: {inactive}\ngold: {gold}\nsilver: {silver}\nplatinum: {platinum}"
        )

        kmeans_kwargs = {
            "init": "k-means++",
            "n_init": 10,
            "max_iter": 300,
            "random_state": 42,
        }
        kmeans = KMeans(n_clusters=5, **kmeans_kwargs)
        label = kmeans.fit_predict(datas)

        plt.scatter(datas[:, 0], datas[:, 1], c=label)
        plt.xlabel("number of customers")
        plt.show()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
