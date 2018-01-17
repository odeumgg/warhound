from . import util
from . import match_round


class Battlerite:
    __slots__ = ('raw')

    def __init__(self):
        self.raw = None


class Player:
    __slots__ = ('raw', 'dict_battlerite_by_id')

    
    def __init__(self):
        self.raw                    = None
        self.dict_battlerite_by_id  = {}


class Team:
    __slots__ = ('dict_team_by_id', 'dict_player_by_id')


    def __init__(self):
        self.dict_team_by_id   = {}
        self.dict_player_by_id = {}


class Match:
    __slots__ = ('dict_start_raw', 'dict_finish_raw',
                 'dict_shutdown_raw', 'dict_team_by_id',
                 'dict_team_id_by_player_id', 'dict_player_by_id',
                 'list_dict_team_by_id', 'list_round')


    def __init__(self):
        self.dict_start_raw            = None
        self.dict_finish_raw           = None
        self.dict_shutdown_raw         = None
        self.dict_team_by_id           = {}
        self.dict_team_id_by_player_id = {}
        self.dict_player_by_id         = {}
        self.list_dict_team_by_id      = util.mk_oil() # by side
        self.list_round                = []


def mk_battlerite():
    return Battlerite()


def mk_player():
    return Player()


def mk_team():
    return Team()


def mk_match(num_round):
    """
    The telemetry demarcates rounds only when they end. We could always
    allocate a new round at the end of the current one, but would have an
    off-by-one problem on the last round without looking ahead.

    To avoid this conundrum, we count the number of rounds before parsing
    and create empty placeholders for the correct number.
    """
    match = Match()

    match.list_round = \
        [match_round.mk_round() for i in range(0, num_round)]

    # one dict for each side...
    match.list_dict_team_by_id.append({})
    match.list_dict_team_by_id.append({})

    return match


def process_match_start(match, data, state):
    match.dict_start_raw = data

    return None


def process_match_reserved_user(match, data, state):
    player_id = data['accountId']
    team_id   = data['teamId']
    side      = data['team']

    player     = mk_player()
    player.raw = data

    team = match.dict_team_by_id.get(team_id, mk_team())

    team.dict_player_by_id[player_id] = player

    match.dict_team_by_id[team_id]             = team
    match.dict_team_id_by_player_id[player_id] = team_id
    match.dict_player_by_id[player_id]         = player
    match.list_dict_team_by_id[side][team_id]  = team

    state[   'dict_side_by_player_id'][player_id] = side
    state['dict_team_id_by_player_id'][player_id] = team_id

    return None


def process_battlerite_pick_event(match, data, state):
    battlerite_id = data['battleriteType']
    player_id     = data['userID']

    battlerite     = mk_battlerite()
    battlerite.raw = data

    player = match.dict_player_by_id[player_id]
    player.dict_battlerite_by_id[battlerite_id] = battlerite

    return None


def process_match_finished_event(match, data, state):
    match.dict_finish_raw = data

    return None


def process_server_shutdown(match, data, state):
    match.dict_shutdown_raw = data

    return None


PROCESSOR_BY_EVENT_TYPE = \
    { 'Structures.MatchStart': process_match_start,
      'Structures.MatchReservedUser': process_match_reserved_user,
      'Structures.BattleritePickEvent': process_battlerite_pick_event,
      'Structures.MatchFinishedEvent': process_match_finished_event,
      'Structures.ServerShutdown': process_server_shutdown }

