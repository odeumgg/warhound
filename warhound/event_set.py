from collections import namedtuple
from . import event


class EventSet(namedtuple('EventSet', ['list_event'])):
    def __new__(cls, list_event):
        return super().__new__(cls, list_event)


    def __len__(self):
        return len(self.list_event)


    def __iter__(self):
        return iter(self.list_event)


def mk(*args, **kwargs): 
    return EventSet(*args, **kwargs)


def from_list(list_evt_json):
    """
    Given a list of telemetry events, return a containing, sorted EventSet.
    """

    # We enforce sorting by cursor.
    list_event = []
    ordered    = sorted(list_evt_json, key=lambda evt_json: evt_json['cursor']) 

    for evt_json in ordered:
        list_event.append(event.from_json(evt_json))

    return mk(list_event)

