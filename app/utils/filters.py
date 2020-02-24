from typing import NoReturn, Union
import datetime
from utils.operators import OPERATORS


class AbstractFilter(object):
    fields = []

    operators = OPERATORS

    def __init__(self, filters: dict):
        self.filters = filters
        self.cleaned_filters = []

    def split_filter(self, field_name: str, raw_filter: str) -> str:
        raise NotImplementedError("`parse_filters` need implement")

    def parse_filters(self) -> NoReturn:
        raise NotImplementedError("`parse_filters` need implement")

    def concatenate_filters(self) -> str:
        raise NotImplementedError("`concatenate_filters` need implement")

    def filter(self) -> str:
        raise NotImplementedError("`concatenate_filters` need implement")


class BaseFilter(AbstractFilter):
    def split_filter(
        self, condition: str, value: Union[str, int, datetime.datetime]
    ) -> Union[str, None]:
        split_data = condition.split("__")
        if len(split_data) != 2:
            return None

        field_name = split_data[0]
        condition_name = split_data[1]

        if (
            (field_name not in self.fields)
            or (value is None)
            or (condition_name not in self.operators)
        ):
            return None

        operator = self.operators[condition_name]

        return operator.to_sql(field_name, value)

    def parse_filters(self) -> NoReturn:
        for key, value in self.filters.items():
            cleaned_filter = self.split_filter(key, value)

            if cleaned_filter:
                self.cleaned_filters.append(cleaned_filter)

    def concatenate_filters(self) -> str:
        return " and ".join(self.cleaned_filters)

    def filter(self) -> str:
        self.parse_filters()

        result = self.concatenate_filters()
        if result:
            return f"WHERE {result}"
        else:
            return ""
