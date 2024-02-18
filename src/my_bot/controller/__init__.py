from models import Facade
import sys
sys.path.append("..")

DATABASE = ".database/game.db"


class Controller:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Создает и возвращает экземпляр класса Controller. Если экземпляр уже существует,
        возвращает существующий экземпляр.

        Args:
            cls: Класс Controller.
            args: Позиционные аргументы.
            kwargs: Именованные аргументы.

        Returns:
            Экземпляр класса Controller.
        """
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, user_name):
        """
        Инициализирует экземпляр класса Controller.

        Args:
            user_name: Имя пользователя(его Имя и Отчество).

        Returns:
            None.
        """
        self._initialized = False
        self.facade = Facade(user_name)

    def get_direction(self):
        """
        Возвращает направления (direction) из текущей локации.

        Args:
            None.

        Returns:
            Список текущих направлений (direction).
        """
        return self.facade.direction

    def get_current_location(self):
        """
        Возвращает имя текущей локации.

        Args:
            None.

        Returns:
            Имя текущей локации.
        """
        return self.facade.name_location

    def get_description_current_location(self):
        """
        Возвращает описание текущей локации.

        Args:
            None.

        Returns:
            Описание текущей локации.
        """
        return self.facade.description_location

    def go_line_script(self, line_id):
        """
        Переходит на следующую линию сценария (story_line).

        Args:
            line_id (int): Идентификатор линии сценария.

        Returns:
            dict or None: Возвращает словарь, если линия сценария продолжается, или None, если конец диалогов в данной локации.
        """
        return self.facade.story_line(line_id)

    def get_health_protogonist(self):
        """
        Показывает текущее количество здоровья протагониста.

        Returns:
            int: Количество здоровья протагониста.
        """
        return self.facade.protagonist.hp

    def get_exp_protogonist(self):
        """
        Показывает текущий опыт протагониста.

        Returns:
            int: Опыт протагониста.
        """
        return self.facade.protagonist.xp

    def get_health_enemy(self):
        """
        Показывает текущее количество здоровья врага.

        Returns:
            int: Количество здоровья врага.
        """
        return self.facade.enemy.hp

    def get_attributes(self):
        """
        Возращает список атрибутов игрока

        Args:
            None.

        Returns:
           Список атрибутов игрока
        """
        if self.facade.protagonist.show_inventory():
            return self.facade.protagonist.show_inventory()[0]
        return None

    def can_move_next_location(self, direction):
        """
        Проверяет может ли игрок перейти на следующую локацию.

        Args:
            direction: Направление движения.

        Returns:
           True - если может перейти, False - переход запрещен
        """
        return self.facade.check_move_next_location()

    def go(self, direction):
        """
        Осуществляет передвижение главного героя в указанном направлении.

        Args:
            direction: Направление движения.

        Returns:
            Результат словарь как в функции go_line_script
        """
        return self.facade.protagonist.go(direction)
