import pytest
import types

import warhound


def test_null_unknown_processor(mocker):
    # This is just to get coverage. The processor doesn't do anything.
    result = warhound.mk_null_unknown_processor()
    result(None, None, None) # all mocks for no-op call


def test_maybe_proc_matchmaking(mocker):
    good_event = 'com.stunlock.service.matchmaking.avro.QueueEvent'
    good       = warhound.maybe_proc_matchmaking(good_event)

    assert type(good) is types.FunctionType
    assert warhound.maybe_proc_matchmaking('foo') is None


def test_maybe_proc_match(mocker):
    good = warhound.maybe_proc_match('Structures.MatchStart')

    assert type(good) is types.FunctionType
    assert warhound.maybe_proc_match('foo') is None


def test_maybe_proc_round(mocker):
    good = warhound.maybe_proc_round('Structures.RoundEvent')

    assert type(good) is types.FunctionType
    assert warhound.maybe_proc_round('foo') is None


def test_maybe_proc_outcome(mocker):
    good = warhound.maybe_proc_outcome('Structures.RoundFinishedEvent')

    assert type(good) is types.FunctionType
    assert warhound.maybe_proc_outcome('foo') is None


def test_round_finished(mocker):
    good = { 'type': 'Structures.RoundFinishedEvent' }

    assert warhound.test_round_finished(good) is True
    assert warhound.test_round_finished({ 'type': 'foo' }) is False


def test_process_single(mocker):
    output = []

    lambda_1 = lambda x, y, z: output.append((x, y, z))
    lambda_2 = lambda x, y, z: output.append((x, y, z))

    list_pairs  = [ ({}, lambda_1), ({}, lambda_2) ]
    data_object = { 'data': 'fake' } # mock
    state       = { 'state': 1 } # mock

    warhound.process_single(list_pairs, data_object, state)

    assert len(output) == 2
    assert output[0] == ({}, data_object, state)
    assert output[1] == ({}, data_object, state)


def test_process(mocker):
    obj = [ { 'cursor': 100, 'type': 'Foo', 'dataObject': {} },
            { 'cursor': 101, 'type': 'Bar', 'dataObject': {} } ] # mock

    proc_unknown = lambda target, data_object, state: None

    mocker.patch('warhound.mk_null_unknown_processor')
    mocker.patch('warhound.mk_matchmaking')
    mocker.patch('warhound.mk_match')
    mocker.patch('warhound.mk_outcome')
    mocker.patch('warhound.maybe_proc_matchmaking')
    mocker.patch('warhound.maybe_proc_match')
    mocker.patch('warhound.maybe_proc_round')
    mocker.patch('warhound.maybe_proc_outcome')
    mocker.patch('warhound.process_single')

    result = warhound.process(obj, proc_unknown)

    assert warhound.mk_null_unknown_processor.call_count == 0
    assert warhound.mk_matchmaking.call_count == 1
    assert warhound.mk_match.call_count == 1
    assert warhound.mk_outcome.call_count == 1
    assert warhound.maybe_proc_matchmaking.call_count == 2
    assert warhound.maybe_proc_match.call_count == 2
    assert warhound.maybe_proc_round.call_count == 2
    assert warhound.maybe_proc_outcome.call_count == 2
    assert warhound.process_single.call_count == 2
    assert type(result) is warhound.Telemetry


def test_process_single_with_no_proc_unknown(mocker):
    obj = [ { 'cursor': 100, 'type': 'Foo', 'dataObject': {} },
            { 'cursor': 101, 'type': 'Bar', 'dataObject': {} },
            { 'cursor': 101, 'type': 'Bar', 'dataObject': {} } ] # mock

    mocker.patch('warhound.mk_null_unknown_processor')
    mocker.patch('warhound.mk_matchmaking')
    mocker.patch('warhound.mk_match')
    mocker.patch('warhound.mk_outcome')
    mocker.patch('warhound.maybe_proc_matchmaking')
    mocker.patch('warhound.maybe_proc_match')
    mocker.patch('warhound.maybe_proc_round')
    mocker.patch('warhound.maybe_proc_outcome')
    mocker.patch('warhound.process_single')

    result = warhound.process(obj)

    assert warhound.mk_null_unknown_processor.call_count == 1
    assert warhound.mk_matchmaking.call_count == 1
    assert warhound.mk_match.call_count == 1
    assert warhound.mk_outcome.call_count == 1
    assert warhound.maybe_proc_matchmaking.call_count == 3
    assert warhound.maybe_proc_match.call_count == 3
    assert warhound.maybe_proc_round.call_count == 3
    assert warhound.maybe_proc_outcome.call_count == 3
    assert warhound.process_single.call_count == 3
    assert type(result) is warhound.Telemetry

