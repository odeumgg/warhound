import pytest

from warhound import match_round


def test_mk_round_event(mocker):
    round_event = match_round.mk_round_event()

    assert type(round_event) is match_round.RoundEvent


def test_mk_death_event(mocker):
    death_event = match_round.mk_death_event()

    assert type(death_event) is match_round.DeathEvent


def test_mk_user_round_spell(mocker):
    user_round_spell = match_round.mk_user_round_spell()

    assert type(user_round_spell) is match_round.UserRoundSpell


def test_mk_round(mocker):
    _round = match_round.mk_round()

    assert len(_round.list_list_gameplay) == 2
    assert len(_round.list_list_spell_info) == 2
    assert type(_round) is match_round.Round


def test_process_round_finished_event(mocker):
    _round = match_round.mk_round()
    data   = None # mock
    state  = None # mock

    assert _round.dict_finish_raw is None

    match_round.process_round_finished_event(_round, data, state)

    assert _round.dict_finish_raw == data


def test_process_round_event(mocker):
    _round = match_round.mk_round()
    data   = { 'userID': '1234', 'round': 2 }
    state  = { 'dict_side_by_player_id': { '1234': 1 },
               'dict_team_id_by_player_id': { '1234': '5678' } }

    fake_round_event = match_round.mk_round_event()
    mocker.patch('warhound.match_round.mk_round_event',
                 return_value=fake_round_event, autospec=True)

    assert fake_round_event.raw is None
    assert _round.list_gameplay == []
    assert _round.list_list_gameplay[1] == []
    assert _round.dict_list_gameplay_by_team_id['5678'] == []
    assert _round.dict_list_gameplay_by_player_id['1234'] == []

    match_round.process_round_event(_round, data, state)

    assert fake_round_event.raw == data
    assert state['round'] == 2
    assert _round.list_gameplay == [fake_round_event]
    assert _round.list_list_gameplay[1] == [fake_round_event]
    assert _round.dict_list_gameplay_by_team_id['5678'] == [fake_round_event]
    assert _round.dict_list_gameplay_by_player_id['1234'] == [fake_round_event]


def test_process_death_event(mocker):
    _round = match_round.mk_round()
    data   = { 'userID': '1234' }
    state  = { 'dict_side_by_player_id': { '1234': 1 },
               'dict_team_id_by_player_id': { '1234': '5678' } }

    fake_death_event = match_round.mk_death_event()
    mocker.patch('warhound.match_round.mk_death_event',
                 return_value=fake_death_event, autospec=True)

    assert fake_death_event.raw is None
    assert _round.list_gameplay == []
    assert _round.list_list_gameplay[1] == []
    assert _round.dict_list_gameplay_by_team_id['5678'] == []
    assert _round.dict_list_gameplay_by_player_id['1234'] == []

    match_round.process_death_event(_round, data, state)

    assert fake_death_event.raw == data
    assert _round.list_gameplay == [fake_death_event]
    assert _round.list_list_gameplay[1] == [fake_death_event]
    assert _round.dict_list_gameplay_by_team_id['5678'] == [fake_death_event]
    assert _round.dict_list_gameplay_by_player_id['1234'] == [fake_death_event]


def test_process_user_round_spell(mocker):
    _round = match_round.mk_round()
    data   = { 'accountId': '1234', 'round': 1 }
    state  = { 'dict_side_by_player_id': { '1234': 1 },
               'dict_team_id_by_player_id': { '1234': '5678' } }

    fake_user_round_spell = match_round.mk_user_round_spell()
    mocker.patch('warhound.match_round.mk_user_round_spell',
                 return_value=fake_user_round_spell, autospec=True)

    assert fake_user_round_spell.raw is None
    assert _round.list_spell_info == []
    assert _round.list_list_spell_info[1] == []
    assert _round.dict_list_spell_info_by_team_id['5678'] == []
    assert _round.dict_list_spell_info_by_player_id['1234'] == []

    match_round.process_user_round_spell(_round, data, state)

    assert fake_user_round_spell.raw == data
    assert _round.list_spell_info == [fake_user_round_spell]
    assert _round.list_list_spell_info[1] == [fake_user_round_spell]
    assert _round.dict_list_spell_info_by_team_id['5678'] == [fake_user_round_spell]
    assert _round.dict_list_spell_info_by_player_id['1234'] == [fake_user_round_spell]

