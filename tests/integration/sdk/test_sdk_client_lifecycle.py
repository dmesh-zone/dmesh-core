from dmesh.sdk.core.id_generator import make_dp_id
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
async def test_sdk_cicd_client(sdk):
    """Simulates the CI/CD client usage of dmesh-sdk. 
    Assuming data product spec is minimalist containing only domain, name and outputPorts
    Assumes other information will be collected from other sources: e.g. repository_info and onboarding_info"""
    # TODO: SDK to populate dpSpec outputPorts contractId and contractVersion
    DOMAIN = "finance"
    DP1_BUSINESS_NAME = "SAP FI"
    DP1_TECHNICAL_NAME = "sap_fi"
    DP1_SCHEMA_NAME = "landing_sap_fi"
    DP1_TABLE1_NAME = "accounting_document_line_items"
    DP1_DATA_SOURCE_TECH = "sap"
    DP1_DOMAIN_DP_ID = "0001"
    DP2_BUSINESS_NAME = "Account Receivables Ledger"
    DP2_TECHNICAL_NAME = "account_receivables_ledger"
    DP2_SCHEMA_NAME = "curated_account_receivables_ledger"
    DP1_TABLE2_NAME = "customer_open_items"
    DP2_DOMAIN_DP_ID = "0002"
    # Step 1-3: domain_data_product_repository_scan() 
    # repository_info = domain_data_product_repository_scan() 
    domain_repository_info = [
        {
            "domain": DOMAIN,
            "name": DP1_TECHNICAL_NAME, 
            "spec": { 
                "outputPorts": [ { "name": DP1_TABLE1_NAME}],
                "customProperties": [
                    { "property": "dataProductTier", "value": "sourceAligned" },
                    { "property": "dataSourceTechnology", "value": DP1_DATA_SOURCE_TECH}
                ]
            }
        },
        {
            "domain": DOMAIN,
            "name": DP2_TECHNICAL_NAME, 
            "spec": { 
                "outputPorts": [ { "name": DP1_TABLE2_NAME} ],
                "customProperties": [
                    { "property": "dataProductTier", "value": "curated" },
                    { "property": "portAdapters", "value": ["odata", "iceberg"] }
                ]
            }
        }
    ]
    # Step 4-5: Get data_product_onboarding information 
    dp_onboarding_info = [
        {
            "domain": DOMAIN,
            "data_product_business_name": DP1_BUSINESS_NAME,
            "data_product_technical_name": DP1_TECHNICAL_NAME,
            "platform_data_product_id": sdk.id_generator.make_dp_id({"domain": DP1_DOMAIN_DP_ID, "name": DP1_TECHNICAL_NAME}),
            "domain_data_product_id": DP1_DOMAIN_DP_ID,
            "schema_name": DP1_SCHEMA_NAME,
            "data_engineer_group_name": f"{DOMAIN.upper()}_DATA_ENGINEER_{DP1_DOMAIN_DP_ID}",
            "data_analyst_group_name": f"{DOMAIN.upper()}_DATA_ANALYST_{DP1_DOMAIN_DP_ID}",
            "consumer_applications_group_name": f"{DOMAIN.upper()}_CONSUMER_APPLICATIONS_{DP1_DOMAIN_DP_ID}",
            "service_account_group_name": f"{DOMAIN.upper()}_SERVICE_ACCOUNT_{DP1_DOMAIN_DP_ID}"
        },
        {
            "domain": DOMAIN,
            "data_product_business_name": DP2_BUSINESS_NAME,
            "data_product_technical_name": DP2_TECHNICAL_NAME,
            "platform_data_product_id": sdk.id_generator.make_dp_id({"domain": DP2_DOMAIN_DP_ID, "name": DP2_TECHNICAL_NAME}),
            "domain_data_product_id": DP2_DOMAIN_DP_ID,
            "schema_name": DP2_SCHEMA_NAME,
            "data_engineer_group_name": f"{DOMAIN.upper()}_DATA_ENGINEER_{DP2_DOMAIN_DP_ID}",
            "data_analyst_group_name": f"{DOMAIN.upper()}_DATA_ANALYST_{DP2_DOMAIN_DP_ID}",
            "consumer_applications_group_name": f"{DOMAIN.upper()}_CONSUMER_APPLICATIONS_{DP2_DOMAIN_DP_ID}",
            "service_account_group_name": f"{DOMAIN.upper()}_SERVICE_ACCOUNT_{DP2_DOMAIN_DP_ID}"
        }
    ]
    # Step 6: Combine repository and onboarding information
    # For each data product in the repository, merge in onboarding information for matching domain and data product (technical) name
    dp_spec_list = []
    for dp in domain_repository_info:
        for dp_onboarding in dp_onboarding_info:
            if dp["domain"] == dp_onboarding["domain"] and dp["name"] == dp_onboarding["data_product_technical_name"]:
                dp_spec_list.append({**dp, **dp_onboarding})

    # Prepare data products and data contracts and update them in dmesh-db for each data product in repository
    for dp_info in dp_spec_list:
        # Step 7: Prepare data product spec
        dp_spec = dp_info["spec"]
        dp_spec["domain"] = dp_info["domain"]
        dp_spec["name"] = dp_info["data_product_technical_name"]
        # Enriching will populate default values for version and status, outputPort version and contractId, and portAdapter expansion
        enchiched_dp_spec = await sdk.enrich_data_product_spec(dp_spec)
        # Step 8: Create or update data product
        upserted_dp = await sdk.put_data_product(enchiched_dp_spec)
        # TODO: sdk.autoDataSourceDpCreationUponSourceAlignedDpCreation
        # TODO: Step 11 Prepare Data Contract
        # TODO: Add data contract roles
        # TODO: Add data contract servers
        # TODO: Upsert Data Contract