from .figura import Protagonist, Enemy, NPC
from .command import CommandDAO

class Facade:
    def __init__(self, user_name: str):
        self.protagonist = Protagonist(user_name)
        self.enemy = Enemy(user_name)
        self.command_dao = CommandDAO()
        
    @property
    def location_id(self):
        return self.protagonist.curr_location

    @property
    def direction(self):
        data = self.command_dao.get_direction(self.location_id)
        return [item[0] for item in data] if data else []
        
    @property
    def name_location(self):
        return self.command_dao.get_name_location(self.location_id)
    
    @property
    def description_location(self):
        return self.command_dao.get_description_location(self.location_id)

    def story_line(self, line_id):
        if (line_id == 51 and (self.protagonist.hp < 10 or self.protagonist.xp < 5)):
            line_id = 29 
        data = self.command_dao.get_story_line(line_id)
        if line_id != self.protagonist.line_id:
            self.change_healith(line_id)
        self.protagonist.line_id = line_id
        if (data):
            data['text'] = data['text'].replace("{name_surname}", self.protagonist.name)
        if (line_id in (25,27,29)):
            self.protagonist.curr_location = 9
        if (line_id == 20):
            self.protagonist.take("Укол")
        return data


    def change_healith(self,line_id):
        res = self.command_dao.change_healith(line_id)
        if res:
            self.protagonist.take_hit(-res.health)
            self.protagonist.advance_xp(res.experience)
            self.enemy.take_hit(-res.health_enemy)
        elif (line_id == 59):
            health_enemy = self.enemy.hp
            self.enemy.take_hit(health_enemy)
            
            
    def check_move_next_location(self):
        max_line_id = self.command_dao.get_max_line_id_location(self.location_id)
        return max_line_id >= self.location_id
    
    

