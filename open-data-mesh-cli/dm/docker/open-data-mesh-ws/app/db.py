import os
from psycopg2 import pool

_REQUIRED = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]

def _get_env(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        raise RuntimeError(f"Required environment variable '{key}' is not set.")
    return value

def get_pool():
    return pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=_get_env("DB_HOST"),
        port=int(_get_env("DB_PORT")),
        user=_get_env("DB_USER"),
        password=_get_env("DB_PASSWORD"),
        dbname=_get_env("DB_NAME"),
    )
