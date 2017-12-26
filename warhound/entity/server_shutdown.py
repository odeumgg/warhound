

class ServerShutdown:
    __slots__ = ('match_duration_sec', 'reason', 'attrs')


    def __init__(self):
        self.match_duration_sec = None
        self.reason             = None
        self.attrs              = None


def mk_empty_server_shutdown():
    return ServerShutdown()

