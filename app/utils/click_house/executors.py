try:
    from aiochclient import ChClient
except ImportError:
    pass


from typing import Union


async def create(client: ChClient, query: str, values: Union[list, tuple]):
    return await client.execute(query, values)


async def get_list(client: ChClient, query: str):
    return await client.fetch(query)


async def get_object(client: ChClient, query: str):
    return await client.fetchrow(query)


async def get_count(client: ChClient, query: str):
    count_query = f"""
    SELECT count() 
    FROM (
        {query}
    ) AS c_t
    """

    return await client.fetchval(count_query)


async def get_list_with_paginate(client: ChClient, query: str, limit: int, offset: int):
    paginate_query = f"""
    {query}
    LIMIT {limit}
    OFFSET {offset}
    """

    return await client.fetch(paginate_query)
