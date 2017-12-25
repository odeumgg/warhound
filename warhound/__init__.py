from collections import defaultdict, namedtuple
import types


class Event(namedtuple('Event', ['cursor', 'e_type', 'data'])):
    __slots__ = ()

    def __new__(cls, cursor, e_type, data):
        return super(Event, cls).__new__(cls, cursor, e_type, data)


def process_queue_event(event, match, state):
    cursor, e_type, data = event


    return None


def process_match_start(event, match, state):
    cursor, e_type, data = event

    match.match_id                   = data['matchID']
    match.dict_attrs                 = data
    match.dict_team_by_id            = {}
    match.player_by_id               = {}
    match.dict_team_by_id_by_ordinal = defaultdict(dict)
    match.dict_round_by_ordinal      = defaultdict(types.SimpleNamespace)
    match.server_shutdown            = None

    return None


def process_match_reserved_user(event, match, state):
    cursor, e_type, data = event

    player = types.SimpleNamespace()
    player.player_id                              = data['accountId']
    player.champion_id                            = data['character']
    player.dict_attrs                             = data
    player.dict_battlerite_by_id                  = {}
    player.dict_round_performance_by_ordinal      = {}
    player.dict_list_all_events_by_ordinal        = defaultdict(list)
    player.dict_list_user_round_spells_by_ordinal = defaultdict(list)

    match.player_by_id[player.player_id] = player

    team_id = data['teamId']
    side    = data['team']

    if team_id in match.dict_team_by_id:
        team = match.dict_team_by_id[team_id]
        team.player_by_id[player.player_id] = player
    else:
        team              = types.SimpleNamespace()
        team.team_id      = team_id
        team.player_by_id = { player.player_id: player }
        match.dict_team_by_id[team_id] = team

    match.dict_team_by_id_by_ordinal[side][team_id] = team

    return None


def process_battlerite_pick_event(event, match, state):
    cursor, e_type, data = event

    battlerite = types.SimpleNamespace()
    battlerite.battlerite_id = data['battleriteType']
    battlerite.player_id     = data['userID']
    battlerite.champion_id   = data['character']
    battlerite.dict_attrs    = data

    player = match.player_by_id[battlerite.player_id]
    player.dict_battlerite_by_id[battlerite.battlerite_id] = battlerite

    return None


def process_round_event(event, match, state):
    cursor, e_type, data = event

    round_event             = types.SimpleNamespace()
    round_event.player_id   = data['userID']
    round_event.champion_id = data['character']
    round_event.event_type  = data['type']
    round_event.dict_attrs  = data

    ordinal        = data['round']
    state['round'] = ordinal

    player = match.player_by_id[round_event.player_id]
    player.dict_list_all_events_by_ordinal[ordinal].append(round_event)
    
    _round = match.dict_round_by_ordinal[ordinal]

    if not hasattr(_round, 'list_all_events'):
        _round.list_all_events = [round_event]
    else:
        _round.list_all_events.append(round_event)

    return None


def process_death_event(event, match, state):
    cursor, e_type, data = event

    death            = types.SimpleNamespace()
    death.player_id  = data['userID']
    death.event_type = 'DEATH'
    death.dict_attrs = data

    ordinal = state['round']

    _round = match.dict_round_by_ordinal[ordinal]

    if not hasattr(_round, 'list_all_events'):
        _round.list_all_events = [death]
    else:
        _round.list_all_events.append(death)

    return None


def process_round_finished_event(event, match, state):
    cursor, e_type, data = event

    round_outcome = types.SimpleNamespace()

    # Store team round performance
    # Story player round performance

    return None


def process_team_update_event(event, match, state):
    cursor, e_type, data = event

    # Store some form of team update

    return None


def process_match_finished_event(event, match, state):
    cursor, e_type, data = event

    match_outcome                       = types.SimpleNamespace()
    match_outcome.duration_sec          = data['matchLength']
    match_outcome.dict_attrs            = data
    match_outcome.dict_score_by_ordinal = \
        { 1: data['teamOneScore'], 2: data['teamTwoScore'] }

    match.outcome = match_outcome

    return None


def process_user_round_spell(event, match, state):
    cursor, e_type, data = event

    user_round_spell             = types.SimpleNamespace()
    user_round_spell.player_id   = data['accountId']
    user_round_spell.champion_id = data['character']
    user_round_spell.dict_attrs  = data

    ordinal = data['round']

    player = match.player_by_id[user_round_spell.player_id]
    player.list_user_round_spells_by_ordinal[ordinal].append(user_round_spell)
    
    _round = match.dict_round_by_ordinal[ordinal]

    if not hasattr(_round, 'list_user_round_spells'):
        _round.list_user_round_spells = [user_round_spell]
    else:
        _round.list_user_round_spells.append(user_round_spell)

    return None


def process_server_shutdown(event, match, state):
    cursor, e_type, data = event
    
    server_shutdown                    = types.SimpleNamespace()
    server_shutdown.match_duration_sec = data['matchTime']
    server_shutdown.reason             = data['reason']
    server_shutdown.dict_attrs         = data

    return None


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
        'com.stunlock.battlerite.team.TeamUpdateEvent':
            process_team_update_event,
        'Structures.MatchFinishedEvent': process_match_finished_event,
        'Structures.UserRoundSpell': process_user_round_spell,
        'Structures.ServerShutdown': process_server_shutdown
    }


def attempt_process_event(dict_processor_by_event_type, obj_event, match,
                          state):
    e_type          = obj_event['type']
    maybe_processor = dict_processor_by_event_type[e_type]

    if maybe_processor:
        event = Event(obj_event['cursor'], e_type, obj_event['dataObject'])
        maybe_processor(event, match, state)
    else:
        print('encountered unknown event: {0}'.format(e_type))

    return None


def process(obj):
    ordered_by_cursor = sorted(obj, key=lambda e: e['cursor'])
    match             = types.SimpleNamespace()
    state             = { round: 0 }

    for obj_event in ordered_by_cursor:
        attempt_process_event(PROCESSOR_BY_EVENT_TYPE, obj_event, match, state)

    return match

