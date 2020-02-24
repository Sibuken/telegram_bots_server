from fastapi import APIRouter, Depends, HTTPException
from core.request_serializers import UpdateSerializer
from core.bots import bots

bots_router = APIRouter()


@bots_router.post("/api/v1/bots/{token}/", tags=["bots.v1"])
async def bot_handler(token: str, update: UpdateSerializer):
    bot_class = bots.get(token)
    if bot_class is None:
        raise HTTPException(status_code=404, detail="Bot don't found")

    bot = bot_class(update)
    res = await bot.handle()
    return res
