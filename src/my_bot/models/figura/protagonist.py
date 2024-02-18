from collections import defaultdict

from .npc import NPC
from .enemy import Enemy
from .location import Direction
import sys
sys.path.append("..")
from ..command import CommandDAO

class Protagonist:
    def __init__(self, name: str) -> None:
        self._command_db = CommandDAO()
        self._name = name
        self._hp = 10
        self._xp = 7
        self._inventory = defaultdict(int)
        self._curr_location = 1
        self._line_id = 1

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = value

    @property
    def xp(self) -> int:
        return self._xp

    @xp.setter
    def xp(self, value: int) -> None:
        self._xp = value

    @property
    def inventory(self) -> defaultdict:
        return self._inventory

    @property
    def curr_location(self) -> int:
        return self._curr_location
    
    @curr_location.setter
    def curr_location(self, value: int) -> None:
        self._curr_location = value
        
    @property
    def line_id(self) -> int:
        return self._line_id
    
    @line_id.setter
    def line_id(self, value: int) -> None:
        self._line_id = value

    def go(self, direction: Direction) -> None:
        self.curr_location = self._command_db.get_next_location_id(direction, self.curr_location)
        self.line_id = self._command_db.get_start_dialog_location(self.curr_location)
        if (self.line_id == 51 and self.hp < 10 and self.xp < 5):
            self.line_id = 29            
        return self.line_id

    def whereami(self) -> None:
        return self._curr_location

    def talk_to(self, npc: NPC) -> None:
        """Разговаривает с NPC"""
        pass

    # from subject
    def attack(self, enemy: Enemy) -> None:
        pass

    def advance_xp(self, value: int = 1) -> None:
        self.xp += value

    def heal(self, value: int = 1) -> None:
        self.hp += value

    def take_hit(self, damage: int = 1) -> None:
        self.hp -= damage
        if self.hp <= 0:
            raise Exception("Сожалеем, но вы умерли. 💔\n\nКонец игры")

    def take(self, item: str) -> None:
        self.inventory[item] += 1

    def give(self, npc: NPC, item: str) -> None:
        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]
        npc.receive(item)

    def show_inventory(self):
        keys_list = list(self.inventory.keys())
        return keys_list if keys_list else []
    
    def use_attributes(self):
        self.heal(2)
        self.advance_xp(2)
        self.inventory[0] -= 1
        if self.inventory[0] == 0:
            del self.inventory[0]