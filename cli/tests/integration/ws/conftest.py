"""Shared fixtures for WS integration tests.

Uses a Postgres testcontainer + FastAPI TestClient.
Each test function gets a clean database via the `db` fixture.
"""
import importlib.resources
import os
from unittest.mock import MagicMock, patch

import psycopg2
import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Postgres container — module-scoped (one container per test module)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pg():
    from testcontainers.postgres import PostgresContainer
    sql = (
        importlib.resources.files("dm.docker.open-data-mesh-db")
        .joinpath("init.sql")
        .read_text()
    )
    with PostgresContainer("postgres:16") as pg:
        conn = psycopg2.connect(
            host=pg.get_container_host_ip(),
            port=pg.get_exposed_port(5432),
            dbname=pg.dbname,
            user=pg.username,
            password=pg.password,
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.close()
        yield pg


# ---------------------------------------------------------------------------
# DB connection — function-scoped, flushes between tests
# ---------------------------------------------------------------------------

@pytest.fixture
def db(pg):
    """Return a psycopg2 connection with a clean database."""
    conn = psycopg2.connect(
        host=pg.get_container_host_ip(),
        port=pg.get_exposed_port(5432),
        dbname=pg.dbname,
        user=pg.username,
        password=pg.password,
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("DELETE FROM data_products")
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# FastAPI TestClient — module-scoped
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def ws(pg):
    os.environ["DB_HOST"] = pg.get_container_host_ip()
    os.environ["DB_PORT"] = str(pg.get_exposed_port(5432))
    os.environ["DB_USER"] = pg.username
    os.environ["DB_PASSWORD"] = pg.password
    os.environ["DB_NAME"] = pg.dbname

    import app.routers.data_products as dp_mod
    import app.routers.data_contracts as dc_mod
    import app.main as main_mod
    dp_mod._pool = None
    dc_mod._pool = None
    main_mod._pool = None

    from app.main import app as ws_app
    import app.odps_validator as validator_mod
    import app.routers.data_contracts as dc_router_mod

    # Mock schema validation to avoid real network calls
    dp_patcher = patch.object(validator_mod, "requests")
    dc_patcher = patch.object(dc_router_mod, "req_lib")

    def _dp_mock_get(url, **kwargs):
        m = MagicMock()
        if "v99.0.0" in url:
            m.status_code = 404
        else:
            m.status_code = 200
            m.json.return_value = {
                "type": "object",
                "additionalProperties": False,
                "required": ["apiVersion", "kind", "domain", "name", "version", "status", "id"],
                "properties": {
                    "apiVersion": {"type": "string"},
                    "kind": {"type": "string"},
                    "domain": {"type": "string"},
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "status": {"type": "string"},
                    "id": {"type": "string"}
                }
            }
        return m

    def _dc_mock_get(url, **kwargs):
        m = MagicMock()
        if "v99.0.0" in url:
            m.status_code = 404
        else:
            m.status_code = 200
            m.json.return_value = {
                "type": "object",
                "additionalProperties": False,
                "required": ["apiVersion", "kind", "status", "version", "id"],
                "properties": {
                    "apiVersion": {"type": "string"},
                    "kind": {"type": "string"},
                    "status": {"type": "string"},
                    "version": {"type": "string"},
                    "id": {"type": "string"}
                }
            }
        return m

    mock_dp = dp_patcher.start()
    mock_dp.get.side_effect = _dp_mock_get
    mock_dp.RequestException = Exception

    mock_dc = dc_patcher.start()
    mock_dc.get.side_effect = _dc_mock_get
    mock_dc.RequestException = Exception

    # Set base path for tests
    os.environ["WS_BASE_PATH"] = "odm"
    # Reload main to pick up env var
    import importlib
    importlib.reload(main_mod)
    from app.main import app as ws_app_reloaded

    yield TestClient(ws_app_reloaded)

    dp_patcher.stop()
    dc_patcher.stop()


def _schema_mock(schema: dict):
    m = MagicMock()
    m.status_code = 200
    m.json.return_value = schema
    return m


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def db_query(db, sql: str, params=None) -> list:
    """Execute a SELECT and return all rows as dicts."""
    with db.cursor() as cur:
        cur.execute(sql, params or [])
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def log(label: str, data):
    """Print labelled output for test reviewers."""
    import json
    if isinstance(data, (dict, list)):
        print(f"\n[{label}]\n{json.dumps(data, indent=2, default=str)}")
    else:
        print(f"\n[{label}] {data}")
