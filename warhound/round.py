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
        self.dict_list_gameplay_by_team_id     = []
        self.dict_list_spell_info_by_team_id   = []
        self.dict_list_gameplay_by_player_id   = []
        self.dict_list_spell_info_by_player_id = []

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


def process_round_finished_event(event, _round, state):
    cursor, e_type, data = event

    _round.dict_finish_attribute_by_name = data

    return None


def process_round_event(event, _round, state):
    cursor, e_type, data = event

    player_id = data['userID']

    round_event                        = mk_empty_round_event()
    round_event.dict_attribute_by_name = data

    state['round'] = ordinal = data['round']

    _round.list_gameplay.append(round_event)

    return None


def process_death_event(event, _round, state):
    cursor, e_type, data = event

    player_id = data['userID']

    death_event                        = mk_empty_death_event()
    death_event.dict_attribute_by_name = data

    _round.list_gameplay.append(death_event)

    return None


def process_user_round_spell(event, match, state):
    cursor, e_type, data = event

    # user_round_spell             = mk_empty_user_round_spell()
    # user_round_spell.player_id   = data['accountId']
    # user_round_spell.champion_id = data['character']
    # user_round_spell.attrs       = data

    ordinal = data['round']

    # player = match.player_by_id[user_round_spell.player_id]

    # if ordinal in player.list_list_user_round_spells:
    #     list_user_round_spells = \
    #         player.list_list_user_round_spells[ordinal]
    # else:
    #     list_user_round_spells = []
    #     player.list_list_user_round_spells.append(list_user_round_spells)

    # list_user_round_spells.append(user_round_spell)

    # if ordinal in match.round_by_ordinal:
    #     _round = match.round_by_ordinal[ordinal]
    # else:
    #     _round = match.round_by_ordinal[ordinal] = mk_empty_round()

    # _round.list_user_round_spells.append(user_round_spell)

    return None


PROCESSOR_BY_EVENT_TYPE = \
    {
        'Structures.RoundEvent': process_round_event,
        'Structures.DeathEvent': process_death_event,
        'Structures.RoundFinishedEvent': process_round_finished_event,
        'Structures.UserRoundSpell': process_user_round_spell
    }

