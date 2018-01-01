

class OneIndexedList(list):
    """
    This class exists to hold data which is one-indexed.

    It pads the zero index with None, and will behave incorrectly if this
    pad is ever removed. Suggested use is append-only.

    When iterating over this list, the first item will be discarded by the
    iterator.

    Consequently, if you want to enumerate with index, you should do:
        enumerate(one_indexed_list, start=1)
    """

    def __init__(self):
        super(OneIndexedList, self).append(None)


    def __getitem__(self, key):
        if key == 0:
            raise IndexError('IndexError: list index out of range')

        return super(OneIndexedList, self).__getitem__(key)


    def __iter__(self):
        return iter(self[1:])


    def __repr__(self):
        return repr(self[1:])

