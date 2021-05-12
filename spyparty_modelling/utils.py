from typing import Sequence, TypeVar

T = TypeVar('T')


def only(given_list: Sequence[T]) -> T:
    assert len(given_list) == 1
    return given_list[0]
