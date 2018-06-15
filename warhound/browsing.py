from collections import defaultdict, namedtuple
from operator import itemgetter
from warhound import event


ONLY_CLASS = 0xf0000000


class NoSuchKindError(RuntimeError):
    pass


class NoSuchOccurrenceError(RuntimeError):
    pass


def build_dict_n_lookup(list_event):
    """
    Given a list of events, produce a dict with keys of type `Kind` (an enum
    value describing one kind of event). The associated value for each `Kind` is
    a list of indexes in the original list where the kind appears.

    Modifying the list will render this function's output incorrect.
    """
    
    dict_n_lookup = defaultdict(list)

    for index, _event in enumerate(list_event):
        _kind, _ = _event
        dict_n_lookup[_kind].append(index)

    return dict(dict_n_lookup.items())


def build_list_n(list_event):
    """
    Return a parallel list of 'n' values along side the list of events.

    The 'n' value of an event is its position in the sequence of same-kind
    events within the original list. It is not an intrinsic property of the
    event, but a contextual one.

    Modifying the list will render this function's output incorrect.
    """

    list_n = []
    counters = defaultdict(lambda: 0)

    for _event in list_event:
        _kind, _ = _event
        list_n.append(counters[_kind])
        counters[_kind] += 1

    return list_n


class Catalog(namedtuple('Catalog', ['dict_n_lookup', 'list_n', 'list_event'])):
    def __new__(cls, dict_n_lookup, list_n, list_event):
        return super().__new__(cls, dict_n_lookup, list_n, list_event)


def mk_catalog(list_event):
    return Catalog(build_dict_n_lookup(list_event), build_list_n(list_event),
                   list_event)


def locate(catalog, kind, n):
    try:
        for_kind = catalog.dict_n_lookup[kind]
    except KeyError:
        raise NoSuchKindError('locate: {0}'.format(kind))

    try:
        index = for_kind[n]
    except IndexError:
        raise NoSuchOccurrenceError('locate: {0}'.format(n))

    return index


def only_kind(catalog, mask):
    masked = mask & ONLY_CLASS

    def test_of_kind(item):
        _, event = item
        return masked & event.kind

    filtered = filter(test_of_kind, enumerate(catalog.list_event))
    indexes  = map(lambda a: a[0], filtered)

    return list(indexes)


def at(catalog, *indexes):
    """
    Return a subcatalog of events at provided indexes.
    """

    list_event = list(itemgetter(*indexes)(catalog.list_event))
    return mk_catalog(list_event)


def between(catalog, since, until):
    """
    Return a subcatalog of events between 'since' and 'until'.

    Keeping in line with python list idioms, 'since' is inclusive;
    'until' is exclusive.
    """

    return mk_catalog(catalog.list_event[since:until])


def since(catalog, index):
    """
    Return a subcatalog of events after 'index', inclusive.
    """

    return mk_catalog(catalog.list_event[index:])


def until(catalog, index):
    """
    Return a subcatalog of events before 'index', exclusive.
    """

    return mk_catalog(catalog.list_event[:index])
