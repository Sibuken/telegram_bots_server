import os


def get_env_boolean(var_name, default_value=True):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


DEBUG = get_env_boolean("DEBUG")
ENVIRONMENT = os.getenv("ENVIRONMENT")
SENTRY_DSN = os.getenv("SENTRY_DSN")
ALLOW_HOST = os.getenv("ALLOW_HOST")


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_ADDRESS = f"redis://{REDIS_HOST}:{REDIS_PORT}"


POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
TORTOISE_DATABASE_URI = (
    f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)
