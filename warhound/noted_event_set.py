from collections import defaultdict, namedtuple
from warhound import event


ONLY_CLASS = 0xf0000000


class OutOfBoundsError(RuntimeError):
    pass


class NotedEvent(namedtuple('NotedEvent', ['n', 'event'])):
    def __new__(cls, n, event):
        return super().__new__(cls, n, event)


def mk_noted_event(*args, **kwargs):
    return NotedEvent(*args, **kwargs)


class NotedEventSet(namedtuple('NotedEventSet', ['list_noted_event'])):
    """
    An event set is a simple list of events with accompanying state about their
    occurrence among like events. Something like this shoddy representation:

      Event (kind=A), n=0 # first event of kind A
      Event (kind=B), n=0 # first event of kind B
      Event (kind=C), n=0 # first event of kind C
      Event (kind=A), n=1 # second event of kind A
      Event (kind=A), n=2 # third event of kind A
      Event (kind=C), n=1 # second event of kind C

    Each list of 'n' values in a noted event set (scoped by kind) will be equal
    to `range(0, n)`, where 'n' is the total number of like events.
    """

    def __new__(cls, list_noted_event):
        return super().__new__(cls, list_noted_event)


    def __len__(self):
        return len(self.list_noted_event)


    def __iter__(self):
        return iter(self.list_noted_event)


def mk(*args, **kwargs):
    return NotedEventSet(*args, **kwargs)


def from_list(list_json):
    """
    Given a list of json events, return a containing, sorted NotedEventSet.
    """

    # We enforce sorting by cursor.
    list_noted_event = []
    ordered = sorted(list_json, key=lambda json: json['cursor'])
    lookup = defaultdict(lambda: 0)

    for json in ordered:
        _event = event.from_source_json(json)
        _noted_event = mk_noted_event(lookup[_event.kind], _event)
        list_noted_event.append(_noted_event)
        lookup[_event.kind] += 1

    return mk(list_noted_event)


def indexes_for_type(list_noted_event, *list_kind):
    """Make a list of indexes of a variable list of event kind, in order."""

    def test_kind(item):
        index, _noted_event = item
        n, (kind, _) = _noted_event
        return kind in list_kind

    filtered = filter(test_kind, enumerate(list_noted_event))
    indexes  = map(lambda a: a[0], filtered)

    return list(indexes)


def subset_between(noted_event_set, first, last):
    pass


def subset_before(noted_event_set, kind, maybe_n=None):
    """
    Return a new NotedEventSet with all events before the given type, exclusive.

    With `maybe_n`, define "before" in terms of the Nth occurrence of the
    event; otherwise, the first. This value is zero-indexed. The caller must
    ensure the Nth occurrence of the event exists.

    `maybe_n` can be negative, as with any other list, to position from the
    end of the occurrence of events.
    """

    n = maybe_n or 0
    indexes = indexes_for_type(noted_event_set.list_noted_event, kind)

    try:
        return mk(noted_event_set.list_noted_event[0:indexes[n]])
    except IndexError:
        template = 'subset_before: maybe_n={0}'
        raise OutOfBoundsError(template.format(maybe_n))


def subset_after(noted_event_set, kind, maybe_n=None):
    """
    Return a new NotedEventSet with all events after the given type, exclusive.

    With `maybe_n`, define "before" in terms of the Nth occurrence of the
    event; otherwise, the first. This value is zero-indexed. The caller must
    ensure the Nth occurrence of the event exists.

    `maybe_n` can be negative, as with any other list, to position from the
    end of the occurrence of events.
    """

    n = maybe_n or 0
    indexes = indexes_for_type(noted_event_set.list_noted_event, kind)

    try:
        return mk(noted_event_set.list_noted_event[indexes[n]+1:])
    except IndexError:
        template = 'subset_after: maybe_n={0}'
        raise OutOfBoundsError(template.format(maybe_n))
