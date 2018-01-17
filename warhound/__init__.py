from collections import namedtuple

from . import matchmaking as mm, match as m, outcome as o, match_round as r

from .match import mk_match
from .matchmaking import mk_matchmaking
from .outcome import mk_outcome


class Telemetry(namedtuple('Telemetry', ['matchmaking', 'match', 'outcome'])):
    __slots__ = ()


    def __new__(cls, matchmaking, match, outcome):
        return super(Telemetry, cls).__new__(cls, matchmaking, match, outcome)


def mk_telemetry(matchmaking, match, outcome):
    return Telemetry(matchmaking, match, outcome)


class NullUnknownProcessor:
    def __call__(self, target, data_object, state):
        pass


def mk_null_unknown_processor():
    return NullUnknownProcessor()


def maybe_proc_matchmaking(kind):
    return mm.PROCESSOR_BY_EVENT_TYPE.get(kind, None)


def maybe_proc_match(kind):
    return m.PROCESSOR_BY_EVENT_TYPE.get(kind, None)


def maybe_proc_round(kind):
    return r.PROCESSOR_BY_EVENT_TYPE.get(kind, None)


def maybe_proc_outcome(kind):
    return o.PROCESSOR_BY_EVENT_TYPE.get(kind, None)


def test_round_finished(obj):
    return obj['type'] == 'Structures.RoundFinishedEvent'


def process_single(list_pairs, data_object, state):
    for (target, proc) in list_pairs:
        proc(target, data_object, state)

    return None


def process(obj, maybe_proc_unknown=None):
    proc_unknown = maybe_proc_unknown or mk_null_unknown_processor()
    num_rounds   = len(list(filter(test_round_finished, obj)))

    matchmaking, match, outcome = \
        mk_matchmaking(), mk_match(num_rounds), mk_outcome(num_rounds)

    state = { 'round': 0, 'dict_team_id_by_player_id': {},
              'dict_side_by_player_id': {} }

    for obj_event in sorted(obj, key=lambda e: e['cursor']):
        kind        = obj_event['type']
        data_object = obj_event['dataObject']

        proc_matchmaking = maybe_proc_matchmaking(kind) or proc_unknown
        proc_match       =       maybe_proc_match(kind) or proc_unknown
        proc_round       =       maybe_proc_round(kind) or proc_unknown
        proc_outcome     =     maybe_proc_outcome(kind) or proc_unknown

        _round = match.list_round[data_object.get('round', state['round'])]

        list_pairs = [ (matchmaking, proc_matchmaking), (match, proc_match),
                       (_round, proc_round), (outcome, proc_outcome) ]

        process_single(list_pairs, data_object, state)

    return mk_telemetry(matchmaking, match, outcome)

