from ..entity.user_round_spell import mk_empty_user_round_spell
from ..entity.match import mk_empty_match_outcome
from ..entity.server_shutdown import mk_empty_server_shutdown


def process_match_finished_event(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

    match_outcome                     = mk_empty_match_outcome()
    match_outcome.duration_sec        = data['matchLength']
    match_outcome.attrs               = data
    match_outcome.score_by_ordinal[1] = data['teamOneScore']
    match_outcome.score_by_ordinal[2] = data['teamTwoScore']

    match.outcome = match_outcome

    return None


def process_user_round_spell(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

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


def process_server_shutdown(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

    server_shutdown                    = mk_empty_server_shutdown()
    server_shutdown.match_duration_sec = data['matchTime']
    server_shutdown.reason             = data['reason']
    server_shutdown.attrs              = data

    match.server_shutdown = server_shutdown

    return None

