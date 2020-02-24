import datetime


class ToPython(object):
    @classmethod
    def to_python(cls, value):
        raise NotImplementedError


class DefaultToPython(ToPython):
    @classmethod
    def to_python(cls, value):
        return value


class StrToPython(ToPython):
    @classmethod
    def to_python(cls, value):
        value = value.replace(";", "")
        return "'{}'".format(value.translate(str.maketrans({"'": r"\'"})))


class IntToPython(ToPython):
    @classmethod
    def to_python(cls, value):
        return value


class DatetimeToPython(ToPython):
    @classmethod
    def to_python(cls, value):
        date = (
            value.astimezone(datetime.timezone.utc)
            .replace(tzinfo=None, microsecond=0)
            .isoformat()
        )
        return f"'{date}'"


class Operator(object):
    @staticmethod
    def to_format(value):
        if isinstance(value, int):
            format_class = IntToPython
        elif isinstance(value, datetime.datetime):
            format_class = DatetimeToPython
        elif isinstance(value, str):
            format_class = StrToPython
        else:
            format_class = DefaultToPython

        return format_class.to_python(value)

    def to_sql(self, field_name: str, value):
        raise NotImplementedError


class SimpleOperator(Operator):
    def __init__(self, sql_operator, sql_for_null=None):
        self._sql_operator = sql_operator
        self._sql_for_null = sql_for_null

    def to_sql(self, field_name, value):
        value = self.to_format(value)

        return f"({field_name} {self._sql_operator} {value})"


OPERATORS = {}


def register_operator(name, operator_class: Operator):
    OPERATORS[name] = operator_class


register_operator("exact", SimpleOperator("="))
register_operator("lt", SimpleOperator("<"))
register_operator("lte", SimpleOperator("<="))
register_operator("gt", SimpleOperator(">"))
register_operator("gte", SimpleOperator(">="))
