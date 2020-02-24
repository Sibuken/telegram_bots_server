from pydantic import BaseModel, ValidationError
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from typing import Optional


class AbstractValidator(object):
    def __init__(
        self,
        to_class,
        request_data: BaseModel,
        context: dict,
        extra: Optional[dict] = None,
    ):
        self.request_data = request_data
        self.context = context
        if extra is None:
            self.extra = {}
        else:
            self.extra = extra

        self.to_class = to_class
        self.validated_data = {}
        self.errors = []

    def is_valid(self):
        raise NotImplementedError

    def validate(self, values: dict) -> dict:
        raise NotImplementedError

    def _validate_fields(self):
        raise NotImplementedError

    def add_extra(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError


class BaseValidator(AbstractValidator):
    non_field_error = "non_field_error"

    def validate(self, values: dict) -> dict:
        return values

    def _validate_fields(self):
        new_data = {}
        for key, value in self.request_data.dict().items():
            method = getattr(self, f"validate_{key}", None)

            if method is None:
                new_data[key] = value
                continue

            try:
                value = method(value)
                new_data[key] = value
            except ValueError as er:
                self.errors.append({"key": er})

        return new_data

    def is_valid(self):
        new_data = self._validate_fields()
        self.validated_data = self.validate(new_data)
        if self.errors:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=self.errors)

    def add_extra(self):
        self.validated_data.update(self.extra)

    def build(self):
        self.add_extra()
        try:
            return self.to_class(**self.validated_data)
        except ValidationError as er:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=er.json())
