from collections import defaultdict, OrderedDict

from .round import mk_empty_round


class MatchOutcome:
    __slots__ = ('duration_sec', 'score_by_ordinal', 'attrs')


    def __init__(self):
        self.duration_sec     = None
        self.score_by_ordinal = OrderedDict()
        self.attrs            = None


class Match:
    __slots__ = ('match_id', 'attrs', 'team_by_id', 'player_by_id',
                 'team_by_id_by_ordinal', 'round_by_ordinal',
                 'server_shutdown', 'outcome')


    def __init__(self):
        self.match_id              = None
        self.attrs                 = None
        self.team_by_id            = {}
        self.player_by_id          = {}
        self.team_by_id_by_ordinal = defaultdict(dict)
        self.round_by_ordinal      = defaultdict(mk_empty_round)
        self.server_shutdown       = None
        self.outcome               = None


def mk_empty_match_outcome():
    return MatchOutcome()


def mk_empty_match():
    return Match()
