import aiogram.exceptions
import re
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from controller import Controller
from enum import Enum, auto
from settings import (
    bot,
    dp,
    hero_name,
    user_info,
    user_progress,
    users_data,
    users_in_game,
    users_story_id
)

"""
Модуль commands является частью вашего проекта и 
содержит обработчики команд для бота.
"""


class UserGameState(Enum):
    """
    Перечисление, представляющее состояния игрока.
    
    Возможные состояния:
    - IN_GAME: Игрок находится в игре.
    - NOT_IN_GAME: Игрок не в игре.
    """
    IN_GAME = auto()
    NOT_IN_GAME = auto()


class PersonNameStates(StatesGroup):
    """
    Группа состояний, связанных с именем персоны.

    Возможные состояния:
    - WAITING_FOR_ANSWER: Ожидание ответа пользователя.
    """
    WAITING_FOR_ANSWER = State()


async def start_bot() -> None:
    """
    Функция start_bot использутся для запуска бота.

    Для запуска бота используется :func:`another_module.another_function`.
    Используется в документе :doc: main.py
    """
    await dp.start_polling(bot)


async def _get_user_info(message: types.Message):
    """
    Получает информацию о пользователе из сообщения.

    :param message: Объект типа types.Message содержащий 
                    информацию о сообщении.
    :type message: types.Message
    :return: Кортеж с информацией о пользователе.
             Возвращаемые значения:
               - telegram_id (int): ID пользователя в Telegram.
               - username (str): Имя пользователя.
               - first_name (str): Имя пользователя.
               - if_bot (bool): Флаг, указывающий, 
                 является ли пользователь ботом.
    :rtype: tuple[int, srt, srt, bool]
    :raises: Нет исключений.

    Эта функция извлекает ID, имя, фамилию и флаг бота из объекта сообщения
    и возвращает их в виде кортежа.
    """
    user = message.from_user
    telegram_id = user.id
    first_name = user.first_name
    username = user.username
    if_bot = user.is_bot

    return telegram_id, username, first_name, if_bot


async def _delete_inline_keyboard(callback_query: types.CallbackQuery):
    """
    Удаляет inline клавиатуру из сообщения в ответ на callback_query.

    :param callback_query: Объект callback_query.
    :type callback_query: types.CallbackQuery
    :raises: aiogram.exceptions.AiogramError

    Описание:
    Эта функция удаляет inline клавиатуру из сообщения, на которое 
    пришел callback_query.
    Если возникает ошибка AiogramError при попытке изменения сообщения,
    она игнорируется.
    """
    try:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None
        )
    except aiogram.exceptions.AiogramError:
        pass
    

@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start для начала игры.

    :param message: Объект типа types.Message содержащий 
                    информацию о сообщении.
    :type message: types.Message
    :param state: Контекст состояния бота.
    :type state: FSMContext

    Описание:
    Функция обрабатывает команду /start для начала игры.
    Проверяет состояние пользователя и предоставляет возможность
    начать игру или продолжить.
    """
    telegram_id, username, first_name, is_bot = await _get_user_info(message)
    user_info.insert_field(telegram_id, username, first_name, is_bot)

    condition = users_in_game.get(telegram_id)
    if condition is not None or condition == UserGameState.IN_GAME:
        await message.answer(
            "/start, недоступно пока вы находитесь в игре"
        )
        return
    
    users_in_game[telegram_id] = UserGameState.NOT_IN_GAME

    progress_code = user_progress.get_plot_code(telegram_id)
    callback_data = "none progress" if progress_code == 1 else "continue"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="начать игру", 
                callback_data="start game",
                ),
            types.InlineKeyboardButton(
                text="продолжить",
                callback_data=callback_data
                ),
        ]
    ])
    
    await message.answer("Выберите действие:",reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == 'none progress')
async def process_new_game(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия кнопки 'none progress' в callback_query.

    :param callback_query: Объект типа types.CallbackQuery,
                           содержащий информацию о запросе.
    :type callback_query: types.CallbackQuery

    Описание:
    Функция обрабатывает нажатие кнопки 'none progress' в callback_query.
    Отправляет сообщение пользователю с возможностью 
    начать игру заново или вернуться в главное меню.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="да", 
                callback_data="start game",
                ),
            types.InlineKeyboardButton(
                text="вернуться в главное меню",
                callback_data="menu"
            )
        ]
    ])

    await bot.send_message(
        callback_query.from_user.id,
        "Сохранение не найдено, хотите ли вы начать сначала ?",
        reply_markup=keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == 'menu')
async def start_command(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия кнопки 'menu' в callback_query.

    :param callback_query: Объект типа types.CallbackQuery,
                           содержащий информацию о запросе.
    :type callback_query: types.CallbackQuery

    Описание:
    Функция обрабатывает нажатие кнопки 'menu' в callback_query.
    Отправляет сообщение пользователю с командой '/start'.
    """
    await callback_query.bot.send_message(
        callback_query.from_user.id,
        "/start")
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == 'start game')
async def process_start_game(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает запрос на начало игры.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий информацию о запросе.
    :type callback_query: types.CallbackQuery
    :param state: Контекст состояния бота.
    :type state: FSMContext

    Описание:
    Функция обрабатывает запрос на начало игры.
    Вставляет начальное значение прогресса для пользователя в базу данных.
    Отправляет сообщение с просьбой ввести Имя и Отчество главного героя.
    Удаляет инлайновую клавиатуру после нажатия кнопки 'start game'.
    Устанавливает состояние ожидания ответа для получения имени героя.
    """
    user_id = callback_query.from_user.id
    user_progress.insert_field(user_id, 1)
    await bot.send_message(
        user_id,
        "Введите Имя и Отчество главного героя:"
    )
    await _delete_inline_keyboard(callback_query)
    await state.set_state(state=PersonNameStates.WAITING_FOR_ANSWER)


@dp.message(PersonNameStates.WAITING_FOR_ANSWER)
async def process_user_answer(message: types.Message, state: FSMContext):
    """
    Обработчик нажатия кнопки 'start game' в callback_query.

    :param callback_query: Объект типа types.CallbackQuery,
                           содержащий информацию о запросе.
    :type callback_query: types.CallbackQuery
    :param state: Объект FSMContext, представляющий состояние ведения
                  переписки с пользователем.
    :type state: FSMContext

    Описание:
    Функция обрабатывает нажатие кнопки 'start game' в callback_query.
    Отправляет сообщение пользователю с запросом ввода Имени и Отчества
    главного героя.
    """
    user_input = message.text.strip()
    name_regex = r'^[A-Za-zА-Яа-я]{2,}\s+[A-Za-zА-Яа-я]{2,}$'
    
    if re.match(name_regex, user_input) and len(user_input.split()) <= 2:
        user_id = message.from_user.id
        formatted_name = ' '.join([part.capitalize() for part in user_input.split()])
        hero_name.insert_field(user_id, formatted_name)

        await message.answer(f"Имя и Отчество главного героя: {formatted_name}")
        await state.clear()
        await _key_continue(message)
    else:
        error_message = """
        Error.
        Пожалуйста, введите два слова (имя и фамилию),
        содержащие по крайней мере две буквы в каждом слове без цифр.
        """
        await message.answer(error_message)


async def _key_continue(message: types.Message):
    """
    Создает сообщение с встроенной клавиатурой для продолжения действия.

    :param message: Объект типа types.Message содержащий информацию о 
                    сообщении.
    :type message: types.Message
    :return: Ничего не возвращает.
    :rtype: None
    :raises: Нет исключений.

    Описание:
    Эта функция создает сообщение с встроенной клавиатурой, предлагающей 
    пользователю возможность продолжить действие, и отправляет это 
    сообщение в чат.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Продолжить", 
                callback_data="continue",
                ),
        ],
    ])

    await message.answer(
        "Нажмите чтобы продолжить:",
        reply_markup=keyboard,
    )


@dp.callback_query(lambda c: c.data == "continue")
async def process_continue(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Продолжить".

    :param callback_query: Объект типа types.CallbackQuery, 
                           содержащий информацию о нажатии на кнопку.
    :type callback_query: types.CallbackQuery
    :return: Ничего не возвращает.
    :rtype: None
    :raises: Нет исключений.

    Описание:
    Эта функция обрабатывает событие нажатия кнопки "Продолжить"
    в чате Telegram. Она обновляет информацию о текущем прогрессе
    игрока, создает новый экземпляр контроллера игры и помечает 
    пользователя как находящегося в игре.
    """
    user_id = callback_query.from_user.id
    users_story_id[user_id] = user_progress.get_plot_code(user_id)
    users_data[user_id] = Controller(
        hero_name.get_hero_name(user_id)
        )
    users_in_game[user_id] = UserGameState.IN_GAME
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "plot")
async def story_line(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие на inline-кнопку с callback_data == "plot".

    :param callback_query: Объект типа types.CallbackQuery содержащий
                           информацию о нажатии на кнопку.
    :type callback_query: types.CallbackQuery

    Описание:
    Функция обрабатывает действие, связанное с нажатием на inline-кнопку 
    с callback_data == "plot". Проверяет данные о пользователе и в зависимости 
    от этого отображает следующую локацию, обрабатывает разветвление сценария 
    и отправляет историю в игре. После выполнения действий удаляет 
    inline-клавиатуру.
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
        
    try:
        history = users_data[user_id].go_line_script(users_story_id[user_id])
        if history is None:
            await _send_next_location_message(user_id)
        elif _is_option_fork(history):
            await _handle_option_fork(callback_query)
        else:
            await _send_history_message(user_id, history)
        await _delete_inline_keyboard(callback_query)
    except Exception as error:
        await _game_over(callback_query, error)
        return


def _is_option_fork(history):
    """
    Проверяет, является ли история в игре разветвлением опций.

    :param history: Словарь с историей игры.
    :type history: dict
    :return: Результат проверки разветвления опций.
    :rtype: bool
    """
    return history.get("option_a") is None and history.get("option_b") is None


async def _handle_option_fork(callback_query):
    """
    Обрабатывает случай, когда в игре есть разветвление опций.

    :param callback_query: Объект типа types.CallbackQuery.
    :type callback_query: types.CallbackQuery
    """
    await option_a(callback_query)


async def _send_next_location_message(user_id):
    """
    Отправляет сообщение о следующей локации в игре.

    :param user_id: ID пользователя в Telegram.
    :type user_id: int
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="перейти в следующую лоакцию",
                callback_data="land"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="локация",
                callback_data="land"
            ),
            types.InlineKeyboardButton(
                text="предметы",
                callback_data="items"
            ),
            types.InlineKeyboardButton(
                text="Выход из игры",
                callback_data="exit"
            )
        ]
    ])
    await _send_game_status_message(user_id)
    await bot.send_message(
        user_id, "Перейдите в следующую локацию", reply_markup=keyboard)


async def _send_history_message(user_id, history):
    """
    Отправляет сообщение с историей и вариантами выбора.

    :param user_id: ID пользователя в Telegram.
    :type user_id: int
    :param history: Словарь с текстом и возможными вариантами истории.
                    Содержит ключи: "text", "option_a", "option_b".
    :type history: dict
    """
    keyboard = []
    row = []

    if history.get("option_a") is not None:
        row.append(types.InlineKeyboardButton(
            text=history["option_a"], callback_data="option_a"))
    if history.get("option_b") is not None:
        row.append(types.InlineKeyboardButton(
            text=history["option_b"], callback_data="option_b"))
    
    keyboard.append(row)
    keyboard.extend([
        [
            types.InlineKeyboardButton(text="локация", callback_data="land"),
            types.InlineKeyboardButton(text="предметы", callback_data="items"),
            types.InlineKeyboardButton(text="Выход из игры",
                                      callback_data="exit")
        ]
    ])

    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard) 
    await _send_game_status_message(user_id)
    await bot.send_message(
        user_id, 
        history["text"], 
        reply_markup=inline_keyboard)


async def _send_game_status_message(user_id):
    """
    Отправляет сообщение с текущим состоянием игры пользователю.

    :param user_id: Идентификатор пользователя в Telegram.
    :type user_id: int
    :raises: aiogram.exceptions.AiogramError

    Описание:
    Эта функция отправляет сообщение с текущим состоянием игры пользователю. 
    Получает информацию о здоровье врага, здоровье главного героя и опыте. 
    Отправляет два сообщения: одно с состоянием здоровья врага и другое 
    с состоянием главного героя (имя, здоровье, опыт).
    """
    enemy_health = users_data[user_id].get_health_enemy()
    hp_hero = users_data[user_id].get_health_protogonist()
    exp = users_data[user_id].get_exp_protogonist()

    await bot.send_message(user_id, f"Роман\n\tЗдоровье: {enemy_health}")
    await bot.send_message(
        user_id, 
        f"{hero_name.get_hero_name(user_id)}\n\tЗдоровье: {hp_hero} \n\tОпыт: {exp}")

    
@dp.callback_query(lambda c: c.data == "option_a")
async def option_a(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "option_a".

    :param callback_query: Объект типа types.CallbackQuery 
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    try:
        history = users_data[user_id].go_line_script(users_story_id[user_id])
    except Exception as error:
        await _game_over(callback_query, error)
        return
    users_story_id[user_id] = history["next_id_dial_a"]
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "option_b")
async def option_b(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "option_b".

    :param callback_query: Объект типа types.CallbackQuery 
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    try:
        history = users_data[user_id].go_line_script(users_story_id[user_id])
    except Exception as error:
        await _game_over(callback_query, error)
        return
    users_story_id[user_id] = history["next_id_dial_b"]
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "land")
async def location(callback_query: types.CallbackQuery):
    """
    Обработчик перехода в новую локацию.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return

    row = []
    keyboard = []
    history = users_data[user_id].go_line_script(users_story_id[user_id])
    
    if history is not None:
        row.append(types.InlineKeyboardButton(
            text="Недоступно. Прослушайте все диалоги",
            callback_data="plot"
        ))
    else:
        list_direction =  users_data[user_id].get_direction()

        for direction in list_direction:
            row.append(types.InlineKeyboardButton(
                text=direction,
                callback_data=direction
            ))
    
    keyboard.append(row)
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard) 
    await bot.send_message(
        user_id,
        f"Локация: {users_data[user_id].get_current_location()}"
    )
    await bot.send_message(
        user_id,
        f"{users_data[user_id].get_description_current_location()}",
        reply_markup=inline_keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == "direction")
async def process_choise_ditection(callback_query: types.CallbackQuery):
    """
    Обработчик выбора направления движения.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    direction = callback_query.data
    users_story_id[user_id] = users_data[user_id].go(direction)
    await story_line(callback_query)


@dp.callback_query(lambda c: c.data == "вперед")
async def process_choise_forward(callback_query: types.CallbackQuery):
    """
    Обработчик выбора движения вперед.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "назад")
async def process_choise_back(callback_query: types.CallbackQuery):
    """
    Обработчик выбора движения назад.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "налево")
async def process_choise_left(callback_query: types.CallbackQuery):
    """
    Обработчик выбора движения налево.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "направо")
async def process_choise_right(callback_query: types.CallbackQuery):
    """
    Обработчик выбора движения направо.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    await process_choise_ditection(callback_query)


@dp.callback_query(lambda c: c.data == "items")
async def process_items(callback_query: types.CallbackQuery):
    """
    Обработчик для вывода предметов пользователя.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    
    row = []
    keyboard = []
    # предмет всегда в 1м количестве
    item = users_data[user_id].get_attributes()
    
    if item is None:
        row.append(types.InlineKeyboardButton(
            text="Предметы не найдены, перейти к сюжету",
            callback_data="plot"
        ))
    else:
        row.append(types.InlineKeyboardButton(
            text=f"использовать предмет",
            callback_data="use_item"
        ))
        row.append(types.InlineKeyboardButton(
            text="Вернуться к сюжету",
            callback_data="plot"
        ))
        
    keyboard.append(row)
    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard) 
    await bot.send_message(
        callback_query.from_user.id,
        f"Предмет:{item}",
        reply_markup=inline_keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == "use_item")
async def process_use_item(callback_query: types.CallbackQuery):
    """
    Обработчик для использования предметов.

    :param callback_query: Объект типа types.CallbackQuery
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is None:
        await process_continue(callback_query)
        return
    await story_line(callback_query)


async def _game_over(callback_query: types.CallbackQuery, error):
    """
    Уведомляет пользователя о завершении игры из-за ошибки.

    :param callback_query: Объект типа types.CallbackQuery 
                           содержащий данные о запросе.
    :type callback_query: types.CallbackQuery
    :param error: Ошибка, приведшая к завершению игры.
    :type error: Exception
    """
    user_id = callback_query.from_user.id
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Выход из игры",
                callback_data="exit"
            )
        ]
    ]

    inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(
        user_id,
        str(error),
        reply_markup=inline_keyboard,
    )
    await _delete_inline_keyboard(callback_query)


@dp.callback_query(lambda c: c.data == "exit")
async def exit(callback_query: types.CallbackQuery):
    """
    Выход пользователя из игры.

    :param callback_query: Объект типа types.CallbackQuery,
                           содержащий данные запроса.
    :type callback_query: types.CallbackQuery
    """
    user_id = callback_query.from_user.id
    if users_data.get(user_id) is not None:
        user_progress.insert_field(user_id, users_story_id[user_id])

        del users_data[user_id]
        del users_story_id[user_id]
        del users_in_game[user_id]

    await callback_query.bot.send_message(
        callback_query.from_user.id,
        "/start")
    await _delete_inline_keyboard(callback_query)
