

class Team:
    __slots__ = ('team_id', 'player_by_id')


    def __init__(self):
        self.team_id      = None
        self.player_by_id = {}


def mk_empty_team():
    return Team()

