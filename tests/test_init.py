import pytest
import os
import simplejson as json
import sys

cwd = os.getcwd()
sys.path.append(cwd)

import warhound

class TestClass():
    def setup(self):
        telemetry_path = os.path.join(cwd, 'telemetries','telemetry.json')
        with open(telemetry_path, 'rb') as telemetry_json:
                raw       = telemetry_json.read()
                self.telemetry = warhound.process(json.loads(raw))

    def test_not_none(self):
        assert self.telemetry is not None
        matchmaking,match,outcome = self.telemetry
        assert matchmaking is not None
        assert match is not None
        assert outcome is not None

    def test_round_finished(self):
        good_event = {'type' : 'Structures.RoundFinishedEvent'}
        bad_event = {'type' : 'My teammates are bad not me'}
        assert warhound.test_round_finished(good_event)
        assert not warhound.test_round_finished(bad_event)
