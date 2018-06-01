from collections import namedtuple
import enum

# The telemetry file format is simple: it is a json file-formatted list of
# events. Here is what an example event from this list looks like:
#
# {
# 	"cursor": 4238368588,
# 	"type": "Structures.RoundEvent",
# 	"dataObject": {
# 		"time": 1525061143435,
# 		"matchID": "28EDDA92368A44CFBE298D614CAC3450",
# 		"externalMatchID": "",
# 		"userID": "956766417846468608",
# 		"round": 1,
# 		"character": 1318732017,
# 		"type": "ENERGY_ABILITY_USED",
# 		"value": 1264792448,
# 		"timeIntoRound": 0
# 	}
# }
#
# Events ordered by 'cursor' value are chronological. They are merely a stream--
# we have to deduce certain boundaries like "when round 2 started" by
# inference. (In this case, we must look for the first event with type
# "Structures.RoundFinished" and pay attention to what follows until the next).
#
# This module pigeonholes events into one of the following categories:
#
# - Match
# - Round
# - Spell summary
#
# This pigeonholing is not clean--some things which SLS regards as "match"
# events make more sense for our purposes as Round events, for example. Keep
# in mind that warhound has its own take on which category each event is.
#
# Match events are top-level "meta" events describing when the match was queued
# for, when it began, when the match (first round) starts, how each team
# performed at the end, etc.
#
# Round events describe something that happened in a particular round, like the
# pickup of a health shard, or the use of an EX ability.
#
# Spell summary events provide an *overview* of a hero's performance through
# information about each spell. This is still a bit TBD as we figure out the
# resolution of each event. Whereas there are many round events for one round,
# there are many spell summary events for each round, each apparently providing
# information about one spell for one hero.


EVT_ONLY_CLASS = 0xf0000000
EVT_ONLY_TYPE = 0x0fffffff

EVT_MASK_MATCH = 0x80000000
EVT_MASK_ROUND = 0x40000000
EVT_MASK_SPELLSUMMARY = 0x20000000


class EventType(enum.IntEnum):
    # Match events, which pertain to the entire game:
    MATCH_UNKNOWN = 0x8fffffff 
    MATCH_BATTLERITEPICK = 0x80000001
    MATCH_FINISHED = 0x80000002
    MATCH_QUEUE = 0x80000004
    MATCH_RESERVEDUSER = 0x80000008
    MATCH_SERVERSHUTDOWN = 0x80000020
    MATCH_START = 0x80000040
    MATCH_TEAMUPDATE = 0x80000080

    # Round events, which pertain to things within a round:
    ROUND_UNKNOWN = 0x4FFFFFFF
    ROUND_ALLYDEATHENERGYPICKUP = 0x40000001
    ROUND_DEATH = 0x40000002
    ROUND_ENERGYABILITYUSED = 0x40000004
    ROUND_ENERGYSHARDPICKUP = 0x40000008
    ROUND_FINISHED = 0x80000010
    ROUND_HEALTHSHARDPICKUP = 0x40000020
    ROUND_MOUNTDURATION = 0x40000040
    ROUND_RUNELASTHIT = 0x40000080
    ROUND_ULTIMATEUSED = 0x40000100

    # Per-round user spell summary:
    SPELLSUMMARY_UNKNOWN = 0x2FFFFFFF
    SPELLSUMMARY_CONTROLDONE = 0x20000001
    SPELLSUMMARY_CONTROLRECEIVED = 0x20000002
    SPELLSUMMARY_DAMAGEDONE = 0x20000004
    SPELLSUMMARY_DAMAGERECEIVED = 0x20000008
    SPELLSUMMARY_ENERGYRECEIVED = 0x20000010
    SPELLSUMMARY_ENERGYUSED = 0x20000020
    SPELLSUMMARY_HEALINGDONE = 0x20000040
    SPELLSUMMARY_HEALINGRECEIVED = 0x20000080
    SPELLSUMMARY_USES = 0x20000100


DICT_MATCH_EVENT_BY_DESCRIPTOR = {
    'Structures.BattleritePickEvent': EventType.MATCH_BATTLERITEPICK,
    'Structures.MatchFinishedEvent': EventType.MATCH_FINISHED,
    'com.stunlock.service.matchmaking.avro.QueueEvent': EventType.MATCH_QUEUE,
    'Structures.MatchReservedUser': EventType.MATCH_RESERVEDUSER,
    'Structures.ServerShutdown': EventType.MATCH_SERVERSHUTDOWN,
    'Structures.MatchStart': EventType.MATCH_START,
    'com.stunlock.battlerite.team.TeamUpdateEvent': EventType.MATCH_TEAMUPDATE,
}


DICT_ROUND_EVENT_BY_DESCRIPTOR = {
    ('Structures.RoundEvent', 'ALLY_DEATH_ENERGY_PICKUP'):
        EventType.ROUND_ALLYDEATHENERGYPICKUP,
    ('Structures.DeathEvent', None): EventType.ROUND_DEATH,
    ('Structures.RoundEvent', 'ENERGY_ABILITY_USED'):
        EventType.ROUND_ENERGYABILITYUSED,
    ('Structures.RoundEvent', 'ENERGY_SHARD_PICKUP'):
        EventType.ROUND_ENERGYSHARDPICKUP,
    ('Structures.RoundFinishedEvent', None): EventType.ROUND_FINISHED,
    ('Structures.RoundEvent', 'HEALTH_SHARD_PICKUP'):
        EventType.ROUND_HEALTHSHARDPICKUP,
    ('Structures.RoundEvent', 'MOUNT_DURATION'): EventType.ROUND_MOUNTDURATION,
    ('Structures.RoundEvent', 'RUNE_LASTHIT'): EventType.ROUND_RUNELASTHIT,
    ('Structures.RoundEvent', 'ULTIMATE_USED'): EventType.ROUND_ULTIMATEUSED,
}


DICT_SPELLSUMMARY_EVENT_BY_DESCRIPTOR = {
    'CONTROL_DONE': EventType.SPELLSUMMARY_CONTROLDONE,
    'CONTROL_RECEIVED': EventType.SPELLSUMMARY_CONTROLRECEIVED,
    'DAMAGE_DONE': EventType.SPELLSUMMARY_DAMAGEDONE,
    'DAMAGE_RECEIVED': EventType.SPELLSUMMARY_DAMAGERECEIVED,
    'ENERGY_RECEIVED': EventType.SPELLSUMMARY_ENERGYRECEIVED,
    'ENERGY_USED': EventType.SPELLSUMMARY_ENERGYUSED,
    'HEALING_DONE': EventType.SPELLSUMMARY_HEALINGDONE,
    'HEALING_RECEIVED': EventType.SPELLSUMMARY_HEALINGRECEIVED,
    'USES': EventType.SPELLSUMMARY_USES,
}


def infer_maybe_spellsummary_event_type(evt_json):
    """Return either spell summary event or None."""

    if evt_json['type'] == 'Structures.UserRoundSpell':
        descriptor = evt_json['dataObject']['scoreType']

        try:
            return DICT_SPELLSUMMARY_EVENT_BY_DESCRIPTOR[descriptor]
        except KeyError:
            return Event.SPELLSUMMARY_UNKNOWN
    else:
        return None


def infer_maybe_round_event_type(evt_json):
    """Return either round event or None."""

    evt_type = evt_json['type']

    if evt_type in ('Structures.DeathEvent', 'Structures.RoundFinishedEvent'):
        evt_subtype = None
    else:
        try:
            evt_subtype = evt_json['dataObject']['type']
        except KeyError:
            return None

    try:
        return DICT_ROUND_EVENT_BY_DESCRIPTOR[(evt_type, evt_subtype)]
    except KeyError:
        if evt_type == 'Structures.RoundEvent':
            return Event.ROUND_UNKNOWN
        else:
            return None


def infer_maybe_match_event_type(evt_json):
    """Return either Match event or None."""

    try:
        return DICT_MATCH_EVENT_BY_DESCRIPTOR[evt_json['type']]
    except KeyError:
        return Event.MATCH_UNKNOWN


def infer_event_type(evt_json):
    """Given raw input from telemetry, return discrete type or None."""
    
    # infer_maybe_match_event defaults to "unknown match event."
    # In other words, at least one heuristic will return something.
    list_heuristic = [
        lambda evt_json: infer_maybe_spellsummary_event_type(evt_json),
        lambda evt_json: infer_maybe_round_event_type(evt_json),
        lambda evt_json: infer_maybe_match_event_type(evt_json)
    ]

    for heuristic in list_heuristic:
        result = heuristic(evt_json)
        if result:
            return result
    else:
        raise RuntimeError('insanity') # See comments above.


class Event(namedtuple('Event', ['evt_type', 'evt_json'])):
    def __new__(cls, evt_type, evt_json):
        return super().__new__(cls, evt_type, evt_json)


def mk(*args, **kwargs):
    return Event(*args, **kwargs)


def from_json(evt_json):
    return mk(infer_event_type(evt_json), evt_json)

