

# Таблица состояний
# | stop: true | attack: false | defence: false | UNIT_STATUS_STOP: 1
# | stop: false | attack: false | defence: false | UNIT_STATUS_MARCH: 2
# | stop: true | attack: true | defence: false | UNIT_STATUS_ATTACK: 3
# | stop: true | attack: false | defence: true | UNIT_STATUS_DEFENCE: 4
# | stop: true | attack: true | defence: true | UNIT_STATUS_ATTACK_DEFENCE: 5
# | stop: false | attack: true | defence: false | UNIT_STATUS_RETREAT: 6
class UnitState:
    stop: bool = False
    attack: bool = False
    defence: bool = False

    def __init__(self, stop: bool = False, attack: bool = False, defence: bool = False):
        self.stop = stop
        self.attack = attack
        self.defence = defence

