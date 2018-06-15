from collections import namedtuple
import enum


# The telemetry file format is simple: it is a source_json file-formatted list
# of events. Here is what an example event from this list looks like:
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
# inference. (In this case, we must look for the first event with kind
# "Structures.RoundFinished" and pay attention to what follows until the next).


class Mask(enum.IntEnum):
    MATCH = 0x80000000
    ROUND = 0x40000000
    SPELLSUMMARY = 0x20000000


class Kind(enum.IntEnum):
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
    ROUND_FINISHED = 0x40000010
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
    'Structures.BattleritePickEvent': Kind.MATCH_BATTLERITEPICK,
    'Structures.MatchFinishedEvent': Kind.MATCH_FINISHED,
    'com.stunlock.service.matchmaking.avro.QueueEvent': Kind.MATCH_QUEUE,
    'Structures.MatchReservedUser': Kind.MATCH_RESERVEDUSER,
    'Structures.ServerShutdown': Kind.MATCH_SERVERSHUTDOWN,
    'Structures.MatchStart': Kind.MATCH_START,
    'com.stunlock.battlerite.team.TeamUpdateEvent': Kind.MATCH_TEAMUPDATE,
}


DICT_ROUND_EVENT_BY_DESCRIPTOR = {
    ('Structures.RoundEvent', 'ALLY_DEATH_ENERGY_PICKUP'):
        Kind.ROUND_ALLYDEATHENERGYPICKUP,
    ('Structures.DeathEvent', None): Kind.ROUND_DEATH,
    ('Structures.RoundEvent', 'ENERGY_ABILITY_USED'):
        Kind.ROUND_ENERGYABILITYUSED,
    ('Structures.RoundEvent', 'ENERGY_SHARD_PICKUP'):
        Kind.ROUND_ENERGYSHARDPICKUP,
    ('Structures.RoundFinishedEvent', None): Kind.ROUND_FINISHED,
    ('Structures.RoundEvent', 'HEALTH_SHARD_PICKUP'):
        Kind.ROUND_HEALTHSHARDPICKUP,
    ('Structures.RoundEvent', 'MOUNT_DURATION'): Kind.ROUND_MOUNTDURATION,
    ('Structures.RoundEvent', 'RUNE_LASTHIT'): Kind.ROUND_RUNELASTHIT,
    ('Structures.RoundEvent', 'ULTIMATE_USED'): Kind.ROUND_ULTIMATEUSED,
}


DICT_SPELLSUMMARY_EVENT_BY_DESCRIPTOR = {
    'CONTROL_DONE': Kind.SPELLSUMMARY_CONTROLDONE,
    'CONTROL_RECEIVED': Kind.SPELLSUMMARY_CONTROLRECEIVED,
    'DAMAGE_DONE': Kind.SPELLSUMMARY_DAMAGEDONE,
    'DAMAGE_RECEIVED': Kind.SPELLSUMMARY_DAMAGERECEIVED,
    'ENERGY_RECEIVED': Kind.SPELLSUMMARY_ENERGYRECEIVED,
    'ENERGY_USED': Kind.SPELLSUMMARY_ENERGYUSED,
    'HEALING_DONE': Kind.SPELLSUMMARY_HEALINGDONE,
    'HEALING_RECEIVED': Kind.SPELLSUMMARY_HEALINGRECEIVED,
    'USES': Kind.SPELLSUMMARY_USES,
}


def infer_maybe_spellsummary_kind(source_json):
    """Return either spell summary kind or None."""

    if source_json['type'] == 'Structures.UserRoundSpell':
        descriptor = source_json['dataObject']['scoreType']

        try:
            return DICT_SPELLSUMMARY_EVENT_BY_DESCRIPTOR[descriptor]
        except KeyError:
            return Kind.SPELLSUMMARY_UNKNOWN
    else:
        return None


def infer_maybe_round_kind(source_json):
    """Return either round kind or None."""

    kind = source_json['type']

    if kind in ('Structures.DeathEvent', 'Structures.RoundFinishedEvent'):
        subkind = None
    else:
        try:
            subkind = source_json['dataObject']['type']
        except KeyError:
            return None

    try:
        return DICT_ROUND_EVENT_BY_DESCRIPTOR[(kind, subkind)]
    except KeyError:
        if kind == 'Structures.RoundEvent':
            return Kind.ROUND_UNKNOWN
        else:
            return None


def infer_maybe_match_kind(source_json):
    """Return either Match kind or None."""

    try:
        return DICT_MATCH_EVENT_BY_DESCRIPTOR[source_json['type']]
    except KeyError:
        return Kind.MATCH_UNKNOWN


def infer_kind(source_json):
    """
    Pigeonholes events into a specific type in one of the following groups:

    - Match
    - Round
    - Spell summary

    This pigeonholing is not clean--some things which SLS regards as "match"
    events make more sense for our purposes as Round events, for example. Keep
    in mind that warhound has its own take on which category each event is.

    Match events are top-level "meta" events describing when the match was
    queued for, when it began, when the match (first round) starts, how each
    team performed at the end, etc.

    Round events describe something that happened in a particular round, like
    the pickup of a health shard, or the use of an EX ability.

    Spell summary events provide an *overview* of a hero's performance through
    information about each spell. This is still a bit TBD as we figure out the
    resolution of each event. Whereas there are many round events for one round,
    there are many spell summary events for each round, each apparently
    providing information about one spell for one hero.

    See the `Kind` enum for a concrete list of types.
    """

    # infer_maybe_match defaults to "unknown match source_json."
    # In other words, at least one heuristic will return something.
    list_heuristic = [
        lambda source_json: infer_maybe_spellsummary_kind(source_json),
        lambda source_json: infer_maybe_round_kind(source_json),
        lambda source_json: infer_maybe_match_kind(source_json)
    ]

    for heuristic in list_heuristic:
        result = heuristic(source_json)
        if result:
            return result
    else:
        raise RuntimeError('insanity') # See comments above.


class Event(namedtuple('Event', ['kind', 'source_json'])):
    def __new__(cls, kind, source_json):
        return super().__new__(cls, kind, source_json)


def mk(*args, **kwargs):
    return Event(*args, **kwargs)


def json_object_to_event(json_object):
    return mk(infer_kind(json_object), json_object)
