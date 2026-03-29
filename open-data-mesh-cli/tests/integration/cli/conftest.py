"""Shared fixtures for CLI integration tests.

Uses the WS TestClient + CliRunner with all httpx calls proxied.
"""
import importlib.resources
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import psycopg2
import pytest
import yaml
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from dm.main import app as cli_app, CLI_NAME


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


@pytest.fixture
def db(pg):
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

    client = TestClient(ws_app)
    yield client

    dp_patcher.stop()
    dc_patcher.stop()


def _schema_mock(schema):
    m = MagicMock()
    m.status_code = 200
    m.json.return_value = schema
    return m


@pytest.fixture
def cli(pg, tmp_path):
    """CliRunner with config in tmp_path, configured to use Postgres repository in the test container."""
    config_path = tmp_path / "config.yaml"
    history_path = tmp_path / "history.yaml"
    from dm.put.config_reader import CONFIG_PATH
    from dm.put.history import HISTORY_PATH as HISTORY_MODULE_PATH
    
    # Configure the CLI to talk to the Postgres container directly
    # This was previously mocked with httpx to the TestClient
    config_dict = {
        "postgres": {
            "host": pg.get_container_host_ip(),
            "port": pg.get_exposed_port(5432),
            "user": pg.username,
            "password": pg.password,
            "dbname": pg.dbname,
        }
    }
    config_path.write_text(yaml.dump(config_dict))

    runner = CliRunner()
    
    # Mocking validation in the SDK as well
    import open_data_mesh_sdk.core.validator as sdk_validator
    
    def _mock_get(url, **kwargs):
        m = MagicMock()
        m.status_code = 200
        # Reduced schema for mocking
        m.json.return_value = {
            "type": "object",
            "additionalProperties": False,
            "required": ["apiVersion", "id"],
            "properties": {
                "apiVersion": {"type": "string"},
                "kind": {"type": "string"},
                "domain": {"type": "string"},
                "name": {"type": "string"},
                "version": {"type": "string"},
                "status": {"type": "string"},
                "id": {"type": "string"},
                "info": {"type": "object"} # Needed for DataContract tests
            }
        }
        return m

    with (
        patch("dm.put.config_reader.CONFIG_PATH", config_path),
        patch("dm.put.history.HISTORY_PATH", history_path),
        patch.object(sdk_validator.requests, "get", side_effect=_mock_get),
    ):
        yield runner, tmp_path, history_path


class _Wrap:
    def __init__(self, r):
        self._r = r
        self.status_code = r.status_code
        self.headers = r.headers

    def json(self):
        return self._r.json()


def _wrap(r):
    return _Wrap(r)


def db_query(db, sql, params=None):
    with db.cursor() as cur:
        cur.execute(sql, params or [])
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def run(cli_runner_tuple, *args):
    """Invoke CLI without prints."""
    runner, _, _ = cli_runner_tuple
    cmd = [str(a) for a in args]
    from dm.main import app as cli_app
    return runner.invoke(cli_app, cmd)


def dp_yaml(tmp_path, spec=None):
    if spec is None:
        spec = {
            "apiVersion": "v1.0.0",
            "kind": "DataProduct",
            "domain": "dom",
            "name": "name",
            "version": "v1.0.0",
            "status": "draft"
        }
    p = tmp_path / f"{spec.get('domain', 'dom')}_{spec.get('name', 'name')}.yaml"
    p.write_text(yaml.dump(spec))
    return p


def dc_yaml(tmp_path, name="dc", spec=None):
    if spec is None:
        spec = {"apiVersion": "v3.1.0"}
    p = tmp_path / f"{name}.yaml"
    p.write_text(yaml.dump(spec) if spec else "")
    return p
