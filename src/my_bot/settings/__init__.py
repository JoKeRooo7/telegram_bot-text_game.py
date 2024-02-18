"""
Файл содержит инициализацию бота и хранилища данных пользователей.

Переменные:
- BOT_TOKEN (str): Токен вашего бота для подключения к API Telegram.
- dp (Dispatcher): Объект Dispatcher для обработки сообщений и команд бота.
- user_info (UserInfo): Объект для хранения информации о пользователях.
- hero_name (HeroName): Объект для управления именами героев в игре.
- user_progress (UserProgress): Объект для отслеживания прогресса пользователей.
- bot (Bot): Объект бота для взаимодействия с API Telegram.
- users_data (dict): Локальное хранилище данных пользователя, где ключ - telegram id, значение - контроллер.
- users_in_game (dict): Локальное хранилище информации о нахождении пользователей в игре, где ключ - telegram id.
- users_story_id (dict): Локальное хранилище для идентификации текущей истории пользователей, где ключ - telegram id.
"""
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from database import (
    UserInfo,
    HeroName,
    UserProgress,
)


BOT_TOKEN = "6667637320:AAHc61wJ19IGY3n7RP2BL1fGc_PSAyS3CYY"


dp = Dispatcher()
user_info = UserInfo()
hero_name = HeroName()
user_progress = UserProgress()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

users_data = {}
users_in_game = {}
users_story_id = {}
