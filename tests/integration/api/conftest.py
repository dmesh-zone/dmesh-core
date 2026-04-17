import pytest
import os
import sys
import asyncio
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.persistency.postgres import PostgresSchema
import dmesh.api.dependencies

@pytest.fixture(scope="session")
def postgres_container():
    """Start a PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:16") as postgres:
        yield postgres

@pytest.fixture(scope="session", autouse=True)
async def setup_api_schema(postgres_container):
    """Create the database schema for tests."""
    import psycopg
    conn_string = f"host={postgres_container.get_container_host_ip()} port={postgres_container.get_exposed_port(5432)} user={postgres_container.username} password={postgres_container.password} dbname={postgres_container.dbname}"
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute("DROP TABLE IF EXISTS data_contracts CASCADE;")
            await cur.execute("DROP TABLE IF EXISTS data_products CASCADE;")
            await cur.execute(PostgresSchema.CREATE_TABLES)
        await conn.commit()

@pytest.fixture
async def api_factory(postgres_container):
    """Create a repository factory and patch it into the API dependencies."""
    factory = RepositoryFactory().create(
        db_type="postgres",
        pg_host=postgres_container.get_container_host_ip(),
        pg_port=postgres_container.get_exposed_port(5432),
        pg_user=postgres_container.username,
        pg_password=postgres_container.password,
        pg_db=postgres_container.dbname
    )
    await factory.open()
    
    # Manually patch the global factory instance in the API module
    original_factory = dmesh.api.dependencies._factory
    dmesh.api.dependencies._factory = factory
    
    yield factory
    
    await factory.close()
    dmesh.api.dependencies._factory = original_factory

@pytest.fixture
async def api_client(api_factory):
    """Provide an AsyncClient for the FastAPI app."""
    from dmesh.api.main import app
    # We use ASGITransport to talk directly to the app without a network port
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def clean_api_db(postgres_container):
    """Ensure a clean database state for each integration test."""
    import psycopg
    conn_string = f"host={postgres_container.get_container_host_ip()} port={postgres_container.get_exposed_port(5432)} user={postgres_container.username} password={postgres_container.password} dbname={postgres_container.dbname}"
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE TABLE data_contracts, data_products CASCADE;")
        await conn.commit()
    yield
