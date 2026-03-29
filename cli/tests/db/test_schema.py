"""
Schema integration and property-based tests for open-data-mesh-db.

Uses testcontainers to spin up a real postgres:16 container, applies init.sql,
and verifies schema correctness.
"""
import importlib.resources
import uuid

import psycopg2
import psycopg2.errors
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from testcontainers.postgres import PostgresContainer


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pg_conn():
    """Start a postgres:16 container, apply init.sql, yield a connection."""
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
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        yield conn
        conn.close()


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_data_products_columns_exist(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'data_products'
            """
        )
        cols = {row[0] for row in cur.fetchall()}
    expected = {"id", "specification", "created_at", "updated_at"}
    assert expected.issubset(cols), f"Missing columns: {expected - cols}"


def test_data_contracts_columns_exist(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'data_contracts'
            """
        )
        cols = {row[0] for row in cur.fetchall()}
    expected = {"id", "data_product_id", "specification", "created_at", "updated_at"}
    assert expected.issubset(cols), f"Missing columns: {expected - cols}"


def test_timestamp_defaults_set_on_insert(pg_conn):
    product_id = str(uuid.uuid4())
    with pg_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO data_products (id) VALUES (%s) RETURNING created_at, updated_at",
            (product_id,),
        )
        row = cur.fetchone()
    pg_conn.rollback()
    assert row[0] is not None, "created_at should not be null"
    assert row[1] is not None, "updated_at should not be null"


def test_cascade_delete_removes_contracts(pg_conn):
    product_id = str(uuid.uuid4())
    with pg_conn.cursor() as cur:
        cur.execute("INSERT INTO data_products (id) VALUES (%s)", (product_id,))
        for _ in range(2):
            cur.execute(
                "INSERT INTO data_contracts (id, data_product_id) VALUES (%s, %s)",
                (str(uuid.uuid4()), product_id),
            )
        cur.execute("DELETE FROM data_products WHERE id = %s", (product_id,))
        cur.execute("SELECT COUNT(*) FROM data_contracts WHERE data_product_id = %s", (product_id,))
        count = cur.fetchone()[0]
    pg_conn.rollback()
    assert count == 0, "Cascade delete should remove all associated contracts"


def test_fk_violation_on_invalid_data_product_id(pg_conn):
    bad_id = str(uuid.uuid4())
    with pytest.raises(psycopg2.errors.ForeignKeyViolation):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO data_contracts (id, data_product_id) VALUES (%s, %s)",
                (str(uuid.uuid4()), bad_id),
            )
    pg_conn.rollback()


# ---------------------------------------------------------------------------
# Property 2: Schema idempotency
# Feature: open-data-mesh-db, Property 2: Schema idempotency
# Validates: Requirements 3.1, 8.3
# ---------------------------------------------------------------------------

@given(n=st.integers(min_value=1, max_value=10))
@settings(max_examples=100, deadline=None)
def test_schema_idempotent(n):
    # Feature: open-data-mesh-db, Property 2: Schema idempotency
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
            for _ in range(n):
                cur.execute(sql)
            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name IN ('data_products','data_contracts')"
            )
            tables = {row[0] for row in cur.fetchall()}
        conn.close()
    assert tables == {"data_products", "data_contracts"}


# ---------------------------------------------------------------------------
# Property 3: PK uniqueness enforced
# Feature: open-data-mesh-db, Property 3: PK uniqueness enforced
# Validates: Requirements 4.2, 5.2
# ---------------------------------------------------------------------------

@given(dup_id=st.uuids())
@settings(max_examples=100)
def test_pk_uniqueness_enforced(pg_conn, dup_id):
    # Feature: open-data-mesh-db, Property 3: PK uniqueness enforced
    dup_id_str = str(dup_id)
    with pg_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO data_products (id) VALUES (%s)",
            (dup_id_str,),
        )
    with pytest.raises(psycopg2.errors.UniqueViolation):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO data_products (id) VALUES (%s)",
                (dup_id_str,),
            )
    pg_conn.rollback()


# ---------------------------------------------------------------------------
# Property 5: FK referential integrity
# Feature: open-data-mesh-db, Property 5: FK referential integrity
# Validates: Requirements 5.4, 6.1
# ---------------------------------------------------------------------------

@given(bad_id=st.uuids())
@settings(max_examples=100)
def test_fk_referential_integrity(pg_conn, bad_id):
    # Feature: open-data-mesh-db, Property 5: FK referential integrity
    with pytest.raises(psycopg2.errors.ForeignKeyViolation):
        with pg_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO data_contracts (id, data_product_id) VALUES (%s, %s)",
                (str(uuid.uuid4()), str(bad_id)),
            )
    pg_conn.rollback()


# ---------------------------------------------------------------------------
# Property 6: Cascade delete
# Feature: open-data-mesh-db, Property 6: Cascade delete
# Validates: Requirements 6.2
# ---------------------------------------------------------------------------

@given(contract_count=st.integers(min_value=1, max_value=20))
@settings(max_examples=100)
def test_cascade_delete(pg_conn, contract_count):
    # Feature: open-data-mesh-db, Property 6: Cascade delete
    product_id = str(uuid.uuid4())
    with pg_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO data_products (id) VALUES (%s)",
            (product_id,),
        )
        for _ in range(contract_count):
            cur.execute(
                "INSERT INTO data_contracts (id, data_product_id) VALUES (%s, %s)",
                (str(uuid.uuid4()), product_id),
            )
        cur.execute("DELETE FROM data_products WHERE id = %s", (product_id,))
        cur.execute("SELECT COUNT(*) FROM data_contracts WHERE data_product_id = %s", (product_id,))
        count = cur.fetchone()[0]
    pg_conn.rollback()
    assert count == 0
