from collections import defaultdict, namedtuple

from .processing.match_beginning import *
from .processing.match_end import *
from .processing.match_round import *
from .processing.matchmaking import *
from .processing.progression import *
from .telemetry import mk_empty_telemetry


class Event(namedtuple('Event', ['cursor', 'e_type', 'data'])):
    __slots__ = ()

    def __new__(cls, cursor, e_type, data):
        return super(Event, cls).__new__(cls, cursor, e_type, data)


PROCESSOR_BY_EVENT_TYPE = \
    {
        'com.stunlock.service.matchmaking.avro.QueueEvent':
            process_queue_event,
        'Structures.MatchStart': process_match_start,
        'Structures.MatchReservedUser': process_match_reserved_user,
        'Structures.BattleritePickEvent': process_battlerite_pick_event,
        'Structures.RoundEvent': process_round_event,
        'Structures.DeathEvent': process_death_event,
        'Structures.RoundFinishedEvent': process_round_finished_event,
        'Structures.MatchFinishedEvent': process_match_finished_event,
        'Structures.UserRoundSpell': process_user_round_spell,
        'com.stunlock.battlerite.team.TeamUpdateEvent':
            process_team_update_event,
        'Structures.ServerShutdown': process_server_shutdown
    }


def attempt_process_event(obj_event, dict_processor_by_event_type, telemetry,
                          state):
    e_type                      = obj_event['type']
    maybe_processor             = dict_processor_by_event_type[e_type]
    matchmaking, match, outcome = telemetry

    if maybe_processor:
        event = Event(obj_event['cursor'], e_type, obj_event['dataObject'])
        maybe_processor(event, telemetry, state)
    else:
        print('encountered unknown event: {0}'.format(e_type))

    return None


def process(obj):
    ordered_by_cursor = sorted(obj, key=lambda e: e['cursor'])
    telemetry         = mk_empty_telemetry()
    state             = { round: 0 }

    for obj_event in ordered_by_cursor:
        attempt_process_event(obj_event, PROCESSOR_BY_EVENT_TYPE, telemetry,
                              state)

    return telemetry

