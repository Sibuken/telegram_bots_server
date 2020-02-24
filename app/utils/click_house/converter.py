import datetime
from enum import Enum


def bool_converter(value: bool):
    return int(value)


def datetime_converter(value: datetime.datetime):
    return value.replace(tzinfo=None, microsecond=0)


def enum_converter(value: Enum):
    return value.value


def clear_data(value):
    if isinstance(value, bool):
        return bool_converter(value)

    if isinstance(value, Enum):
        return enum_converter(value)

    return value
