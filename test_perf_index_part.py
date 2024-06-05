import os
import mysql.connector
from dotenv import load_dotenv
import time
import numpy as np
import matplotlib.pyplot as plt
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


@pytest.fixture(scope="module")
def db_connection():
    # Подключение к базе данных
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    yield cursor
    # Закрытие соединения после завершения тестов
    cursor.close()
    conn.close()


def test_add_index(db_connection):
    table_name = 'random_strings_big'
    column1 = 'col1'
    column2 = 'col2'
    column3 = 'col3'
    column4 = 'col4'
    cursor = db_connection
    target_value1, target_value2, target_value3, target_value4 = '%ny%', '%cv%', '%ot%', '%hq%'


    # Добавление индекса
    cursor.execute(f"CREATE INDEX idx_1 ON {table_name}({column1}, {column2}, {column3}, {column4});")

    tests_amount = 500
    time_values = np.zeros(tests_amount)  # Создание массива numpy для хранения времени выполнения

    for i in range(tests_amount):
        cursor.execute(f"FLUSH TABLE {table_name};")
        query = (f"SELECT {column1}, {column2}, {column3}, {column4} FROM {table_name} WHERE "
                 f"{column1} LIKE '{target_value1}' "
                 f"AND {column2} LIKE '{target_value2}' "
                 f"AND {column3} LIKE '{target_value3}' "
                 f"AND {column4} LIKE '{target_value4}';")
        start = time.time()
        cursor.execute(query)
        end = time.time()
        a = cursor.fetchall()
        time_values[i] = end - start  # Заполнение массива времени выполнения



    cursor.execute(f"DROP INDEX idx_1 ON {table_name};")



    avg_time = np.mean(time_values)  # Использование numpy для вычисления среднего времени
    median_time = np.median(time_values)  # Медиана
    std_dev_time = np.std(time_values)  # Стандартное отклонение
    percentile_25 = np.percentile(time_values, 25)  # 25-й перцентиль
    percentile_75 = np.percentile(time_values, 75)  # 75-й перцентиль

    print(f"\nСреднее время выполнения запроса: {avg_time} секунд")
    print(f"Максимальное время выполнения запроса: {np.max(time_values)} секунд")
    print(f"Минимальное время выполнения запроса: {np.min(time_values)} секунд")
    print(f"Медиана времени выполнения запроса: {median_time} секунд")
    print(f"Стандартное отклонение времени выполнения запроса: {std_dev_time} секунд")
    print(f"25-й перцентиль времени выполнения запроса: {percentile_25} секунд")
    print(f"75-й перцентиль времени выполнения запроса: {percentile_75} секунд")

    # Гистограмма времени выполнения запросов
    plt.hist(time_values, bins=30, edgecolor='black')
    plt.title('Гистограмма времени выполнения запросов \nс индексом при поиске подстроки')
    plt.xlabel('Время выполнения (секунды)')
    plt.ylabel('Частота')
    plt.axvline(median_time, color='red', linestyle='dashed', linewidth=2)
    plt.legend({'Медиана': median_time})

    stats_text = (f"Среднее: {avg_time:.6f} сек\n"
                  f"Медиана: {median_time:.6f} сек\n"
                  f"Максимальное: {np.max(time_values):.6f} сек\n"
                  f"Минимальное: {np.min(time_values):.6f} сек\n"
                  f"Стд. отклонение: {std_dev_time:.6f} сек\n"
                  f"25-й перцентиль: {percentile_25:.6f} сек\n"
                  f"75-й перцентиль: {percentile_75:.6f} сек")

    plt.text(0.95, 0.95, stats_text, fontsize=10, verticalalignment='top', horizontalalignment='right',
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))

    plt.show()



if __name__ == "__main__":
    pytest.main()