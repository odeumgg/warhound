from .entity.matchmaking import mk_empty_matchmaking
from .entity.match import mk_empty_match
from .entity.outcome import mk_empty_outcome


class Telemetry:
    __slots__ = ('matchmaking', 'match', 'outcome')


    def __init__(self):
        self.matchmaking = mk_empty_matchmaking()
        self.match       = mk_empty_match()
        self.outcome     = mk_empty_outcome()


    def __iter__(self):
        return iter([self.matchmaking, self.match, self.outcome])


def mk_empty_telemetry():
    return Telemetry()

