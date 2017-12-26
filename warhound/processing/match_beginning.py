from ..entity.battlerite import mk_empty_battlerite
from ..entity.gameplay import mk_empty_round_event, mk_empty_death_event
from ..entity.player import mk_empty_player
from ..entity.team import mk_empty_team


def process_match_start(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

    match.match_id = data['matchID']
    match.attrs    = data

    return None


def process_match_reserved_user(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

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


def process_battlerite_pick_event(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

    battlerite               = mk_empty_battlerite()
    battlerite.battlerite_id = data['battleriteType']
    battlerite.player_id     = data['userID']
    battlerite.champion_id   = data['character']
    battlerite.attrs         = data

    player = match.player_by_id[battlerite.player_id]
    player.battlerite_by_id[battlerite.battlerite_id] = battlerite

    return None

