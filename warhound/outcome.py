from collections import defaultdict

from warhound import util


class PlayerRoundStats:
    __slots__ = ('raw')


    def __init__(self):
        self.raw = None


class RoundSummary:
    __slots__ = ('raw', 'list_dict_player_round_stats_by_player_id',
                 'dict_player_round_stats_by_player_id')


    def __init__(self):
        self.raw                                       = None
        self.list_dict_player_round_stats_by_player_id = util.mk_oil()
        self.dict_player_round_stats_by_player_id      = {}


class TeamUpdate:
    __slots__ = ('raw')


    def __init__(self):
        self.raw = None


class Outcome:
    __slots__ = ('raw', 'list_round_summary', 'dict_team_update_by_team_id')

    
    def __init__(self):
        self.raw                         = None
        self.list_round_summary          = []
        self.dict_team_update_by_team_id = {}


def mk_player_round_stats():
    return PlayerRoundStats()


def mk_round_summary():
    round_summary = RoundSummary()

    # one dict for each side...
    round_summary.list_dict_player_round_stats_by_player_id.append({})
    round_summary.list_dict_player_round_stats_by_player_id.append({})

    return round_summary


def mk_team_update():
    return TeamUpdate()


def mk_outcome(num_rounds):
    outcome = Outcome()
    outcome.list_round_summary = \
        [mk_round_summary() for i in range(0, num_rounds)]

    return outcome


def process_round_stats(round_summary, data, state):
    player_id = data['userID']
    side      = state['dict_side_by_player_id'][player_id]

    player_round_stats     = mk_player_round_stats()
    player_round_stats.raw = data

    round_summary.list_dict_player_round_stats_by_player_id[side][player_id] = \
        player_round_stats
    round_summary.dict_player_round_stats_by_player_id[player_id] = \
        player_round_stats

    return None


def process_round_finished_event(outcome, data, state):
    ordinal = data['round']
    
    round_summary     = outcome.list_round_summary[ordinal]
    round_summary.raw = data

    for obj_stats in data['playerStats']:
        process_round_stats(round_summary, obj_stats, state)

    return None


def process_match_finished_event(outcome, data, state):
    outcome.raw = data

    return None


def process_team_update_event(outcome, data, state):
    team_id = data['teamID']

    team_update                                  = mk_team_update()
    team_update.raw                              = data
    outcome.dict_team_update_by_team_id[team_id] = team_update

    return None


PROCESSOR_BY_EVENT_TYPE = \
    { 'Structures.RoundFinishedEvent': process_round_finished_event,
      'Structures.MatchFinishedEvent': process_match_finished_event,
      'com.stunlock.battlerite.team.TeamUpdateEvent':
            process_team_update_event }

