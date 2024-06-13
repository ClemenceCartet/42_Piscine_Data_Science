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
        with open("ex05/Clustering.sql", "r") as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        datas = cursor.fetchall()

        c_groups = {
            "new": 0,
            "inactive": 0,
            "gold": 0,
            "silver": 0,
            "platinum": 0,
        }
        for data in datas:
            # print(data)
            if data[1] == 1 and data[2] == 2:
                c_groups["new"] += 1
            elif data[1] == 1 and data[2] == 10 or data[1] == 2 and data[2] == 11:
                c_groups["inactive"] += 1
            elif data[1] == 5:
                c_groups["gold"] += 1
            elif data[1] == 4:
                c_groups["silver"] += 1
            elif data[1] == 3:
                c_groups["platinum"] += 1

        # c_groups_list = []
        # for key, value in c_groups.items():
        #     print(f"{key}: {value}")
        #     c_groups_list.append(value)
        # c_groups_list = np.array(c_groups_list).reshape(len(c_groups_list), 1)

        # kmeans_kwargs = {
        #     "init": "k-means++",
        #     "n_init": 10,
        #     "max_iter": 300,
        #     "random_state": 42,
        # }
        # kmeans = KMeans(n_clusters=5, **kmeans_kwargs)
        # label = kmeans.fit_predict(c_groups_list)
        # print(label)

        # plt.figure(figsize=(10, 7))
        # colors = ['r', 'g', 'b', 'p', 'y']
        # for i in range(5):
        #     indices_cluster = np.where(label == i)[0]
        #     print(indices_cluster)
        #     plt.scatter(c_groups_list[indices_cluster, 0], c_groups_list[indices_cluster, 1], color=colors[i])
        # plt.xlabel("number of customers")
        # plt.show()

        cursor.execute(
            """SELECT SUM(price) FROM customers.customersv3 \
            WHERE event_type = 'purchase' GROUP BY user_id"""
        )
        purchases_per_customer = cursor.fetchall()

        kmeans_kwargs = {
            "init": "k-means++",
            "n_init": 10,
            "max_iter": 300,
            "random_state": 42,
        }
        kmeans = KMeans(n_clusters=5, **kmeans_kwargs)
        label = kmeans.fit_predict(purchases_per_customer)
        ppc = np.array([elt for tup in purchases_per_customer for elt in tup]).reshape(
            len(purchases_per_customer), 1
        )
        scaler = StandardScaler()
        ppc_normalized = scaler.fit_transform(ppc)

        plt.figure(figsize=(10, 7))
        colors = ["r", "g", "b", "y", "p"]
        for i in range(5):
            indices_cluster = np.where(label == i)[0]
            plt.scatter(indices_cluster, ppc_normalized[indices_cluster], color=colors[i])
        # plt.scatter(ppc[label == 0, 0], ppc[label == 0, 1], s=100, c="red", label="Cluster 1")
        # plt.scatter(ppc[label == 1, 0], ppc[label == 1, 1], s=100, c="blue", label="Cluster 2")
        # plt.scatter(ppc[label == 2, 0], ppc[label == 2, 1], s=100, c="green", label="Cluster 3")
        # plt.scatter(ppc[label == 3, 0], ppc[label == 3, 1], s=100, c="pink", label="Cluster 4")
        # plt.scatter(ppc[label == 4, 0], ppc[label == 4, 1], s=100, c="yellow", label="Cluster 5")
        # plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c="black", label="Centroids")
        plt.title("Clusters")
        plt.legend()
        plt.show()

        cursor.close()
        connect.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
