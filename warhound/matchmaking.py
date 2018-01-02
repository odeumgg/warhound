

class Matchmaking:
    __slots__ = ()


    def __init__(self):
        pass


def mk_empty_matchmaking():
    return Matchmaking()


def process_queue_event(matchmaking, data, state):
    # TODO

    return None


PROCESSOR_BY_EVENT_TYPE = \
    {
        'com.stunlock.service.matchmaking.avro.QueueEvent':
            process_queue_event,
    }

