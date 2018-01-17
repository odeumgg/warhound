import pytest

from warhound import util


def test_one_indexed_list_len(mocker):
    result = util.mk_oil()
    result.append(1)

    assert len(result) == 1


def test_one_indexed_list_getitem(mocker):
    result = util.mk_oil()
    result.append('hai')

    assert result[1] == 'hai'


def test_one_indexed_list_getitem_on_zero(mocker):
    result = util.mk_oil()

    with pytest.raises(IndexError) as e_info:
        result[0]


def test_one_indexed_list_iter(mocker):
    result = util.mk_oil()
    result.append('hai')

    assert list(iter(result)) == ['hai']


def test_one_indexed_list_repr(mocker):
    result = util.mk_oil()
    result.append('hai')

    assert str(result) == str(['hai'])

