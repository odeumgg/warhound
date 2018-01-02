from .util import OneIndexedList
from .round import mk_empty_round


class Battlerite:
    __slots__ = ('dict_attribute_by_name')

    def __init__(self):
        self.dict_attribute_by_name = {}


class Player:
    __slots__ = ('dict_attribute_by_name', 'dict_battlerite_by_id')

    
    def __init__(self):
        self.dict_attribute_by_name = {}
        self.dict_battlerite_by_id  = {}


class Team:
    __slots__ = ('dict_team_by_id', 'dict_player_by_id')


    def __init__(self):
        self.dict_team_by_id   = {}
        self.dict_player_by_id = {}


class Match:
    __slots__ = ('dict_start_attribute_by_name',
                 'dict_finish_attribute_by_name',
                 'dict_shutdown_attribute_by_name', 'dict_team_by_id',
                 'dict_team_id_by_player_id', 'dict_player_by_id',
                 'list_dict_team_by_id', 'list_round')


    def __init__(self):
        self.dict_start_attribute_by_name    = {}
        self.dict_finish_attribute_by_name   = {}
        self.dict_shutdown_attribute_by_name = {}
        self.dict_team_by_id                 = {}
        self.dict_team_id_by_player_id       = {}
        self.dict_player_by_id               = {}
        self.list_dict_team_by_id            = OneIndexedList() # by side
        self.list_round                      = []

        # one dict for each side...
        self.list_dict_team_by_id.append({})
        self.list_dict_team_by_id.append({})


def mk_empty_battlerite():
    return Battlerite()


def mk_empty_player():
    return Player()


def mk_empty_team():
    return Team()


def mk_empty_match(num_round):
    """
    The telemetry demarcates rounds only when they end. We could always
    allocate a new round at the end of the current one, but would have an
    off-by-one problem on the last round without looking ahead.

    To avoid this conundrum, we count the number of rounds before parsing
    and create empty placeholders for the correct number.
    """
    match = Match()

    for ordinal in range(0, num_round):
        match.list_round.append(mk_empty_round())

    return match


def process_match_start(event, match, state):
    cursor, e_type, data = event

    match.dict_start_attribute_by_name = data

    return None


def process_match_reserved_user(event, match, state):
    cursor, e_type, data = event

    player_id = data['accountId']
    team_id   = data['teamId']
    side      = data['team']

    player                        = mk_empty_player()
    player.dict_attribute_by_name = data

    team = match.dict_team_by_id.get(team_id, mk_empty_team())

    team.dict_player_by_id[player_id] = player

    match.dict_team_by_id[team_id]             = team
    match.dict_team_id_by_player_id[player_id] = team_id
    match.dict_player_by_id[player_id]         = player
    match.list_dict_team_by_id[side][team_id]  = team

    state['dict_team_id_by_player_id'][player_id] = team_id
    state[   'dict_side_by_player_id'][player_id] = side

    return None


def process_battlerite_pick_event(event, match, state):
    cursor, e_type, data = event

    battlerite_id = data['battleriteType']
    player_id     = data['userID']

    battlerite                        = mk_empty_battlerite()
    battlerite.dict_attribute_by_name = data

    player = match.dict_player_by_id[player_id]
    player.dict_battlerite_by_id[battlerite_id] = battlerite

    return None


def process_match_finished_event(event, match, state):
    cursor, e_type, data = event

    match.dict_finish_attribute_by_name = data

    return None


def process_server_shutdown(event, match, state):
    cursor, e_type, data = event

    match.dict_shutdown_attribute_by_name = data

    return None


PROCESSOR_BY_EVENT_TYPE = \
    {
        'Structures.MatchStart': process_match_start,
        'Structures.MatchReservedUser': process_match_reserved_user,
        'Structures.BattleritePickEvent': process_battlerite_pick_event,
        'Structures.MatchFinishedEvent': process_match_finished_event,
        'Structures.ServerShutdown': process_server_shutdown
    }

