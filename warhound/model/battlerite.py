

class Battlerite:
    __slots__ = ('battlerite_id', 'player_id', 'champion_id', 'attrs')


    def __init__(self):
        self.battlerite_id = None
        self.player_id     = None
        self.champion_id   = None
        self.attrs         = None


def mk_empty_battlerite():
    return Battlerite()
