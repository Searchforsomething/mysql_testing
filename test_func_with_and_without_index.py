import os
import mysql.connector
from dotenv import load_dotenv
import pytest

load_dotenv()

user_name = os.getenv('USER_NAME')
password = os.getenv('USER_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')

# Параметры подключения к базе данных
config = {
    'user': user_name,
    'password': password,
    'host': host,
    'database': database,
}

table_name = 'random_strings'
no_index_results = []

@pytest.fixture(scope="module")
def db_connection():
    # Подключение к базе данных
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    yield cursor
    # Закрытие соединения после завершения тестов
    cursor.close()
    conn.close()

def test_func(db_connection):
    cursor = db_connection
    with open('sql_query.txt', 'r') as file:
        for query in file:
            cursor.execute(query)
            no_index_results.append(cursor.fetchall())

    cursor.execute(f"CREATE INDEX idx_1 ON {table_name}(col1, col2, col3, col4, col5);")

    i = 0
    with open('sql_query.txt', 'r') as file:
        for query in file:
            cursor.execute(query)
            assert no_index_results[i] == cursor.fetchall()
            i += 1

    cursor.execute(f"DROP INDEX idx_1 ON {table_name};")

if __name__ == "__main__":
    pytest.main()