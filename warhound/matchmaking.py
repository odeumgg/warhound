

class QueueEvent:
    __slots__ = ('raw')


    def __init__(self):
        self.raw = None


class Matchmaking:
    __slots__ = ('dict_queue_event_by_player_id')


    def __init__(self):
        self.dict_queue_event_by_player_id = {}


def mk_queue_event():
    return QueueEvent()


def mk_matchmaking():
    return Matchmaking()


def process_queue_event(matchmaking, data, state):
    player_id = data['userId']

    queue_event     = mk_queue_event()
    queue_event.raw = data

    matchmaking.dict_queue_event_by_player_id[player_id] = queue_event

    return None


PROCESSOR_BY_EVENT_TYPE = \
    { 'com.stunlock.service.matchmaking.avro.QueueEvent': process_queue_event }

