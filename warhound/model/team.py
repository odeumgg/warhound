

class TeamRoundOutcome:
    __slots__ = ()


    def __init__(self):
        pass


class TeamMatchOutcome():
    __slots__ = ()


    def __init__(self):
        pass


class Team:
    __slots__ = ('team_id', 'player_by_id')


    def __init__(self):
        self.team_id      = None
        self.player_by_id = {}


def mk_empty_team_round_outcome():
    return TeamRoundOutcome()


def mk_empty_team_match_outcome():
    return TeamMatchOutcome()


def mk_empty_team():
    return Team()

