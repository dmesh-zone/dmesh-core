from datetime import datetime
import pytest
from uuid import UUID
from typing import List, Optional
from testcontainers.postgres import PostgresContainer
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk import AsyncSDK, DataProductValidationError, DataContractValidationError
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.persistency.postgres import PostgresSchema

@pytest.fixture(scope="session")
def postgres_container():
    """Start a PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:16") as postgres:
        yield postgres

@pytest.fixture(scope="session", autouse=True)
async def setup_schema(postgres_container):
    """Create the database schema for tests."""
    import psycopg
    conn_string = f"host={postgres_container.get_container_host_ip()} port={postgres_container.get_exposed_port(5432)} user={postgres_container.username} password={postgres_container.password} dbname={postgres_container.dbname}"
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute(PostgresSchema.CREATE_TABLES)
        await conn.commit()

@pytest.fixture(autouse=True)
async def clean_database(postgres_container, setup_schema):
    """Ensure a clean database state for each integration test."""
    import psycopg
    conn_string = f"host={postgres_container.get_container_host_ip()} port={postgres_container.get_exposed_port(5432)} user={postgres_container.username} password={postgres_container.password} dbname={postgres_container.dbname}"
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE TABLE data_contracts, data_products CASCADE;")
        await conn.commit()
    yield

@pytest.fixture
async def factory(postgres_container, setup_schema):
    """Create a repository factory connected to the test database."""
    factory = RepositoryFactory().create(
        db_type="postgres",
        pg_host=postgres_container.get_container_host_ip(),
        pg_port=postgres_container.get_exposed_port(5432),
        pg_user=postgres_container.username,
        pg_password=postgres_container.password,
        pg_db=postgres_container.dbname
    )
    await factory.open()
    yield factory
    await factory.close()

@pytest.fixture
def sdk(factory):
    """Provide an AsyncSDK instance for tests."""
    return AsyncSDK(factory)

@pytest.fixture
def dp_repo(factory):
    """Short-cut to DataProduct repository."""
    return factory.get_data_product_repository()

@pytest.fixture
def dc_repo(factory):
    """Short-cut to DataContract repository."""
    return factory.get_data_contract_repository()

@pytest.mark.asyncio
async def test_discover_by_id(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n", "version": "v"})
    await sdk.put_data_contract({}, dp_id=dp["id"])
    
    results = await sdk.discover(dp_id=dp["id"])
    assert len(results) == 2 # 1 DP + 1 DC

@pytest.mark.asyncio
async def test_discover_by_domain_name(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n", "version": "v"})
    await sdk.put_data_contract({}, dp_id=dp["id"])
    
    results = await sdk.discover(domain="d", name="n")
    assert len(results) == 2

@pytest.mark.asyncio
async def test_discover_id_not_found(sdk):
    results = await sdk.discover(dp_id="ba781283-1f14-5db2-a3f3-ce330da2c6dd")
    assert results == []