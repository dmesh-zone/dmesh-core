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
async def test_expand_port_adapters(sdk):
    dp_finance_ledger = await sdk.put_data_product(
        {
            "domain": "finance", 
            "name": "ledger", 
            "outputPorts": [
                    {
                        "name": "ledger"
                    },
                    {
                        "name": "transactions",
                        "customProperties": [
                            { "property": "portAdapters", "value": ["odata", "iceberg"] }
                        ]
                    }
                ]
        }
    )
    assert sdk.expand_port_adapters is True
    # assert dp_finance_ledger has 4 output ports: 1 ledger + 1 transactions + 2 adapted versions
    assert len(dp_finance_ledger["outputPorts"]) == 4
    
    output_ports_dictionary = {p["name"]: p for p in dp_finance_ledger["outputPorts"]}
    
    assert "ledger" in output_ports_dictionary
    assert "transactions" in output_ports_dictionary
    assert "transactions_iceberg" in output_ports_dictionary
    
    iceberg_port = output_ports_dictionary["transactions_iceberg"]
    adapted_from_iceberg = next((p["value"] for p in iceberg_port["customProperties"] if p["property"] == "adaptedFrom"), None)
    assert adapted_from_iceberg == "transactions"
    
    assert "transactions_odata" in output_ports_dictionary
    odata_port = output_ports_dictionary["transactions_odata"]
    adapted_from_odata = next((p["value"] for p in odata_port["customProperties"] if p["property"] == "adaptedFrom"), None)
    assert adapted_from_odata == "transactions"
    

@pytest.mark.asyncio
async def test_expand_port_adapters_disabled(sdk):
    sdk.expand_port_adapters = False
    dp_finance_ledger = await sdk.put_data_product(
        {
            "domain": "finance", 
            "name": "ledger", 
            "outputPorts": [
                    {
                        "name": "ledger"
                    },
                    {
                        "name": "transactions",
                        "customProperties": [
                            { "property": "portAdapters", "value": ["odata", "iceberg"] }
                        ]
                    }
                ]
        }
    )
    # assert dp_finance_ledger has 2 output ports (no expansion)
    assert len(dp_finance_ledger["outputPorts"]) == 2
    port_names = [p["name"] for p in dp_finance_ledger["outputPorts"]]
    assert "ledger" in port_names
    assert "transactions" in port_names
    assert "transactions_iceberg" not in port_names
    assert "transactions_odata" not in port_names