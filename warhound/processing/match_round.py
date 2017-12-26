from ..entity.gameplay import mk_empty_round_event, mk_empty_death_event
from ..entity.round import mk_empty_round, mk_empty_round_outcome
from ..entity.player import mk_empty_player_round_outcome
from ..entity.team import mk_empty_team_round_outcome


def process_round_event(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

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


def process_death_event(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

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


def process_round_finished_event(event, telemetry, state):
    cursor, e_type, data        = event
    matchmaking, match, outcome = telemetry

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

