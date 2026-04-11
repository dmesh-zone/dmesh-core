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

@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.asyncio
async def test_sdk_client_full_lifecycle(sdk):
    """Simulates the full lifecycle of a dmesh-sdk client. 
    Assuming data product spec is minimalist containing only domain, name and outputPorts
    Assumes other information will be collected from other sources"""
    # TODO: (later) Consider how to delete data product and data contracts that have been decommissioned
    # Step 1. data product spec is provided with with minimal input provided: domain, finance and outputPorts
    dp_spec_input = {"domain": "finance", "name": "ledger", "outputPorts": [{"name": "ledger"}, {"name": "transactions"}]}
    # The client must infer the version and status of the data product, as these are required by the spec schema
    dp_spec_enriched = dp_spec_input.copy()
    # Set defaults for version and status if not provided
    if "version" not in dp_spec_enriched:
        dp_spec_enriched["version"] = "v1.0.0"
    if "status" not in dp_spec_enriched:
        dp_spec_enriched["status"] = "active"
    # Step 2: Get additional information from data product onboarding information
    # dp_onboarding_info = client.sdk.get_data_product_onboarding_information(dp_spec_input["domain"], dp_spec_input["name"])
    dp_onboarding_info = {
        "data_product_business_name": "",
        "data_product_technical_name": "",
        "platform_data_product_id": "123e4567-e89b-12d3-a456-426614174000",
        "domain_data_product_id": "0001",
        "schema_name": "",
        "data_engineer_group_name": "",
        "data_analyst_group_name": "",
        "consumer_applications_group_name": "",
        "service_account_group_name": ""
    }
    # TODO: (later) Step x: test retrived id conforms with deterministic dp id algorithm
    # TODO: Step x: Check if existing data product and data contracts
    # TODO: Step x: Create data product and data contracts if they don't exist
        # TODO: Step x.x: set dp id
        # TODO: Step x.x: set dp dataProductTier (sourceAligned)
        # TODO: Step x.x: set dp technology (databricks)
        # TODO: Step x.x: set dp domainDataProductId (0001)
        # TODO: Step x.x: create output port contractId
        # TODO: Step x.x: Create data product with all information (output port contract ids added later)
        # TODO: Step x.x: Prepare data contract with main server info including host, catalog and schema
        # TODO: Step x.x: Prepare data contract with roles including role (name) and acccess (read/write)
        # TODO: Step x.x: Prepare data contract with port adapter server info (e.g. location)
        # TODO: Step x.x: Create dataSource data product for data source (using sadp.dataSourceType as hint for source dp.technoloy) - Consider deterministic dp id input for dataSource data product
        # TODO: Step x.x: Create Data Usage Agreement Specification for source data product (to capture source dp to sadp connection)
        # TODO: Step x.x: Create application data product for applications (using curated_discover_and_observe.applications - derived from landing_iam.groups_and_members) - Consider deterministic dp id input for application data product
        # TODO: Step x.x: Create Data Usage Agreement Specification for application data product (to capture dp to application connections)
    # TODO: Step x: Update data product and data contracts if they exist
        # TODO: Step x.x: Check correct dp id
        # TODO: Step x.x: Check correct dp dataProductTier (sourceAligned)
        # TODO: Step x.x: Check correct dp technology (databricks)
        # TODO: Step x.x: Check correct dp domainDataProductId (0001)
        # TODO: Step x.x: Check correct output port contractId
        # TODO: Step x.x: Check data product has all information (output port contract ids added later)
        # TODO: Step x.x: Check data contract has main server info including host, catalog and schema
        # TODO: Step x.x: Check data contract has all roles including role (name) and acccess (read/write)
        # TODO: Step x.x: Check data contract has all port adapter server info (e.g. location)
        # TODO: Step x.x: Check dataSource data product for data source (using sadp.dataSourceType as hint for source dp.technoloy)
        # TODO: Step x.x: Check Data Usage Agreement Specification for source data product (to capture source dp to sadp connection)
        # TODO: Step x.x: Check application data product for applications (using curated_discover_and_observe.applications - derived from landing_iam.groups_and_members) - Consider deterministic dp id input for application data product
        # TODO: Step x.x: Check Data Usage Agreement Specification for application data product (to capture dp to application connections)
    # TODO: Step x: Create or Update schema for each output port (will execute periodically - unless dp.schemaAutoDiscovery:disabled)