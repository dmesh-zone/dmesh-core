import pytest
import os
import asyncio
from testcontainers.postgres import PostgresContainer
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.persistency.postgres import PostgresSchema

def pytest_addoption(parser):
    parser.addoption(
        "--external-db", action="store_true", default=False, help="Use external DB instead of testcontainers"
    )

class ExternalDB:
    """Mock object for PostgresContainer when using external DB."""
    def get_container_host_ip(self):
        return os.getenv("DMESH_DB__HOST", "localhost")
    
    def get_exposed_port(self, port):
        return os.getenv("DMESH_DB__PORT", "5432")
    
    @property
    def username(self):
        return os.getenv("DMESH_DB__USER", "postgres")
    
    @property
    def password(self):
        return os.getenv("DMESH_DB__PASSWORD", "postgres")
    
    @property
    def dbname(self):
        return os.getenv("DMESH_DB__NAME", "postgres")

@pytest.fixture(scope="session")
def postgres_container(request):
    """Start a PostgreSQL container or use external DB."""
    if request.config.getoption("--external-db"):
        yield ExternalDB()
    else:
        with PostgresContainer("postgres:16") as postgres:
            yield postgres

@pytest.fixture(scope="session", autouse=True)
async def setup_schema(postgres_container):
    """Create the database schema for tests."""
    import psycopg
    conn_string = (
        f"host={postgres_container.get_container_host_ip()} "
        f"port={postgres_container.get_exposed_port(5432)} "
        f"user={postgres_container.username} "
        f"password={postgres_container.password} "
        f"dbname={postgres_container.dbname}"
    )
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute(PostgresSchema.CREATE_TABLES)
        await conn.commit()

@pytest.fixture(autouse=True)
async def clean_database(postgres_container, setup_schema):
    """Ensure a clean database state for each integration test."""
    import psycopg
    conn_string = (
        f"host={postgres_container.get_container_host_ip()} "
        f"port={postgres_container.get_exposed_port(5432)} "
        f"user={postgres_container.username} "
        f"password={postgres_container.password} "
        f"dbname={postgres_container.dbname}"
    )
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
    from dmesh.sdk import AsyncSDK
    return AsyncSDK(factory)

@pytest.fixture
def dc_repo(factory):
    """Short-cut to DataContract repository."""
    return factory.get_data_contract_repository()
