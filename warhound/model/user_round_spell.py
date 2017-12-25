

class UserRoundSpell:
    __slots__ = ('player_id', 'champion_id', 'attrs')


    def __init__(self):
        self.player_id   = None
        self.champion_id = None
        self.attrs       = None


def mk_empty_user_round_spell():
    return UserRoundSpell()

