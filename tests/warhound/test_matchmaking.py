import pytest

from warhound import matchmaking


def test_mk_queue_event(mocker):
    queue_event = matchmaking.mk_queue_event()

    assert type(queue_event) is matchmaking.QueueEvent


def test_mk_matchmaking(mocker):
    _matchmaking = matchmaking.mk_matchmaking()

    assert type(_matchmaking) is matchmaking.Matchmaking


def test_process_queue_event(mocker):
    _matchmaking = matchmaking.mk_matchmaking()
    data         = { 'userId': '1234' }
    state        = None # mock

    fake_queue_event = matchmaking.mk_queue_event()
    mocker.patch('warhound.matchmaking.mk_queue_event',
                 return_value=fake_queue_event, autospec=True)

    assert fake_queue_event.raw is None
    assert '1234' not in _matchmaking.dict_queue_event_by_player_id

    matchmaking.process_queue_event(_matchmaking, data, state)

    assert fake_queue_event.raw == data
    assert _matchmaking.dict_queue_event_by_player_id['1234'] == \
        fake_queue_event

