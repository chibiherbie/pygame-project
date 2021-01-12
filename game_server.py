from hero import Hero
from random import choice


class Game:
    def __init__(self, id):
        self.id = id
        self.players = [Hero('data/image/hero1', 0, 0),
                   Hero('data/image/hero2', 0, 0)]

        self.p_ypd = [(0, 0, 0), (0, 0, 0)]
        self.code = ''.join([choice('qwertasdyhjozovbu') for i in range(4)])
        self.count_player = 0
        print('КОД ЛОББИ:', self.code)
