import sys

from fastapi import FastAPI
from core import config, routes
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from tortoise.contrib.starlette import register_tortoise


version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


if not config.DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(config.SENTRY_DSN, environment=config.ENVIRONMENT)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
    app.add_middleware(SentryAsgiMiddleware)
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=config.ALLOW_HOST.split(",")
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)


for router in routes.routers:
    app.include_router(router)


register_tortoise(
    app, db_url=config.TORTOISE_DATABASE_URI, modules={"models": ["party_maker_bot.models"]}, generate_schemas=True
)
