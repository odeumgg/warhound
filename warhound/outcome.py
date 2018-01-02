from collections import defaultdict
from .util import OneIndexedList


class TeamRoundPerformance:
    __slots__ = ('team_id', 'round', 'won', 'stats_by_player_id')


    def __init__(self):
        self.team_id            = None
        self.round              = None
        self.won                = None
        self.stats_by_player_id = {}


class TeamMatchPerformance:
    __slots__ = ()


    def __init__(self):
        pass


class PlayerRoundPerformance:
    __slots__ = ('player_id', 'team_id', 'round', 'won', 'stats')


    def __init__(self):
        self.player_id = None
        self.team_id   = None
        self.round     = None
        self.won       = None
        self.stats     = None


class PlayerMatchPerformance:
    __slots__ = ('match_id', 'attrs')


    def __init__(self):
        pass


class Outcome:
    __slots__ = ()

    
    def __init__(self):
        pass


def mk_empty_team_round_performance():
    return TeamRoundPerformance()


def mk_empty_team_match_performance():
    return TeamMatchPerformance()


def mk_empty_player_round_performance():
    return PlayerRoundPerformance()


def mk_empty_player_match_performance():
    return PlayerMatchPerformance()


def mk_empty_outcome():
    return Outcome()


def process_round_finished_event(event, outcome, state):
    cursor, e_type, data = event

    ordinal = data['round']

    # for index, team_by_id in enumerate(match.list_dict_team_by_id, start=1):
    #     for team_id, team in team_by_id.items():
    #         won = data['winningTeam'] == index

    #         team_round_performance         = mk_empty_team_round_performance()
    #         team_round_performance.team_id = team.team_id
    #         team_round_performance.round   = ordinal
    #         team_round_performance.won     = won

    #         for player_id, player in team.player_by_id.items():
    #             l = lambda s: s['userID'] == player_id

    #             player_stats = list(filter(l, data['playerStats']))

    #             player_round_performance = mk_empty_player_round_performance()
    #             player_round_performance.player_id = player_id
    #             player_round_performance.team_id   = team_id
    #             player_round_performance.round     = ordinal
    #             player_round_performance.won       = won
    #             player_round_performance.stats     = player_stats

    #             team_round_performance.stats_by_player_id[player_id] = player_stats

    #             outcome.list_player_round_performance_by_player_id[player_id].append(player_round_performance)

    #         outcome.list_team_round_performance_by_team_id[player_id].append(team_round_performance)

    return None


def process_match_finished_event(event, outcome, state):
    cursor, e_type, data        = event

    # outcome                     = mk_empty_outcome()

    return None


def process_team_update_event(event, outcome, state):
    cursor, e_type, data = event

    # Store some form of team update

    return None


PROCESSOR_BY_EVENT_TYPE = \
    {
        'Structures.RoundFinishedEvent': process_round_finished_event,
        'Structures.MatchFinishedEvent': process_match_finished_event,
        'com.stunlock.battlerite.team.TeamUpdateEvent':
            process_team_update_event,
    }

