

class RoundEvent:
    __slots__ = ('player_id', 'champion_id', 'event_type', 'attrs')


    def __init__(self):
        self.player_id   = None
        self.champion_id = None
        self.event_type  = None
        self.attrs       = None


class DeathEvent:
    __slots__ = ('player_id', 'attrs')


    def __init__(self):
        self.player_id = None
        self.attrs     = None


def mk_empty_round_event():
    return RoundEvent()


def mk_empty_death_event():
    return DeathEvent()

