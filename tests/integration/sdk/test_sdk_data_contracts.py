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
            await cur.execute("DROP TABLE IF EXISTS data_contracts CASCADE;")
            await cur.execute("DROP TABLE IF EXISTS data_products CASCADE;")
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

# Data Contract Tests
@pytest.mark.asyncio
async def test_create_dc_valid_minimum_input(sdk, dc_repo):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    assert dc["kind"] == "DataContract"
    assert dc["apiVersion"] == "v3.1.0"
    assert dc["status"] == "draft"
    assert dc["version"] == "v1.0.0"
    assert dc["domain"] == "d"
    assert dc["dataProduct"] == "n"
    
    # Assert persistency state
    persisted = await dc_repo.get(dc["id"])
    assert persisted is not None
    assert persisted.data_product_id == dp["id"]

@pytest.mark.asyncio
async def test_create_dc_single_dc_config(sdk, dc_repo, monkeypatch):
    # Single contract is the default behavior
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    dc1 = await sdk.put_data_contract({}, dp_id=dp["id"])
    assert dc1["status"] == "draft"

    dc2 = await sdk.put_data_contract({"status": "active"}, dp_id=dp["id"])
    assert dc1["id"] == dc2["id"]
    assert dc2["status"] == "active"
    assert dc2["domain"] == "d"

    # Verify we have 1 contract in repo (dc1)
    dcs = await dc_repo.list(dp_id=dp["id"])
    assert len(dcs) == 1
    
@pytest.mark.asyncio
async def test_create_dc_multiple_dc_config(factory, dc_repo, monkeypatch):
    # Multiple contracts allowed via environment variable
    monkeypatch.setenv("DMESH_SDK__SINGLE_DATA_CONTRACT_PER_PRODUCT", "false")
    # or via .toml
    # [sdk]
    # single_data_contract_per_product = true
    
    # Force reload of settings to pick up the new env var
    from dmesh.sdk.config import get_settings
    settings = get_settings(force_reload=True)
    
    # Create fresh SDK instance. It will pick up the 'false' value from env.
    sdk = AsyncSDK(factory, settings=settings)
    assert sdk.single_data_contract_per_product is False
    
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    dc1 = await sdk.put_data_contract({}, dp_id=dp["id"])
    dc2 = await sdk.put_data_contract({"status": "active"}, dp_id=dp["id"])
    
    assert dc1["id"] != dc2["id"]
    assert dc2["status"] == "active"
    assert dc2["domain"] == "d"
    
    # Verify we have 2 contracts in repo
    dcs = await dc_repo.list(dp_id=dp["id"])
    assert len(dcs) == 2
    
@pytest.mark.asyncio
async def test_create_dc_invalid_property(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    spec = {"invalid": "property"}
    with pytest.raises(DataContractValidationError) as exc:
        await sdk.put_data_contract(spec, dp_id=dp["id"])
    assert "Invalid Data Contract specification: Additional properties are not allowed ('invalid' was unexpected)" in str(exc.value)

@pytest.mark.asyncio
async def test_update_dc_valid_more_input(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    dc = await sdk.put_data_contract({"dataProduct": "n"}, dp_id=dp["id"])
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    
    # get dc
    updated_spec = await sdk.get_data_contract(id=dc["id"])
    updated_spec["dataProduct"] = "m"
    updated = await sdk.put_data_contract(updated_spec)
    
    assert updated["dataProduct"] == "m"

@pytest.mark.asyncio
async def test_patch_dc_valid_patching_schema(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    custom_property_1 = {"property": "p1", "value": "v1"}
    custom_property_2 = {"property": "p2", "value": "v2"}
    dc = await sdk.put_data_contract({
        "dataProduct": "n", 
        "status": "proposed",
        "customProperties": [custom_property_1]
    }, dp_id=dp["id"])
    
    assert dc["status"] == "proposed"
    assert dc["customProperties"] == [custom_property_1]

    schema_array = [{"name": "table", "properties": [{"name": "id", "logicalType": "string"}, {"name": "age", "logicalType": "integer"}]}]
    patching_input = {"id": dc["id"], "status": "active", "schema": schema_array, "customProperties": [custom_property_2]}
    patched = await sdk.patch_data_contract(patching_input)
    
    assert patched["status"] == "active"
    assert patched["schema"] == schema_array
    assert patched["customProperties"][0] == custom_property_1
    assert patched["customProperties"][1] == custom_property_2

@pytest.mark.asyncio
async def test_delete_dc_valid(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n", "version": "v"})
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    assert await sdk.delete_data_contract(dc["id"]) is True
    assert await sdk.get_data_contract(id=dc["id"]) is None

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