from .defaultdb import DefaultDatabase

"""
Модуль для управления базой данных игры на sqlite3.

Переменные:
- DATABASE (str): Путь к файлу базы данных.
"""


DATABASE = "database/game.db"


class UserInfo(DefaultDatabase):
    """
    Класс для управления информацией о пользователях.

    Атрибуты:
    - table_name (str): Название таблицы в базе данных.
    
    Методы:
    - __init__(self, db_name=DATABASE): Инициализация объекта, создание таблицы в базе данных.
    - insert_field(self, telegram_id, username, first_name, is_bot): Вставка записи в таблицу.
    - get_telegram_id(self, telegram_id): Получение ID Telegram пользователя из таблицы.

    """
    def __init__(self, db_name=DATABASE):
        super().__init__(db_name)
        self.table_name = "user_info"
        self.create_tables(
            self.table_name,
            "telegram_id INTEGER UNIQUE",
            "username TEXT",
            "first_name TEXT",
            "is_bot INTEGER",
            )

    def insert_field(
        self,
        telegram_id,
        username,
        first_name,
        is_bot,
    ):
        existing_telegram_id = self.get_telegram_id(telegram_id)
        if not existing_telegram_id:
            data = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "is_bot": is_bot
            }
            self.insert_data(self.table_name, data)

    def get_telegram_id(self, telegram_id):
        cursor = self.connect_db.cursor()
        query = f"""
        SELECT telegram_id 
          FROM {self.table_name} 
         WHERE telegram_id = ?
        """
        cursor.execute(query, (telegram_id, ))
        result = cursor.fetchone()
        return result[0] if result else None


class UserProgress(DefaultDatabase):
    """
    Класс для управления прогрессом пользователей в игре.

    Атрибуты:
    - table_name (str): Название таблицы в базе данных.
    
    Методы:
    - __init__(self, db_name=DATABASE): Инициализация объекта, создание таблицы в базе данных.
    - insert_field(self, telegram_id, plot_code): Вставка записи в таблицу.
    - get_plot_code(self, telegram_id): Получение кода сюжета пользователя из таблицы.

    """
    def __init__(self, db_name=DATABASE):
        super().__init__(db_name)
        self.table_name = "user_progress"
        self.create_tables(
            self.table_name,
            "telegram_id INTEGER UNIQUE",
            "plot_code INTEGER",
            )
    
    def insert_field(
        self,
        telegram_id,
        plot_code,
    ):
        data = {
            "telegram_id": telegram_id,
            "plot_code": plot_code,
        }
        self.insert_or_replace_data(self.table_name, data)

    def get_plot_code(self, telegram_id):
        cursor = self.connect_db.cursor()
        query = f"""
        SELECT plot_code
          FROM {self.table_name} 
         WHERE telegram_id = ?
        """
        cursor.execute(query, (telegram_id, ))
        result = cursor.fetchone()
        return result[0] if result else 1


class HeroName(DefaultDatabase):
    """
    Класс для управления именами героев в игре.

    Атрибуты:
    - table_name (str): Название таблицы в базе данных.
    
    Методы:
    - __init__(self, db_name=DATABASE): Инициализация объекта, создание таблицы в базе данных.
    - insert_field(self, telegram_id, hero_name): Вставка записи в таблицу.
    - get_hero_name(self, telegram_id): Получение имени героя из таблицы.

    """
    def __init__(self, db_name=DATABASE):
        super().__init__(db_name)
        self.table_name = "hero_name"
        self.create_tables(
            self.table_name,
            "telegram_id INTEGER UNIQUE",
            "hero_name TEXT",
            )

    def insert_field(
        self,
        telegram_id,
        hero_name,
    ):
        data = {
            "telegram_id": telegram_id,
            "hero_name": hero_name,
        }
        self.insert_or_replace_data(self.table_name, data)

    def get_hero_name(self, telegram_id):
        cursor = self.connect_db.cursor()
        query = f"""
        SELECT hero_name
          FROM {self.table_name} 
         WHERE telegram_id = ?
        """
        cursor.execute(query, (telegram_id, ))
        result = cursor.fetchone()
        return result[0] if result else None
