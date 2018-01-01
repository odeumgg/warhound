from collections import namedtuple

from . import matchmaking as mm, match as m, outcome as o, round as r

from .match import mk_empty_match
from .matchmaking import mk_empty_matchmaking
from .outcome import mk_empty_outcome


class Event(namedtuple('Event', ['cursor', 'e_type', 'data'])):
    __slots__ = ()


    def __new__(cls, cursor, e_type, data):
        return super(Event, cls).__new__(cls, cursor, e_type, data)


class Telemetry(namedtuple('Telemetry', ['matchmaking', 'match', 'outcome'])):
    __slots__ = ()


    def __new__(cls, _matchmaking, _match, _outcome):
        return super(Telemetry, cls).__new__(cls, _matchmaking, _match,
                                             _outcome)


def attempt(obj_event, dict_processor_by_event_type, dest,state):
    e_type = obj_event['type']

    if e_type in dict_processor_by_event_type:
        maybe_processor = dict_processor_by_event_type[e_type]
        event = Event(obj_event['cursor'], e_type, obj_event['dataObject'])
        maybe_processor(event, dest, state)

    return None


def test_round_finished(event):
    return event['type'] == 'Structures.RoundFinishedEvent'


def process(obj):
    list_round_finished_event = list(filter(test_round_finished, obj))

    _matchmaking = mk_empty_matchmaking()
    _match       = mk_empty_match(len(list_round_finished_event))
    _outcome     = mk_empty_outcome()

    state = { 'round': 0,
              'match_dict_team_id_by_player_id': _match.dict_team_id_by_player_id }

    for _evt in sorted(obj, key=lambda e: e['cursor']):
        attempt(_evt, mm.PROCESSOR_BY_EVENT_TYPE, _matchmaking, state)
        attempt(_evt,  m.PROCESSOR_BY_EVENT_TYPE,       _match, state)

        if _evt['type'] in r.PROCESSOR_BY_EVENT_TYPE:
            _round = _match.list_round[state['round']]
            attempt(_evt, r.PROCESSOR_BY_EVENT_TYPE, _round, state)

        attempt(_evt, o.PROCESSOR_BY_EVENT_TYPE, _outcome, state)

    return Telemetry(_matchmaking, _match, _outcome)

