from collections import namedtuple

from . import matchmaking as mm, match as m, outcome as o, round as r

from .match import mk_empty_match
from .matchmaking import mk_empty_matchmaking
from .outcome import mk_empty_outcome


class Telemetry(namedtuple('Telemetry', ['matchmaking', 'match', 'outcome'])):
    __slots__ = ()


    def __new__(cls, matchmaking, match, outcome):
        return super(Telemetry, cls).__new__(cls, matchmaking, match, outcome)


def attempt(obj_event, dict_processor_by_event_type, dest,state):
    e_type = obj_event['type']

    if e_type in dict_processor_by_event_type:
        maybe_processor = dict_processor_by_event_type[e_type]
        maybe_processor(dest, obj_event['dataObject'], state)

    return None


def test_round_finished(event):
    return event['type'] == 'Structures.RoundFinishedEvent'


def process(obj):
    list_round_finished_event = list(filter(test_round_finished, obj))

    matchmaking = mk_empty_matchmaking()
    match       = mk_empty_match(len(list_round_finished_event))
    outcome     = mk_empty_outcome(len(list_round_finished_event))

    state = { 'round': 0, 'dict_team_id_by_player_id': {},
              'dict_side_by_player_id': {} }

    for event in sorted(obj, key=lambda e: e['cursor']):
        attempt(event, mm.PROCESSOR_BY_EVENT_TYPE, matchmaking, state)
        attempt(event,  m.PROCESSOR_BY_EVENT_TYPE,       match, state)

        if event['type'] in r.PROCESSOR_BY_EVENT_TYPE:
            if 'round' in event['dataObject']:
                _round = match.list_round[event['dataObject']['round']]
            else:
                _round = match.list_round[state['round']]

            attempt(event, r.PROCESSOR_BY_EVENT_TYPE, _round, state)

        attempt(event, o.PROCESSOR_BY_EVENT_TYPE, outcome, state)

    return Telemetry(matchmaking, match, outcome)

