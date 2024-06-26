import configparser
import psycopg2
from psycopg2 import OperationalError
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np


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
        with open("ex05/Clustering1.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        datas = cursor.fetchall()

        c_groups = {
            "new": 0,
            "inactive": 0,
            "platinum": 0,
            "gold": 0,
            "silver": 0,
        }
        for data in datas:
            if data[1] == 1 and str(data[2]).find("2023-02") != -1:
                c_groups["new"] += 1
            elif (
                str(data[3]).find("2022-11") != -1
                or str(data[3]).find("2022-10") != -1
            ):
                c_groups["inactive"] += 1
            elif data[1] == 5:
                c_groups["platinum"] += 1
            elif data[1] == 4:
                c_groups["gold"] += 1
            elif data[1] == 3:
                c_groups["silver"] += 1

        print(c_groups)
        plt.barh(c_groups.keys(), c_groups.values())
        plt.xlabel("number of cutsomers")
        plt.ylabel("Total sales in million")
        plt.show()

        with open("ex05/Clustering2.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        datas = cursor.fetchall()
        nb_months = [element[1] for element in datas]
        total_prices = [element[2] for element in datas]
        blop = np.column_stack((nb_months, total_prices))

        kmeans_kwargs = {
            "init": "k-means++",
            "n_init": 10,
            "max_iter": 300,
            "random_state": 42,
        }
        kmeans = KMeans(n_clusters=5, **kmeans_kwargs)
        labels = kmeans.fit_predict(blop)  # identifiant des clusters
        centroids = kmeans.cluster_centers_

        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(blop[i])
        colors = ["b", "g", "r", "c", "m"]
        for i, (label, points) in enumerate(clusters.items()):
            plt.scatter(
                [(point[0]) for point in points],
                [(point[1]) for point in points],
                color=colors[i % len(colors)],
            )

        plt.scatter(
            centroids[:, 0],
            centroids[:, 1],
            marker="x",
            s=80,
            color="r",
        )
        plt.xlabel("months")
        plt.ylabel("total prices")
        plt.show()

        cursor.close()
        connect.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
