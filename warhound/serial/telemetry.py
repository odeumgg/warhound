
# This file contains routines for special event sets which contain events for
# only one match, aka telemetries.


def all_evt_class(event_set, mask):
    masked = mask & event.EVT_ONLY_CLASS

    def test_evt_class(pair):
        return masked & pair.evt_type

    return filter(test_evt_class, iter(event_set))


def all_evt_type(event_set, *list_evt_type):
    def test_evt_type(pair):
        return pair.evt_type in list_evt_type

    return filter(test_evt_type, iter(event_set))

