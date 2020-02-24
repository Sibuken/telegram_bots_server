import aioredis
from typing import Union, Any
import json


async def get_data_by_key(redis_pool: aioredis.Redis, key: str) -> Any:
    return await redis_pool.get(key)


async def get_int_data_by_key(redis_pool: aioredis.Redis, key: str) -> Union[int, None]:
    data = await get_data_by_key(redis_pool, key)
    if data is None:
        return None

    return int(data)


async def get_obj_data_by_key(
    redis_pool: aioredis.Redis, key: str
) -> Union[dict, None]:
    data = await get_data_by_key(redis_pool, key)
    if data is None:
        return None

    return json.loads(data)
