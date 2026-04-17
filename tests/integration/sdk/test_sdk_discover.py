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
async def test_discover(sdk):
    ledger_table_schema = [
        {"name": "table", "properties": [
            {"name": "date", "logicalType": "timestamp"}, 
            {"name": "credit_amount", "logicalType": "number"},
            {"name": "debit_amount", "logicalType": "number"}
        ]}]
    employee_table_schema = [
        {"name": "table", "properties": [
            {"name": "id", "logicalType": "string"}, 
            {"name": "name", "logicalType": "string"}, 
            {"name": "department", "logicalType": "string"}
        ]}]
    employee_skills_table_schema = [
        {"name": "table", "properties": [
            {"name": "employee_id", "logicalType": "string"}, 
            {"name": "skill", "logicalType": "string"}
        ]}]
    dp_finance_ledger = await sdk.put_data_product({"domain": "finance", "name": "ledger", "outputPorts": [{"name": "ledger"}, {"name": "transactions"}]})
    dc_finance_ledger = await sdk.put_data_contract({"schema": ledger_table_schema}, dp_id=dp_finance_ledger["id"])

    dp_hr_employees = await sdk.put_data_product({"domain": "hr", "name": "employees", "outputPorts": [{"name": "employees"}]})
    dc_hr_employees = await sdk.put_data_contract({"schema": employee_table_schema}, dp_id=dp_hr_employees["id"])

    dp_employee_skills = await sdk.put_data_product({"domain": "hr", "name": "employee_skills", "outputPorts": [{"name": "employee_skills"}]})
    dc_employee_skills = await sdk.put_data_contract({"schema": employee_skills_table_schema}, dp_id=dp_employee_skills["id"])

    # Discover all domains and data products
    results = await sdk.discover()
    assert len(results) == 6
    assert dc_finance_ledger in results
    assert dp_finance_ledger in results
    assert dc_hr_employees in results
    assert dp_hr_employees in results
    assert dc_employee_skills in results
    assert dp_employee_skills in results

    # Discover all data products within a domain
    results = await sdk.discover(domain="hr")
    assert len(results) == 4
    assert dc_hr_employees in results
    assert dp_hr_employees in results
    assert dc_employee_skills in results
    assert dp_employee_skills in results

    # Discover one data product within a domain
    results = await sdk.discover(domain="hr", name="employees")
    assert len(results) == 2
    assert dc_hr_employees in results
    assert dp_hr_employees in results

@pytest.mark.asyncio
async def test_discover_id_not_found(sdk):
    results = await sdk.discover(dp_id=UUID("ba781283-1f14-5db2-a3f3-ce330da2c6dd"))
    assert results == []

@pytest.mark.asyncio
async def test_discover_expands_data_usage_agreement(sdk):
    consumer_dp = await sdk.put_data_product(
        {
            "domain": "finance", 
            "name": "ledger"
        }
    )
    provider_dp = await sdk.put_data_product(
        {
            "domain": "finance", 
            "name": "sap",
            "customProperties": [
                {
                    "property": "dataUsageAgreements",
                    "value": [
                        {
                            "info": {
                                "startDate": "2026-04-12",
                                "purpose": "Source aligned data product replication"
                            },
                            "consumer": {"dataProductId": consumer_dp["id"]}
                        }
                    ]
                }
            ]
        }
    )
    data_usage_agreement = {
        "dataUsageAgreementSpecification": "0.0.1",
        "info": {
            "active": True,
            "purpose": "Source aligned data product replication",
            "status": "approved",
            "startDate": "2026-04-12"
        },
        "provider": {
            "teamId": provider_dp["domain"],
            "outputPortId": "*",
            "dataProductId": provider_dp["id"]
        },
        "consumer": {
            "teamId": consumer_dp["domain"],
            "dataProductId": consumer_dp["id"]
        }
    }
    data_usage_agreement["id"] = str(sdk.id_generator.make_dua_id(data_usage_agreement))
    results = await sdk.discover()
    assert len(results) == 3
    assert provider_dp in results
    assert consumer_dp in results
    assert data_usage_agreement in results

    # Test missing startDate
    import copy
    provider_dp_no_start_date_spec = copy.deepcopy(provider_dp)
    provider_dp_no_start_date_spec["customProperties"][0]["value"][0]["info"].pop("startDate")
    await sdk.put_data_product(provider_dp_no_start_date_spec)
    
    dua_no_start_date = copy.deepcopy(data_usage_agreement)
    dua_no_start_date["info"]["startDate"] = sdk.dua_start_date_default 
    dua_no_start_date["id"] = str(sdk.id_generator.make_dua_id(dua_no_start_date))
    
    results = await sdk.discover()
    assert len(results) == 3
    assert dua_no_start_date in results

    # Test missing purpose
    provider_dp_no_purpose_spec = copy.deepcopy(provider_dp)
    provider_dp_no_purpose_spec["customProperties"][0]["value"][0]["info"].pop("purpose")
    # restore startDate if it was popped in previous test (but deepcopy from provider_dp which still has it)
    await sdk.put_data_product(provider_dp_no_purpose_spec)
    
    dua_no_purpose = copy.deepcopy(data_usage_agreement)
    dua_no_purpose["info"]["purpose"] = sdk.dua_purpose_default 
    # ID doesn't change since purpose is not in scheme, but let's be safe
    dua_no_purpose["id"] = str(sdk.id_generator.make_dua_id(dua_no_purpose))
    
    results = await sdk.discover()
    assert len(results) == 3
    assert dua_no_purpose in results
