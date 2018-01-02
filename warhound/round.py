from collections import defaultdict

from .util import OneIndexedList


class RoundEvent:
    __slots__ = ('dict_attribute_by_name')


    def __init__(self):
        self.dict_attribute_by_name = {}


class DeathEvent:
    __slots__ = ('dict_attribute_by_name')


    def __init__(self):
        self.dict_attribute_by_name = {}


class UserRoundSpell:
    __slots__ = ('dict_attribute_by_name')


    def __init__(self):
        self.dict_attribute_by_name = {}


class Round:
    __slots__ = ('dict_finish_attribute_by_name', 'list_gameplay',
                 'list_spell_info', 'list_list_gameplay',
                 'list_list_spell_info',
                 'dict_list_gameplay_by_team_id',
                 'dict_list_spell_info_by_team_id',
                 'dict_list_gameplay_by_player_id',
                 'dict_list_spell_info_by_player_id')


    def __init__(self):
        self.dict_finish_attribute_by_name     = {}
        self.list_gameplay                     = []
        self.list_spell_info                   = []
        self.list_list_gameplay                = OneIndexedList() # by side
        self.list_list_spell_info              = OneIndexedList() # by side
        self.dict_list_gameplay_by_team_id     = defaultdict(list)
        self.dict_list_spell_info_by_team_id   = defaultdict(list)
        self.dict_list_gameplay_by_player_id   = defaultdict(list)
        self.dict_list_spell_info_by_player_id = defaultdict(list)

        # one for each side...
        self.list_list_gameplay.append([])
        self.list_list_gameplay.append([])

        # one for each side...
        self.list_list_spell_info.append([])
        self.list_list_spell_info.append([])


def mk_empty_round_event():
    return RoundEvent()


def mk_empty_death_event():
    return DeathEvent()


def mk_empty_user_round_spell():
    return UserRoundSpell()


def mk_empty_round():
    return Round()


def process_round_finished_event(_round, data, state):
    _round.dict_finish_attribute_by_name = data

    return None


def process_round_event(_round, data, state):
    player_id = data['userID']
    side      = state[   'dict_side_by_player_id'][player_id]
    team_id   = state['dict_team_id_by_player_id'][player_id]

    round_event                        = mk_empty_round_event()
    round_event.dict_attribute_by_name = data

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

    death_event                        = mk_empty_death_event()
    death_event.dict_attribute_by_name = data

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

    user_round_spell                        = mk_empty_user_round_spell()
    user_round_spell.dict_attribute_by_name = data

    _round.list_spell_info.append(user_round_spell)
    _round.list_list_spell_info[side].append(user_round_spell)
    _round.dict_list_spell_info_by_team_id[team_id].append(user_round_spell)
    _round.dict_list_spell_info_by_player_id[player_id].append(user_round_spell)

    return None


PROCESSOR_BY_EVENT_TYPE = \
    {
        'Structures.RoundEvent': process_round_event,
        'Structures.DeathEvent': process_death_event,
        'Structures.RoundFinishedEvent': process_round_finished_event,
        'Structures.UserRoundSpell': process_user_round_spell
    }

