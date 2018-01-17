import pytest

from warhound import match, match_round


def test_mk_battlerite(mocker):
    result = match.mk_battlerite()

    assert type(result) is match.Battlerite


def test_mk_player(mocker):
    result = match.mk_player()

    assert type(result) is match.Player


def test_mk_team(mocker):
    result = match.mk_team()

    assert type(result) is match.Team


def test_mk_match(mocker):
    mocker.patch('warhound.match_round.mk_round',
                 return_value=None, autospec=True)

    result = match.mk_match(3)

    assert match_round.mk_round.call_count == 3
    assert len(result.list_round) == 3
    assert type(result) is match.Match


def test_process_match_start(mocker):
    _match = match.mk_match(3)
    data   = { 'foo': 'bar' } # mock
    state  = None # mock

    assert _match.dict_start_raw is None

    match.process_match_start(_match, data, state)

    assert _match.dict_start_raw == data


def test_process_match_reserved_user(mocker):
    _match = match.mk_match(3)
    data   = { 'accountId': '1234', 'teamId': '5678', 'team': 2 }
    state  = { 'dict_side_by_player_id': {},
               'dict_team_id_by_player_id': {} }

    fake_player = match.mk_player()
    mocker.patch('warhound.match.mk_player',
                 return_value=fake_player, autospec=True)
    fake_team = match.mk_team()
    mocker.patch('warhound.match.mk_team',
                 return_value=fake_team, autospec=True)

    assert fake_player.raw is None
    assert '5678' not in _match.dict_team_by_id
    assert '1234' not in _match.dict_team_id_by_player_id
    assert '1234' not in _match.dict_player_by_id
    assert '5678' not in _match.list_dict_team_by_id[2]

    match.process_match_reserved_user(_match, data, state)

    assert fake_player.raw == data
    assert _match.dict_team_by_id['5678'] == fake_team
    assert _match.dict_team_id_by_player_id['1234'] == '5678'
    assert _match.dict_player_by_id['1234'] == fake_player
    assert _match.list_dict_team_by_id[2]['5678'] == fake_team

    assert state[   'dict_side_by_player_id']['1234'] == 2
    assert state['dict_team_id_by_player_id']['1234'] == '5678'

    assert match.mk_player.call_count == 1
    assert match.mk_team.call_count == 1


def test_process_battlerite_pick_event(mocker):
    _match = match.mk_match(3)
    data   = { 'battleriteType': '8989', 'userID': '1234' }
    state  = None # mock

    fake_player = match.mk_player()
    _match.dict_player_by_id['1234'] = fake_player

    assert '8989' not in fake_player.dict_battlerite_by_id

    fake_battlerite = match.mk_battlerite()
    mocker.patch('warhound.match.mk_battlerite',
                 return_value=fake_battlerite, autospec=True)

    match.process_battlerite_pick_event(_match, data, state)

    assert fake_battlerite.raw == data
    assert fake_player.dict_battlerite_by_id['8989'] == fake_battlerite


def test_process_match_finished_event(mocker):
    _match = match.mk_match(3)
    data   = { 'foo': 'bar' } # mock
    state  = None # mock

    assert _match.dict_finish_raw is None

    match.process_match_finished_event(_match, data, state)

    assert _match.dict_finish_raw == data


def test_process_server_shutdown(mocker):
    _match = match.mk_match(3)
    data   = { 'foo': 'bar' } # mock
    state  = None # mock

    assert _match.dict_shutdown_raw is None

    match.process_server_shutdown(_match, data, state)

    assert _match.dict_shutdown_raw == data

