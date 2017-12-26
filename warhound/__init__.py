from collections import defaultdict, namedtuple

from .model.gameplay import mk_empty_death_event, mk_empty_round_event
from .model.battlerite import mk_empty_battlerite
from .model.match import mk_empty_match, mk_empty_match_outcome
from .model.player import mk_empty_player, mk_empty_player_round_outcome
from .model.round import mk_empty_round, mk_empty_round_outcome
from .model.server_shutdown import mk_empty_server_shutdown
from .model.team import mk_empty_team, mk_empty_team_round_outcome
from .model.user_round_spell import mk_empty_user_round_spell


class Event(namedtuple('Event', ['cursor', 'e_type', 'data'])):
    __slots__ = ()

    def __new__(cls, cursor, e_type, data):
        return super(Event, cls).__new__(cls, cursor, e_type, data)


def process_queue_event(event, match, state):
    cursor, e_type, data = event


    return None


def process_match_start(event, match, state):
    cursor, e_type, data = event

    match.match_id = data['matchID']
    match.attrs    = data

    return None


def process_match_reserved_user(event, match, state):
    cursor, e_type, data = event

    player             = mk_empty_player()
    player.player_id   = data['accountId']
    player.champion_id = data['character']
    player.attrs       = data

    match.player_by_id[player.player_id] = player

    team_id = data['teamId']
    side    = data['team']

    if team_id in match.team_by_id:
        team = match.team_by_id[team_id]
        team.player_by_id[player.player_id] = player
    else:
        team              = mk_empty_team()
        team.team_id      = team_id
        team.player_by_id = { player.player_id: player }
        match.team_by_id[team_id] = team

    player.team_id = team_id

    if side in match.team_by_id_by_ordinal:
        team_by_id = match.team_by_id_by_ordinal[side]
    else:
        team_by_id = match.team_by_id_by_ordinal[side] = {}

    team_by_id[team_id] = team

    return None


def process_battlerite_pick_event(event, match, state):
    cursor, e_type, data = event

    battlerite               = mk_empty_battlerite()
    battlerite.battlerite_id = data['battleriteType']
    battlerite.player_id     = data['userID']
    battlerite.champion_id   = data['character']
    battlerite.attrs         = data

    player = match.player_by_id[battlerite.player_id]
    player.battlerite_by_id[battlerite.battlerite_id] = battlerite

    return None


def process_round_event(event, match, state):
    cursor, e_type, data = event

    round_event             = mk_empty_round_event()
    round_event.player_id   = data['userID']
    round_event.champion_id = data['character']
    round_event.event_type  = data['type']
    round_event.attrs       = data

    ordinal        = data['round']
    state['round'] = ordinal

    player = match.player_by_id[round_event.player_id]

    if ordinal in player.list_gameplay_by_ordinal:
        list_gameplay = player.list_gameplay_by_ordinal[ordinal]
    else:
        list_gameplay = player.list_gameplay_by_ordinal[ordinal] = []

    list_gameplay.append(round_event)
    
    if ordinal in match.round_by_ordinal:
        _round = match.round_by_ordinal[ordinal]
    else:
        _round = match.round_by_ordinal[ordinal] = mk_empty_round()

    _round.list_gameplay.append(round_event)

    return None


def process_death_event(event, match, state):
    cursor, e_type, data = event

    death            = mk_empty_death_event()
    death.player_id  = data['userID']
    death.attrs      = data

    ordinal = state['round']

    if ordinal in match.round_by_ordinal:
        _round = match.round_by_ordinal[ordinal]
    else:
        _round = match.round_by_ordinal[ordinal] = mk_empty_round()

    _round.list_gameplay.append(death)

    return None


def process_round_finished_event(event, match, state):
    cursor, e_type, data = event

    round_outcome = mk_empty_round_outcome()
    ordinal = data['round']
    list_stats = data['playerStats']

    for _, team_by_id in match.team_by_id_by_ordinal.items():
        for team_id, team in team_by_id.items():
            won = data['winningTeam'] == ordinal

            team_round_outcome         = mk_empty_team_round_outcome()
            team_round_outcome.team_id = team.team_id
            team_round_outcome.round   = ordinal
            team_round_outcome.won     = won

            for player_id, player in team.player_by_id.items():
                l = lambda s: s['userID'] == player_id

                player_stats = list(filter(l, data['playerStats']))

                player_round_outcome = mk_empty_player_round_outcome()
                player_round_outcome.player_id = player_id
                player_round_outcome.team_id   = team_id
                player_round_outcome.round     = ordinal
                player_round_outcome.won       = won
                player_round_outcome.stats     = player_stats

                team_round_outcome.stats_by_player_id[player_id] = player_stats

                player.round_outcome_by_ordinal[ordinal] = player_round_outcome

            team.round_outcome_by_ordinal[ordinal] = team_round_outcome

    return None


def process_team_update_event(event, match, state):
    cursor, e_type, data = event

    # Store some form of team update

    return None


def process_match_finished_event(event, match, state):
    cursor, e_type, data = event

    match_outcome                     = mk_empty_match_outcome()
    match_outcome.duration_sec        = data['matchLength']
    match_outcome.attrs               = data
    match_outcome.score_by_ordinal[1] = data['teamOneScore']
    match_outcome.score_by_ordinal[2] = data['teamTwoScore']

    match.outcome = match_outcome

    return None


def process_user_round_spell(event, match, state):
    cursor, e_type, data = event

    user_round_spell             = mk_empty_user_round_spell()
    user_round_spell.player_id   = data['accountId']
    user_round_spell.champion_id = data['character']
    user_round_spell.attrs       = data

    ordinal = data['round']

    player = match.player_by_id[user_round_spell.player_id]

    if ordinal in player.list_user_round_spells_by_ordinal:
        list_user_round_spells = \
            player.list_user_round_spells_by_ordinal[ordinal]
    else:
        list_user_round_spells = \
            player.list_user_round_spells_by_ordinal[ordinal] = []

    list_user_round_spells.append(user_round_spell)

    if ordinal in match.round_by_ordinal:
        _round = match.round_by_ordinal[ordinal]
    else:
        _round = match.round_by_ordinal[ordinal] = mk_empty_round()

    _round.list_user_round_spells.append(user_round_spell)

    return None


def process_server_shutdown(event, match, state):
    cursor, e_type, data = event
    
    server_shutdown                    = mk_empty_server_shutdown()
    server_shutdown.match_duration_sec = data['matchTime']
    server_shutdown.reason             = data['reason']
    server_shutdown.attrs              = data

    match.server_shutdown = server_shutdown

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
    match             = mk_empty_match()
    state             = { round: 0 }

    for obj_event in ordered_by_cursor:
        attempt_process_event(PROCESSOR_BY_EVENT_TYPE, obj_event, match, state)

    return match

