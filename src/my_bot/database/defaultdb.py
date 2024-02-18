import os
import sqlite3


"""
Модуль для работы с базой данных SQLite.

Классы:
- DefaultDatabase: Предоставляет базовые операции для работы с базой данных.

"""

class DefaultDatabase:
    """
    Предоставляет базовые методы для работы с базой данных SQLite.

    Атрибуты:
    - db_name (str): Название базы данных.
    - db_exists (bool): Флаг наличия базы данных.

    Методы:
    - __init__(self, db_name="default.db"): Инициализация объекта, установка соединения с базой данных.
    - create_tables(self, table_name, *args): Создание таблицы в базе данных.
    - insert_data(self, table_name, data): Вставка записи в таблицу.
    - insert_or_replace_data(self, table_name, data): Вставка или замена записи в таблице.
    - get_all_data(self, table_name): Получение всех записей из таблицы.
    - delete_row(self, table_name, condition): Удаление записи из таблицы по условию.
    - clear_table(self, table_name): Очистка таблицы.
    - drop_table(self, table_name): Удаление таблицы из базы данных.
    - drop_database(self): Удаление базы данных.

    """
    def __init__(self, db_name="default.db"):
        self.db_name = db_name
        self.db_exists = os.path.exists(self.db_name)
        self.connect_db = sqlite3.connect(self.db_name)

    def create_tables(self, table_name, *args):
        cursor = self.connect_db.cursor()
        columns = ", ".join(args)
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY, 
                {columns}
            )
        """
        cursor.execute(query)
        self.connect_db.commit()

    def insert_data(self, table_name, data):
        cursor = self.connect_db.cursor()
        columns = ", ".join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query= f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})

        """
        values = tuple(data.values())
        cursor.execute(query, values)
        self.connect_db.commit()

    def insert_or_replace_data(self, table_name, data):
        cursor = self.connect_db.cursor()
        columns = ", ".join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query= f"""
            INSERT OR REPLACE INTO {table_name} ({columns})
            VALUES ({placeholders})

        """
        values = tuple(data.values())
        cursor.execute(query, values)
        self.connect_db.commit()

    def get_all_data(self, table_name):
        cursor = self.connect_db.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def delete_row(self, table_name, condition):
        cursor = self.connect_db.cursor()
        query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(query)
        self.connect_db.commit()

    def clear_table(self, table_name):
        cursor = self.connect_db.cursor()
        query = f"DELETE FROM {table_name}"
        cursor.execute(query)
        self.connect_db.commit()

    def drop_table(self, table_name):
        cursor = self.connect_db.cursor()
        query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(query)
        self.connect_db.commit()

    def drop_database(self):
        self.connect_db.close()
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
