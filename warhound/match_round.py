from collections import defaultdict

from warhound import util


class RoundEvent:
    __slots__ = ('raw')


    def __init__(self):
        self.raw = None


class DeathEvent:
    __slots__ = ('raw')


    def __init__(self):
        self.raw = None


class UserRoundSpell:
    __slots__ = ('raw')


    def __init__(self):
        self.raw = None


class Round:
    __slots__ = ('dict_finish_raw', 'list_gameplay', 'list_spell_info',
                 'list_list_gameplay', 'list_list_spell_info',
                 'dict_list_gameplay_by_team_id',
                 'dict_list_spell_info_by_team_id',
                 'dict_list_gameplay_by_player_id',
                 'dict_list_spell_info_by_player_id')


    def __init__(self):
        self.dict_finish_raw                   = None
        self.list_gameplay                     = []
        self.list_spell_info                   = []
        self.list_list_gameplay                = util.mk_oil() # by side
        self.list_list_spell_info              = util.mk_oil() # by side
        self.dict_list_gameplay_by_team_id     = defaultdict(list)
        self.dict_list_spell_info_by_team_id   = defaultdict(list)
        self.dict_list_gameplay_by_player_id   = defaultdict(list)
        self.dict_list_spell_info_by_player_id = defaultdict(list)


def mk_round_event():
    return RoundEvent()


def mk_death_event():
    return DeathEvent()


def mk_user_round_spell():
    return UserRoundSpell()


def mk_round():
    match_round = Round()

    # one for each side...
    match_round.list_list_gameplay.append([])
    match_round.list_list_gameplay.append([])

    # one for each side...
    match_round.list_list_spell_info.append([])
    match_round.list_list_spell_info.append([])

    return match_round


def process_round_finished_event(_round, data, state):
    _round.dict_finish_raw = data

    return None


def process_round_event(_round, data, state):
    player_id = data['userID']
    side      = state[   'dict_side_by_player_id'][player_id]
    team_id   = state['dict_team_id_by_player_id'][player_id]

    round_event     = mk_round_event()
    round_event.raw = data

    _round.list_gameplay.append(round_event)
    _round.list_list_gameplay[side].append(round_event)
    _round.dict_list_gameplay_by_team_id[team_id].append(round_event)
    _round.dict_list_gameplay_by_player_id[player_id].append(round_event)

    state['round'] = ordinal = data['round']

    return None


def process_death_event(_round, data, state):
    player_id = data['userID']
    side      = state[   'dict_side_by_player_id'][player_id]
    team_id   = state['dict_team_id_by_player_id'][player_id]

    death_event     = mk_death_event()
    death_event.raw = data

    _round.list_gameplay.append(death_event)
    _round.list_list_gameplay[side].append(death_event)
    _round.dict_list_gameplay_by_team_id[team_id].append(death_event)
    _round.dict_list_gameplay_by_player_id[player_id].append(death_event)

    return None


def process_user_round_spell(_round, data, state):
    player_id = data['accountId']
    ordinal   = data['round']
    side      = state[   'dict_side_by_player_id'][player_id]
    team_id   = state['dict_team_id_by_player_id'][player_id]

    user_round_spell     = mk_user_round_spell()
    user_round_spell.raw = data

    _round.list_spell_info.append(user_round_spell)
    _round.list_list_spell_info[side].append(user_round_spell)
    _round.dict_list_spell_info_by_team_id[team_id].append(user_round_spell)
    _round.dict_list_spell_info_by_player_id[player_id].append(user_round_spell)

    return None


PROCESSOR_BY_EVENT_TYPE = \
    { 'Structures.RoundEvent': process_round_event,
      'Structures.DeathEvent': process_death_event,
      'Structures.RoundFinishedEvent': process_round_finished_event,
      'Structures.UserRoundSpell': process_user_round_spell }

