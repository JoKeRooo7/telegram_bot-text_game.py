from .npc import NPC


class Enemy(NPC):
    def __init__(self, name: str) -> None:
        super().__init__( name)
        self._hp = 1

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = value

    def attack(self) -> None:
        pass

    def take_hit(self, damage: int) -> None:
        self._hp -= damage
        if self._hp <= 0:
            raise Exception(" Сожалеем, но ваш пациент не выжил. 💔😢\n\nКонец игры")
