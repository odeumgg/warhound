

class RoundOutcome:
    __slots__ = ('winning_team_ordinal', 'duration_sec', 'attrs',
                 'player_outcome_by_player_id', 'team_outcome_by_team_id',
                 'team_outcome_by_ordinal')


class Round:
    __slots__ = ('list_all_events', 'list_user_round_spells')


    def __init__(self):
        self.list_all_events        = []
        self.list_user_round_spells = []


def mk_empty_round():
    return Round()


def mk_empty_round_outcome():
    return RoundOutcome()

