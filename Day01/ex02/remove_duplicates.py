import csv
from io import StringIO
from datetime import timedelta
import psycopg2
from psycopg2 import OperationalError


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


def check_tuple(first, second) -> bool:
    """Check if the five last variables in tuple ar the same"""
    for i in (1, 5, 1):
        if first[i] != second[i]:
            return False

    return True


def check_duplicate(data, previous, previous_time) -> bool:

    if previous == data:
        return True
    if check_tuple(previous, data) is True:
        if data[0] - previous_time <= timedelta(seconds=1):
            return True

    return False


def create_new_table(cursor):
    new_list: list[tuple] = []
    data = cursor.fetchone()
    tmp_date = data[0]
    new_list.append(
        (str(data[0]), data[1], data[2], data[3], data[4], data[5])
    )
    data = cursor.fetchone()
    i = 0
    while data is not None:
        print(i)
        if check_duplicate(data, new_list[-1], tmp_date) is False:
            new_list.append(
                (str(data[0]), data[1], data[2], data[3], data[4], data[5])
            )
        tmp_date = data[0]
        data = cursor.fetchone()
        i += 1

    return new_list


def send_chunk(input_list: list, cursor):
    data_size = len(input_list)
    chunk_size = 100000
    j = chunk_size
    output: list[list[tuple]]= []
    for i in range(0, data_size, chunk_size):
        output_list = input_list[i:j]
        buffer = StringIO()
        writer = csv.writer(buffer)
        for row in output_list:
            writer.writerow(row)
        buffer.seek(0)
        cursor.copy_expert(
            sql="""COPY customers.customersV2 FROM STDIN WITH CSV""",
            file=buffer,
        )
        buffer.truncate(0)
        buffer.seek(0)
        j += chunk_size
    return output


def main():  # from io import StringIO
    """Main function"""
    try:
        connect = create_connection(
            "piscineds", "ccartet", "mysecretpassword", "localhost", "5432"
        )
        connect.autocommit = True
        cursor = connect.cursor()

        create_table = """
            CREATE TABLE IF NOT EXISTS customers.customersV2 (
            event_time TIMESTAMPTZ,
            event_type VARCHAR,
            product_id INTEGER,
            price FLOAT,
            user_id BIGINT,
            user_session UUID
            )
            """
        cursor.execute(create_table)

        query = """SELECT * FROM customers.customers\
            ORDER BY event_type, product_id, price,\
                user_id, user_session, event_time"""
        cursor.execute(query)

        new_list = create_new_table(cursor)
        send_chunk(new_list, cursor)
        cursor.close()
        connect.close()

    except OperationalError as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
