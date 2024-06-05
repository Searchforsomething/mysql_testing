import os
import mysql.connector
import random
import string
from dotenv import load_dotenv

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

columns_number = 5
rows = 25

# Подключение к базе данных
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Название таблицы
table_name = 'random_strings'

# Удаление таблицы, если она существует
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Создание таблицы с 5 столбцами
columns = ", ".join([f"col{i+1} VARCHAR(50)" for i in range(columns_number)])
create_table_query = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
cursor.execute(create_table_query)

# Функция для генерации случайной строки
def generate_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(5))


# Заполнение таблицы случайными комбинациями символов
for _ in range(rows):
    values = ", ".join([f"'{generate_random_string()}'" for _ in range(columns_number)])
    insert_query = f"INSERT INTO {table_name} ({', '.join([f'col{i+1}' for i in range(columns_number)])}) VALUES ({values})"
    cursor.execute(insert_query)

# Фиксирование изменений
conn.commit()

# Закрытие соединения
cursor.close()
conn.close()

print("Таблица успешно создана и заполнена случайными комбинациями символов.")
