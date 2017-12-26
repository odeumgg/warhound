from collections import namedtuple, OrderedDict


class PlayerRoundOutcome:
    __slots__ = ('player_id', 'team_id', 'round', 'won', 'stats')


    def __init__(self):
        self.player_id = None
        self.team_id   = None
        self.round     = None
        self.won       = None
        self.stats     = None


class PlayerMatchOutcome:
    __slots__ = ('match_id', 'attrs')


    def __init__(self):
        pass


class Player:
    __slots__ = ('player_id', 'champion_id', 'team_id', 'attrs',
                 'battlerite_by_id', 'round_outcome_by_ordinal',
                 'list_gameplay_by_ordinal',
                 'list_user_round_spells_by_ordinal')


    def __init__(self):
        self.player_id                         = None
        self.champion_id                       = None
        self.team_id                           = None
        self.battlerite_by_id                  = {}
        self.round_outcome_by_ordinal          = OrderedDict()
        self.list_gameplay_by_ordinal          = OrderedDict()
        self.list_user_round_spells_by_ordinal = OrderedDict()


def mk_empty_player_round_outcome():
    return PlayerRoundOutcome()


def mk_empty_player_match_outcome():
    return PlayerMatchOutcome()


def mk_empty_player():
    return Player()

