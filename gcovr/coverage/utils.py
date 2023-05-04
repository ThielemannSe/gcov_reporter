from typing import TypeVar, Dict

_KeyType = TypeVar("_KeyType", str, int)
_ValueType = TypeVar("_ValueType")


def merge_dict(left: Dict[_KeyType, _ValueType], right: Dict[_KeyType, _ValueType]):
    merged = left.copy()

    for key, value in right.items():
        if key in left:
            item = left[key] + value
        else:
            item = value

        merged[key] = item

    return merged
