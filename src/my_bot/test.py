from controller import Controller



def story_line(line_id, contr):
    print("LINE ID", line_id)
    data = contr.go_line_script(line_id)
    print("-------------------------------------")
    print("HEALTH PROTOGONIST", contr.get_health_protogonist())
    print("HEALTH ENEMY", contr.get_health_enemy())
    print("EXP PROTOGONIST", contr.get_exp_protogonist())
    print("LOCATION", contr.get_current_location())
    print("DIRECTION", contr.get_direction())
    print("DESCRIPTION", contr.get_description_current_location())
    print("ATTRIBUTES", contr.get_attributes())
    print("-------------------------------------")
    
    print(data['text'])
    if data['option_a'] or data['option_b']:
        if data['option_a']:
            print("ВЫБОР 1", data['option_a'])
        if data['option_b']:
            print("ВЫБОР 2", data['option_b'])
    else:
        if data['next_id_dial_a']:
            story_line(data['next_id_dial_a'], contr)
        else:
            print("перейти к следующей локации")

        
    a = input()
    if a == "1":
        story_line(data['next_id_dial_a'], contr)
    if a == "2":
        story_line(data['next_id_dial_b'], contr)
    direction = a
    if direction in contr.get_direction():
        if contr.can_move_next_location(direction):
            story_line(contr.go(direction), contr)
        else:
            print("Вы не можете покинуть данную локацию, пока не выполните все квесты")
            story_line(line_id, contr)
        
        

if __name__ == "__main__":
    line_id = 1
    contr = Controller("DFQ FGH")
    story_line(line_id, contr)