import pytest
from uuid import UUID
from typing import List, Optional
from testcontainers.postgres import PostgresContainer
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk import (
    create_dp, update_dp, get_dp, list_dps, delete_dp,
    create_dc, update_dc, patch_dc, get_dc, list_dcs, delete_dc,
    discover, DataProductValidationError, DataContractValidationError
)
from dmesh.sdk.persistency.factory import RepositoryFactory

@pytest.fixture(scope="session")
def postgres_container():
    """Start a PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session", autouse=True)
async def setup_schema(postgres_container):
    """Create the database schema for tests."""
    import psycopg
    conn_string = f"host={postgres_container.get_container_host_ip()} port={postgres_container.get_exposed_port(5432)} user={postgres_container.username} password={postgres_container.password} dbname={postgres_container.dbname}"
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS data_products (
                    id          UUID        PRIMARY KEY,
                    specification JSONB,
                    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    dp_domain   TEXT        GENERATED ALWAYS AS (specification->>'domain')  STORED,
                    dp_name     TEXT        GENERATED ALWAYS AS (specification->>'name')    STORED,
                    dp_version  TEXT        GENERATED ALWAYS AS (specification->>'version') STORED
                );

                CREATE UNIQUE INDEX IF NOT EXISTS uq_data_products_domain_name_version
                    ON data_products (dp_domain, dp_name, dp_version);

                CREATE TABLE IF NOT EXISTS data_contracts (
                    id              UUID        PRIMARY KEY,
                    data_product_id UUID        NOT NULL REFERENCES data_products(id) ON DELETE CASCADE,
                    specification   JSONB,
                    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
            """)
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
async def repos(postgres_container, setup_schema):
    """Create repositories using the test postgres container."""
    factory = RepositoryFactory().create(
        db_type="postgres",
        pg_host=postgres_container.get_container_host_ip(),
        pg_port=postgres_container.get_exposed_port(5432),
        pg_user=postgres_container.username,
        pg_password=postgres_container.password,
        pg_db=postgres_container.dbname
    )
    await factory.open()
    try:
        yield factory.get_data_product_repository(), factory.get_data_contract_repository()
    finally:
        await factory.close()

# Data Product Tests
@pytest.mark.asyncio
async def test_create_dp_valid_minimum_input(repos):
    dp_repo, _ = repos
    spec = {"domain": "finance", "name": "ledger"}
    dp = await create_dp(dp_repo, spec)
    
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
async def test_create_dp_valid_more_input(repos):
    dp_repo, _ = repos
    spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "status": "draft", "version": "v1.0.0"}
    dp = await create_dp(dp_repo, spec, domain="finance", name="ledger")
    
    # Assert return value
    assert dp["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"

@pytest.mark.asyncio
async def test_create_dp_invalid_property(repos):
    dp_repo, _ = repos
    spec = {"domain": "finance", "name": "ledger", "invalid": "property"}
    with pytest.raises(DataProductValidationError) as exc:
        await create_dp(dp_repo, spec)
    assert "Invalid Data Product specification: Additional properties are not allowed ('invalid' was unexpected)" in str(exc.value)

@pytest.mark.asyncio
async def test_update_dp_valid(repos):
    dp_repo, _ = repos
    spec = {"domain": "finance", "name": "ledger"}
    dp = await create_dp(dp_repo, spec)
    dp_id = dp["id"]

    # get dp
    fetched = await get_dp(dp_repo, id=dp_id)
    assert fetched["status"] == "draft"
    
    # update dp
    spec_to_update = fetched.copy()
    spec_to_update["status"] = "active"
    updated = await update_dp(dp_repo, spec_to_update)
    
    # Assert return value
    assert updated["status"] == "active"
    
    # Assert persistency state
    persisted = await dp_repo.get(UUID(dp_id))
    assert persisted.specification["status"] == "active"

@pytest.mark.asyncio
async def test_get_dp_by_id(repos):
    dp_repo, _ = repos
    spec = {"domain": "f", "name": "n"}
    created = await create_dp(dp_repo, spec)
    fetched = await get_dp(dp_repo, id=created["id"])
    
    assert isinstance(fetched, dict)
    assert fetched["id"] == created["id"]

@pytest.mark.asyncio
async def test_get_dp_by_domain_name(repos):
    dp_repo, _ = repos
    await create_dp(dp_repo, {"domain": "f", "name": "n"})
    fetched = await list_dps(dp_repo, domain="f", name="n")
    
    assert fetched[0]["domain"] == "f"
    assert fetched[0]["name"] == "n"

@pytest.mark.asyncio
async def test_get_dp_not_found(repos):
    dp_repo, _ = repos
    assert await get_dp(dp_repo, id="ba781283-1f14-5db2-a3f3-ce330da2c6dd") is None

@pytest.mark.asyncio
async def test_list_dps_filter(repos):
    dp_repo, _ = repos
    await create_dp(dp_repo, {"domain": "d1", "name": "n1"})
    await create_dp(dp_repo, {"domain": "d2", "name": "n2"})
    
    d1s = await list_dps(dp_repo, domain="d1")
    assert len(d1s) == 1
    assert d1s[0]["domain"] == "d1"

@pytest.mark.asyncio
async def test_delete_dp_valid(repos):
    dp_repo, _ = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n", "version": "v"})
    assert await delete_dp(dp_repo, dp["id"]) is True
    assert await get_dp(dp_repo, id=dp["id"]) is None

# Data Contract Tests
@pytest.mark.asyncio
async def test_create_dc_valid_minimum_input(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n"})
    dc = await create_dc(dc_repo, dp_repo, {}, dp_id=dp["id"])
    
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
async def test_create_dc_invalid_property(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n"})
    spec = {"invalid": "property"}
    with pytest.raises(DataContractValidationError) as exc:
        await create_dc(dc_repo, dp_repo, spec, dp_id=dp["id"])
    assert "Invalid Data Contract specification: Additional properties are not allowed ('invalid' was unexpected)" in str(exc.value)

@pytest.mark.asyncio
async def test_update_dc_valid_more_input(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n"})
    dc = await create_dc(dc_repo, dp_repo, {"dataProduct": "n"}, dp_id=dp["id"])
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    
    # get dc
    updated_spec = await get_dc(dc_repo, dc["id"])
    updated_spec["dataProduct"] = "m"
    updated = await update_dc(dc_repo, updated_spec)
    
    assert updated["dataProduct"] == "m"

@pytest.mark.asyncio
async def test_patch_dc_valid_patching_schema(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n"})
    custom_property_1 = {"property": "p1", "value": "v1"}
    custom_property_2 = {"property": "p2", "value": "v2"}
    dc = await create_dc(dc_repo, dp_repo, {
        "dataProduct": "n", 
        "status": "proposed",
        "customProperties": [custom_property_1]
    }, dp_id=dp["id"])
    
    assert dc["status"] == "proposed"
    assert dc["customProperties"] == [custom_property_1]

    schema_array = [{"name": "table", "properties": [{"name": "id", "logicalType": "string"}, {"name": "age", "logicalType": "integer"}]}]
    patching_input = {"id": dc["id"], "status": "active", "schema": schema_array, "customProperties": [custom_property_2]}
    patched = await patch_dc(dc_repo, patching_input)
    
    assert patched["status"] == "active"
    assert patched["schema"] == schema_array
    assert patched["customProperties"][0] == custom_property_1
    assert patched["customProperties"][1] == custom_property_2

@pytest.mark.asyncio
async def test_delete_dc_valid(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n", "version": "v"})
    dc = await create_dc(dc_repo, dp_repo, {}, dp_id=dp["id"])
    assert await delete_dc(dc_repo, dc["id"]) is True
    assert await get_dc(dc_repo, dc["id"]) is None

# Discovery Tests
@pytest.mark.asyncio
async def test_discover_by_id(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n", "version": "v"})
    await create_dc(dc_repo, dp_repo, {}, dp_id=dp["id"])
    
    results = await discover(dp_repo, dc_repo, dp_id=dp["id"])
    assert len(results) == 2 # 1 DP + 1 DC

@pytest.mark.asyncio
async def test_discover_by_domain_name(repos):
    dp_repo, dc_repo = repos
    dp = await create_dp(dp_repo, {"domain": "d", "name": "n", "version": "v"})
    await create_dc(dc_repo, dp_repo, {}, dp_id=dp["id"])
    
    results = await discover(dp_repo, dc_repo, domain="d", name="n")
    assert len(results) == 2

@pytest.mark.asyncio
async def test_discover_id_not_found(repos):
    dp_repo, dc_repo = repos
    results = await discover(dp_repo, dc_repo, dp_id="ba781283-1f14-5db2-a3f3-ce330da2c6dd")
    assert results == []
