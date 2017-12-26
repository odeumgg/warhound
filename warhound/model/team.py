from collections import OrderedDict


class TeamRoundOutcome:
    __slots__ = ('team_id', 'round', 'won', 'stats_by_player_id')


    def __init__(self):
        self.team_id            = None
        self.round              = None
        self.won                = None
        self.stats_by_player_id = {}


class TeamMatchOutcome():
    __slots__ = ()


    def __init__(self):
        pass


class Team:
    __slots__ = ('team_id', 'player_by_id', 'round_outcome_by_ordinal')


    def __init__(self):
        self.team_id                  = None
        self.player_by_id             = {}
        self.round_outcome_by_ordinal = OrderedDict()


def mk_empty_team_round_outcome():
    return TeamRoundOutcome()


def mk_empty_team_match_outcome():
    return TeamMatchOutcome()


def mk_empty_team():
    return Team()

