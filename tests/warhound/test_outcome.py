import pytest

from warhound import outcome


def test_mk_player_round_stats(mocker):
    result = outcome.mk_player_round_stats()

    assert type(result) is outcome.PlayerRoundStats


def test_mk_round_summary(mocker):
    result = outcome.mk_round_summary()

    assert len(result.list_dict_player_round_stats_by_player_id) == 2
    assert type(result) is outcome.RoundSummary


def test_mk_team_update(mocker):
    result = outcome.mk_team_update()

    assert type(result) is outcome.TeamUpdate


def test_mk_outcome(mocker):
    result = outcome.mk_outcome(3)

    assert len(result.list_round_summary) == 3
    assert type(result) is outcome.Outcome


def test_process_round_stats(mocker):
    round_summary = outcome.mk_round_summary()
    data          = { 'userID': '1234' }
    state         = { 'dict_side_by_player_id': { '1234': 2 } }

    fake_player_round_stats = outcome.PlayerRoundStats()
    mocker.patch('warhound.outcome.mk_player_round_stats',
                 return_value=fake_player_round_stats, autospec=True)

    assert fake_player_round_stats.raw is None
    assert '1234' not in \
        round_summary.list_dict_player_round_stats_by_player_id[2]
    assert '1234' not in round_summary.dict_player_round_stats_by_player_id

    outcome.process_round_stats(round_summary, data, state)

    assert fake_player_round_stats.raw == data
    assert round_summary.list_dict_player_round_stats_by_player_id[2]['1234'] == \
        fake_player_round_stats
    assert round_summary.dict_player_round_stats_by_player_id['1234'] == \
        fake_player_round_stats


def test_process_round_finished_event(mocker):
    _outcome = outcome.mk_outcome(3)
    data     = { 'round': 2, 'playerStats': [1, 2, 3] } # mock with fake data
    state    = None # mock

    mocker.patch('warhound.outcome.process_round_stats')

    assert _outcome.list_round_summary[2].raw == None # for round 2

    outcome.process_round_finished_event(_outcome, data, state)

    assert _outcome.list_round_summary[2].raw == data
    assert outcome.process_round_stats.call_count == 3


def test_process_match_finished_event(mocker):
    _outcome = outcome.mk_outcome(3)
    data     = { 'data': 1 } # mock
    state    = None # mock

    assert _outcome.raw is None

    outcome.process_match_finished_event(_outcome, data, state)

    assert _outcome.raw == data


def test_process_team_update_event(mocker):
    _outcome = outcome.mk_outcome(3)
    data     = { 'teamID': '5678' } # mock
    state    = None # mock

    fake_team_update = outcome.mk_team_update()
    mocker.patch('warhound.outcome.mk_team_update',
                 return_value=fake_team_update, autospec=True)

    assert '5678' not in _outcome.dict_team_update_by_team_id

    outcome.process_team_update_event(_outcome, data, state)

    assert fake_team_update.raw is not None
    assert _outcome.dict_team_update_by_team_id['5678'] == fake_team_update

