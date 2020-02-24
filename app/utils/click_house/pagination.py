from pydantic import BaseModel
from starlette.requests import Request
from typing import Union, Any, List
from core import executors
import asyncio


class AbstractPagination(object):
    def __init__(self, request: Request, offset: int = 0, limit: int = 100):
        self.request = request
        self.offset = offset
        self.limit = limit
        self.query = None
        self.count = None
        self.list = []
        self.client = request.app.click_house_client

    async def get_count(self, **kwargs) -> int:
        raise NotImplementedError

    def get_next_url(self) -> Union[str, None]:
        raise NotImplementedError

    def get_previous_url(self) -> Union[str, None]:
        raise NotImplementedError

    async def get_list(self, **kwargs):
        raise NotImplementedError

    async def paginate(self, query: str, response_class, **kwargs):
        """

        :param query: query to click house
        :param response_class: serializer which return data
        :param kwargs:
        :return: object that should be returned as a response
        """

        raise NotImplementedError


class OffsetLimitPagination(AbstractPagination):
    async def get_count(self, **kwargs) -> int:
        """

        :param kwargs:
        :return: number of found records
        """

        self.count = await executors.get_count(self.client, self.query)
        return self.count

    def get_next_url(self) -> Union[str, None]:
        """

        :return: URL for next "page" of paginated results.
        """

        if self.offset + self.limit >= self.count:
            return None

        return str(
            self.request.url.include_query_params(
                limit=self.limit, offset=self.offset + self.limit
            )
        )

    def get_previous_url(self) -> Union[str, None]:
        """

        :return: URL for previous "page" of paginated results.
        """

        if self.offset <= 0:
            return None

        if self.offset - self.limit <= 0:
            return str(self.request.url.remove_query_params(keys=["offset"]))

        return str(
            self.request.url.include_query_params(
                limit=self.limit, offset=self.offset - self.limit
            )
        )

    async def get_list(self, **kwargs):
        self.list = await executors.get_list_with_paginate(
            self.client, self.query, self.limit, self.offset
        )
        return self.list

    async def paginate(self, query: str, **kwargs):
        """

        :param query: query to click house
        :param kwargs:
        :return: object that should be returned as a response
        """
        self.query = query

        count, list_result = await asyncio.gather(self.get_count(), self.get_list())
        return {
            "count": count,
            "next": self.get_next_url(),
            "previous": self.get_previous_url(),
            "result": list_result,
        }
