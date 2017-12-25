from collections import namedtuple, OrderedDict


class RoundPerformance:
    __slots__ = ('round', 'attrs')


    def __init__(self):
        pass


class MatchPerformance:
    __slots__ = ('match_id', 'attrs')


    def __init__(self):
        pass


class Player:
    __slots__ = ('player_id', 'champion_id', 'team_id', 'attrs',
                 'battlerite_by_id', 'round_performance_by_ordinal',
                 'list_all_events_by_ordinal',
                 'list_user_round_spells_by_ordinal')


    def __init__(self):
        self.player_id                         = None
        self.champion_id                       = None
        self.team_id                           = None
        self.battlerite_by_id                  = {}
        self.round_performance_by_ordinal      = OrderedDict()
        self.list_all_events_by_ordinal        = OrderedDict()
        self.list_user_round_spells_by_ordinal = OrderedDict()


def mk_empty_player():
    return Player()

