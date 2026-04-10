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

# Data Product Tests
@pytest.mark.asyncio
async def test_create_dp_valid_minimum_input(sdk, dp_repo):
    spec = {"domain": "finance", "name": "ledger"}
    dp = await sdk.put_data_product(spec)
    
    # Assert return value
    assert dp["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"
    assert dp["apiVersion"] == "v1.0.0"
    assert dp["kind"] == "DataProduct"
    assert dp["status"] == "draft"
    assert dp["version"] == "v1.0.0"
    
    # Assert persistency state
    persisted = await dp_repo.get(UUID(dp["id"]))
    assert persisted is not None
    assert persisted.id == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert persisted.domain == "finance"
    assert persisted.name == "ledger"

@pytest.mark.asyncio
async def test_create_dp_valid_more_input(sdk):
    spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "status": "draft", "version": "v1.0.0"}
    dp = await sdk.put_data_product(spec, domain="finance", name="ledger")
    
    # Assert return value
    assert dp["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"

@pytest.mark.asyncio
async def test_create_dp_with_minimal_output_ports(sdk):
    spec = {"domain": "finance", "name": "ledger", "outputPorts": [{"name": "ledger"}, {"name": "transactions"}]}
    dp = await sdk.put_data_product(spec)
    
    # Assert return value
    assert dp["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert dp["apiVersion"] == "v1.0.0"
    assert dp["kind"] == "DataProduct"
    assert dp["status"] == "draft"
    assert dp["version"] == "v1.0.0"
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"
    assert dp["outputPorts"][0]["name"] == "ledger"
    assert dp["outputPorts"][0]["version"] == "v1"
    assert dp["outputPorts"][1]["name"] == "transactions"
    assert dp["outputPorts"][1]["version"] == "v1"

@pytest.mark.asyncio
async def test_create_dp_invalid_property(sdk):
    spec = {"domain": "finance", "name": "ledger", "invalid": "property"}
    with pytest.raises(DataProductValidationError) as exc:
        await sdk.put_data_product(spec)
    assert "Invalid Data Product specification: Additional properties are not allowed ('invalid' was unexpected)" in str(exc.value)

@pytest.mark.asyncio
async def test_update_dp_valid(sdk, dp_repo):
    spec = {"domain": "finance", "name": "ledger"}
    dp = await sdk.put_data_product(spec)
    dp_id = dp["id"]

    # get dp
    fetched = await sdk.get_data_product(id=dp_id)
    assert fetched["status"] == "draft"
    
    # update dp
    spec_to_update = fetched.copy()
    spec_to_update["status"] = "active"
    updated = await sdk.put_data_product(spec_to_update)
    
    # Assert return value
    assert updated["status"] == "active"
    
    # Assert persistency state
    persisted = await dp_repo.get(UUID(dp_id))
    assert persisted.specification["status"] == "active"

@pytest.mark.asyncio
async def test_update_dp_created_and_updated_at_are_set(sdk, dp_repo):
    spec1 = {"domain": "finance", "name": "ledger", "status": "draft"}
    spec2 = {"domain": "finance", "name": "ledger", "status": "proposed"}
    spec3 = {"domain": "finance", "name": "ledger", "status": "active"}
    dp1 = await sdk.put_data_product(spec1, include_metadata=True)
    assert dp1.created_at is not None
    assert dp1.updated_at is not None
    assert isinstance(dp1.created_at, datetime) 
    assert isinstance(dp1.updated_at, datetime) 
    assert dp1.created_at == dp1.updated_at
    dp2 = await sdk.put_data_product(spec2, include_metadata=True)
    assert dp2.created_at == dp1.created_at
    assert dp2.updated_at > dp1.updated_at
    dp3 = await sdk.put_data_product(spec3, include_metadata=True)
    assert dp3.created_at == dp1.created_at
    assert dp3.updated_at > dp2.updated_at

@pytest.mark.asyncio
async def test_update_dp_no_change_does_not_save(sdk, dp_repo):
    spec = {"domain": "finance", "name": "ledger", "outputPorts": [{"name": "ledger"}, {"name": "transactions"}]}
    dp1 = await sdk.put_data_product(spec, include_metadata=True)
    first_updated_at = dp1.updated_at

    # update dp
    dp2 = await sdk.put_data_product(spec, include_metadata=True)
    second_updated_at = dp2.updated_at
    assert second_updated_at == first_updated_at


@pytest.mark.asyncio
async def test_get_dp_by_id(sdk):
    spec = {"domain": "f", "name": "n"}
    created = await sdk.put_data_product(spec)
    fetched = await sdk.get_data_product(id=created["id"])
    
    assert isinstance(fetched, dict)
    assert fetched["id"] == created["id"]

@pytest.mark.asyncio
async def test_get_dp_by_domain_name(sdk):
    await sdk.put_data_product({"domain": "f", "name": "n"})
    fetched = await sdk.list_data_products(domain="f", name="n")
    
    assert fetched[0]["domain"] == "f"
    assert fetched[0]["name"] == "n"

@pytest.mark.asyncio
async def test_get_dp_not_found(sdk):
    assert await sdk.get_data_product(id="ba781283-1f14-5db2-a3f3-ce330da2c6dd") is None

@pytest.mark.asyncio
async def test_list_dps_filter(sdk):
    await sdk.put_data_product({"domain": "d1", "name": "n1"})
    await sdk.put_data_product({"domain": "d2", "name": "n2"})
    
    d1s = await sdk.list_data_products(domain="d1")
    assert len(d1s) == 1
    assert d1s[0]["domain"] == "d1"

@pytest.mark.asyncio
async def test_delete_dp_valid(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n", "version": "v"})
    assert await sdk.delete_data_product(dp["id"]) is True
    assert await sdk.get_data_product(id=dp["id"]) is None

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
    persisted = await dc_repo.get(UUID(dc["id"]))
    assert persisted is not None
    assert persisted.data_product_id == dp["id"]
    
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