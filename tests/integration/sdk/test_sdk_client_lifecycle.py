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

@pytest.mark.asyncio
async def test_sdk_client_example_usage(sdk):
    """Simulates the CI/CD client usage of dmesh-sdk. 
    Assuming data product spec is minimalist containing only domain, name and outputPorts
    Assumes other information will be collected from other sources: e.g. repository_info and onboarding_info"""
    # TODO: Provide ID maker showing how to handle dataSource dp
    DOMAIN = "finance"
    DP1_BUSINESS_NAME = "SAP FI"
    DP1_TECHNICAL_NAME = "sap_fi"
    DP1_CATALOG_NAME = "dmesh-finance"
    DP1_SCHEMA_NAME = "landing_sap_fi"
    DP1_TABLE1_NAME = "accounting_document_line_items"
    DP1_DATA_SOURCE_TECH = "sap"
    DP1_DOMAIN_DP_ID = "0001"
    DP2_BUSINESS_NAME = "Account Receivables Ledger"
    DP2_TECHNICAL_NAME = "account_receivables_ledger"
    DP2_CATALOG_NAME = "dmesh-finance"
    DP2_SCHEMA_NAME = "curated_account_receivables_ledger"
    DP2_TABLE1_NAME = "customer_open_items"
    DP2_DOMAIN_DP_ID = "0002"
    # *** CI/CD commit flow ***
    # Step 1-3: domain_data_product_repository_scan() 
    # repository_info = domain_data_product_repository_scan() 
    domain_repository_info = [
        {
            "domain": DOMAIN,
            "name": DP1_TECHNICAL_NAME, 
            "catalog": DP1_CATALOG_NAME,
            "schema": DP1_SCHEMA_NAME,
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
            "catalog": DP2_CATALOG_NAME,
            "schema": DP2_SCHEMA_NAME,
            "spec": { 
                "outputPorts": [ { "name": DP2_TABLE1_NAME} ],
                "customProperties": [
                    { "property": "dataProductTier", "value": "curated" }
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
        dp_spec["name"] = dp_info["data_product_business_name"]
        # Add technical_product_name custom property to dp_spec
        dp_spec["customProperties"].append({"property": "technical_product_name", "value": dp_info["data_product_technical_name"]})
        # Enriching will populate default values for version and status, outputPort version and contractId, and portAdapter expansion
        enchiched_dp_spec = await sdk.enrich_data_product_spec(dp_spec)
        # Step 8-10: Create or update data product
        upserted_dp = await sdk.put_data_product(enchiched_dp_spec)
        # Step 11 Prepare Data Contract
        dc_spec = await sdk.enrich_data_contract(spec=None, dp_spec=upserted_dp)
        # TODO: Consider adding sdk support for data contract databricks servers
        dc_spec["servers"] = [
                {
                    "server": "Databricks",
                    "type": "databricks",
                    "environment": "dev",
                    "host": "https://dbc-12345678-90ab.workspace.cloud.databricks.com/explore/data/food_production/food_production_analytics",
                    "catalog": dp_info["catalog"],
                    "schema": dp_info["schema"]
                }
            ]
        # Add data contract roles
        dc_spec['roles'] = [
                {
                    "role": dp_info["data_analyst_group_name"],
                    "access": "read",
                },
                {
                    "role": dp_info["data_engineer_group_name"],
                    "access": "write",
                },
                {
                    "role": dp_info["consumer_applications_group_name"],
                    "access": "read",
                },
                {
                    "role": dp_info["service_account_group_name"],
                    "access": "write",
                }
            ]
        # Step 12-14: Upsert Data Contract
        upserted_dc = await sdk.put_data_contract(dc_spec, dp_id=upserted_dp["id"])
    discover = await sdk.discover()
    assert len(discover) == 6
    
    # Maps for easy lookup
    dps_by_name = {dp["name"]: dp for dp in discover if dp.get("kind") == "DataProduct"}
    dcs_by_product = {dc["dataProduct"]: dc for dc in discover if dc.get("kind") == "DataContract"}
    duas = [x for x in discover if "dataUsageAgreementSpecification" in x]

    # Check SADP and curated data products exist
    assert DP1_BUSINESS_NAME in dps_by_name # "SAP FI"
    assert DP2_BUSINESS_NAME in dps_by_name # "Account Receivables Ledger"

    # Check DP1_BUSINESS_NAME data source exists
    data_source_name = f"{DP1_BUSINESS_NAME} data source"
    assert data_source_name in dps_by_name
    data_source_dp = dps_by_name[data_source_name]

    # Check DP1_BUSINESS_NAME data source has a dataUsageAgreement custom property with SADP as consumer
    custom_props = {p["property"]: p["value"] for p in data_source_dp.get("customProperties", [])}
    assert "dataUsageAgreements" in custom_props
    agreements = custom_props["dataUsageAgreements"]
    assert len(agreements) > 0
    assert agreements[0]["consumer"]["dataProductId"] == dps_by_name[DP1_BUSINESS_NAME]["id"]

    # Check there is dataUsageAgreementSpecification node with data source dp as producer and SADP as consumer
    assert len(duas) == 1
    dua = duas[0]
    assert dua["provider"]["dataProductId"] == data_source_dp["id"]
    assert dua["consumer"]["dataProductId"] == dps_by_name[DP1_BUSINESS_NAME]["id"]

    # Check there is a DP2_BUSINESS_NAME data product
    assert DP2_BUSINESS_NAME in dps_by_name

    # Check there is a data contract for DP1_BUSINESS_NAME data product
    assert DP1_BUSINESS_NAME in dcs_by_product

    # Check there is a data contract for DP2_BUSINESS_NAME data product
    assert DP2_BUSINESS_NAME in dcs_by_product

    # *** Schema refresh flow ***
    # The following code would be executed by a Schema Discovery service
    # Step 1-2: Get all tables technical metadata via databricks unity catalog tables get endpoint 
    # https://docs.databricks.com/api/workspace/tables/get
    schema_technical_metadata_dict = {
        f"{DP1_CATALOG_NAME}.{DP1_SCHEMA_NAME}" : [
            {
                "name" : DP1_TABLE1_NAME,
                "columns": [
                    {"name": "id", "type_name": "string", "type_text": "string"},
                    {"name": "some_column", "type_name": "number", "type_text": "bigint"}
                ]
            }
        ],
        f"{DP2_CATALOG_NAME}.{DP2_SCHEMA_NAME}" : [
            {
                "name" : DP2_TABLE1_NAME,
                "columns": [
                    {"name": "id", "type_name": "string", "type_text": "string"},
                    {"name": "some_column", "type_name": "number", "type_text": "bigint"}
                ]
            }
        ]
    }
    data_contracts = await sdk.list_data_contracts()
    for data_contract in data_contracts:
        # Step 2: Convert technical metadata to data contract schema 
        databricks_server_info = data_contract["servers"][0]
        key = f"{databricks_server_info["catalog"]}.{databricks_server_info["schema"]}"
        tables_technical_metadata = schema_technical_metadata_dict.get(key)
        data_contract_schema = []
        for table in tables_technical_metadata:
            # Convert table technical metadata to data contract schema
            table_columns = []
            for column in table["columns"]:
                table_columns.append({
                    "name": column["name"],
                    "physicalName": column["name"],
                    "logicalType": column["type_name"],
                    "physicalType": column["type_text"]
                })
            # add schema to dc
            data_contract_schema.append({
                "name": table["name"], # this must match the dataProduct's port name that the contract relates to
                "physicalName": table["name"], # the physical name of the table in the data source
                "physicalType": "table", # this could be table or view depending on source and what discover service returns
                "properties": table_columns
            })
        # Step 4-5: Patch Data Contract
        schema_updated_dc = await sdk.patch_data_contract({"id": data_contract["id"], "schema": data_contract_schema})

    # TODO: *** Data Usage Agreement flow ***
    pass
