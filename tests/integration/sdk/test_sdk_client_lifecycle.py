import uuid
from datetime import datetime
import pytest
from uuid import UUID
from typing import Any, List, Optional
from testcontainers.postgres import PostgresContainer
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk import AsyncSDK, DataProductValidationError, DataContractValidationError
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.persistency.postgres import PostgresSchema
from dmesh.sdk.core.id_generator import DefaultIDGenerator

# Fixtures are now provided by conftest.py

@pytest.fixture
def dp_repo(factory):
    """Short-cut to DataProduct repository."""
    return factory.get_data_product_repository()

@pytest.fixture
def dc_repo(factory):
    """Short-cut to DataContract repository."""
    return factory.get_data_contract_repository()


class PlatformXCustomIDGenerator(DefaultIDGenerator):
    def __init__(self):
        super().__init__()
        self.NAMESPACE_PLATFORM_X = uuid.uuid5(uuid.NAMESPACE_OID, "platform-x")

    def make_dp_id(self, spec: dict[str, Any]) -> uuid.UUID:
        domain = spec.get("domain", "unknown")
        name = spec.get("name", "unknown")
        
        custom_props = spec.get("customProperties", [])
        data_product_tier = AsyncSDK.get_custom_property_value(custom_props, "dataProductTier")
        if data_product_tier not in ["dataSource", "application"]: 
            domain_data_product_id = AsyncSDK.get_custom_property_value(custom_props, "domainDataProductId")
            # Expect domainDataProductId in custom properties
            if domain_data_product_id is None:
                raise ValueError(f"Domain data product ID not found in spec: {spec}")
            domain_data_product_unique_identifier = domain_data_product_id
        else:
            domain_data_product_unique_identifier = name
        return uuid.uuid5(self.NAMESPACE_PLATFORM_X, f"DataProduct/{domain}.{domain_data_product_unique_identifier}")

@pytest.mark.asyncio
async def test_sdk_client_example_usage(factory):
    """Simulates the CI/CD client usage of dmesh-sdk. 
    Assuming data product spec is minimalist containing only domain, name and outputPorts
    Assumes other information will be collected from other sources: e.g. repository_info and onboarding_info"""
    DOMAIN = "finance"
    DP1_BUSINESS_NAME = "SAP FI"
    DP1_TECHNICAL_NAME = "sap_fi"
    DP1_CATALOG_NAME = "dmesh-finance"
    DP1_SCHEMA_NAME = "landing_sap_fi"
    DP1_TABLE1_NAME = "accounting_document_line_items"
    DP1_DATA_SOURCE_TECH = "sap"
    DP1_DOMAIN_DP_ID = "0001"
    DATA_SOURCE_DATA_PRODUCT_NAME = f"{DP1_BUSINESS_NAME} data source"
    DP2_BUSINESS_NAME = "Account Receivables Ledger"
    DP2_TECHNICAL_NAME = "account_receivables_ledger"
    DP2_CATALOG_NAME = "dmesh-finance"
    DP2_SCHEMA_NAME = "curated_account_receivables_ledger"
    DP2_TABLE1_NAME = "customer_open_items"
    DP2_DOMAIN_DP_ID = "0002"

    # *** Custom ID generation for data products
    # initialise sdk here instead of fixture
    sdk = AsyncSDK(factory, id_generator=PlatformXCustomIDGenerator())
    
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
            "platform_data_product_id": sdk.id_generator.make_dp_id(
                {
                    "domain": DP1_DOMAIN_DP_ID,
                    "name": DP1_TECHNICAL_NAME, 
                    "customProperties": [
                        { "property": "dataProductTier", "value": "sourceAligned" },
                        { "property": "domainDataProductId", "value": DP1_DOMAIN_DP_ID}
                    ]
                }
                ),
            "domain_data_product_id": DP1_DOMAIN_DP_ID,
            "schema_name": DP1_SCHEMA_NAME,
            "data_engineer_group_name": f"{DOMAIN.upper()}_DATA_ENGINEER_{DP1_DOMAIN_DP_ID}",
            "data_analyst_group_name": f"{DOMAIN.upper()}_DATA_ANALYST_{DP1_DOMAIN_DP_ID}",
            "consumer_applications_group_name": f"{DOMAIN.upper()}_CONSUMER_APPLICATIONS_{DP1_DOMAIN_DP_ID}",
            "service_account_group_name": f"{DOMAIN.upper()}_DP_SERVICE_ACCOUNT_{DP1_DOMAIN_DP_ID}"
        },
        {
            "domain": DOMAIN,
            "data_product_business_name": DP2_BUSINESS_NAME,
            "data_product_technical_name": DP2_TECHNICAL_NAME,
            "platform_data_product_id": sdk.id_generator.make_dp_id(
                    {
                        "domain": DP2_DOMAIN_DP_ID,
                        "name": DP2_TECHNICAL_NAME, 
                        "customProperties": [
                            { "property": "dataProductTier", "value": "curated" },
                            { "property": "domainDataProductId", "value": DP2_DOMAIN_DP_ID}
                        ]
                    }
                ),
            "domain_data_product_id": DP2_DOMAIN_DP_ID,
            "schema_name": DP2_SCHEMA_NAME,
            "data_engineer_group_name": f"{DOMAIN.upper()}_DATA_ENGINEER_{DP2_DOMAIN_DP_ID}",
            "data_analyst_group_name": f"{DOMAIN.upper()}_DATA_ANALYST_{DP2_DOMAIN_DP_ID}",
            "consumer_applications_group_name": f"{DOMAIN.upper()}_CONSUMER_APPLICATIONS_{DP2_DOMAIN_DP_ID}",
            "service_account_group_name": f"{DOMAIN.upper()}_DP_SERVICE_ACCOUNT_{DP2_DOMAIN_DP_ID}"
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
        if not dp_spec.get("customProperties"):
            dp_spec["customProperties"] = []
        sdk.set_custom_property_value(dp_spec, "domainDataProductId", dp_info["domain_data_product_id"])
        
        # Add technicalProductName custom property to dp_spec (as this value will be useful to correlate businsess and technical names)
        sdk.set_custom_property_value(dp_spec, "technicalProductName", dp_info["domain_data_product_id"])
        # Enriching will populate default values for version and status, outputPort version and contractId, and portAdapter expansion
        enchiched_dp_spec = await sdk.enrich_data_product_spec(dp_spec)
        # Step 8-10: Create or update data product
        upserted_dp = await sdk.put_data_product(enchiched_dp_spec)
        # Step 11 Prepare Data Contract
        dc_spec = await sdk.enrich_data_contract(spec=None, dp_spec=upserted_dp)
        # Create host URL from workspace, catalog and schema
        catalog = dp_info["catalog"]
        schema = dp_info["schema"]
        host = f"https://dbc-12345678-90ab.workspace.cloud.databricks.com/explore/data/{catalog}/{schema}"
        dc_spec["servers"] = [
                {
                    "server": "Databricks",
                    "type": "databricks",
                    "environment": "dev",
                    "host": host,
                    "catalog": catalog,
                    "schema": schema 
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
        key = f"{databricks_server_info['catalog']}.{databricks_server_info['schema']}"
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

    # *** Data Usage Agreement flow ***
    # Step 1-2: Read AD Group information
    # Step 3: Update ad_group_memberships table
    APPLICATION_SERVICE_ACCOUNT = "FINANCE_360_APPLICATION_SERVICE_ACCOUNT"
    ad_group_memberships = [  
        {
            "group": f"{DOMAIN.upper()}_CONSUMER_APPLICATIONS_{DP1_DOMAIN_DP_ID}",
            "member": f"{DOMAIN.upper()}_DP_SERVICE_ACCOUNT_{DP2_DOMAIN_DP_ID}",
            "membershipStartDate": "2026-04-12"
        },
        {
            "group": f"{DOMAIN.upper()}_CONSUMER_APPLICATIONS_{DP2_DOMAIN_DP_ID}",
            "member": APPLICATION_SERVICE_ACCOUNT,
            "membershipStartDate": "2026-03-01"
        }
    ]
    APPLICATION_DATA_PRODUCT_NAME = "Finance 360 application"
    service_account_to_application_info_map = {
        APPLICATION_SERVICE_ACCOUNT: {"name": APPLICATION_DATA_PRODUCT_NAME, "applicationId": "2346"}
    }
    # Step 6: Prepare data product usage agreements
    # a. map service account to data product id (to identify consumer.dataProductIds)
    service_account_to_data_product_id = {}
    data_product_id_to_consumer_application_group = {}
    dc_list = await sdk.list_data_contracts()
    for dc in dc_list:
        for role in dc["roles"]:
            dp_id = sdk.get_custom_property_value(dc, "dataProductId")
            if "DP_SERVICE_ACCOUNT" in role["role"]:
                service_account_to_data_product_id[role["role"]] = dp_id
            if "CONSUMER_APPLICATIONS" in role["role"]:
                data_product_id_to_consumer_application_group[dp_id] = role["role"]
    memberships_in_consumer_application_group = {}
    for membership in ad_group_memberships:
        if membership["group"] not in memberships_in_consumer_application_group:
            memberships_in_consumer_application_group[membership["group"]] = [membership]
        else:
            memberships_in_consumer_application_group[membership["group"]].append(membership)
    # c. for each data product apply data usage agreements from consuming application membership info
    data_product_list = await sdk.list_data_products()
    for data_product in data_product_list:
        dp_memberships = []
        if data_product["id"] in data_product_id_to_consumer_application_group:
            dp_memberships = memberships_in_consumer_application_group.get(data_product_id_to_consumer_application_group[data_product["id"]], [])
        else:
            pass # Data Source data products data usage agreements managed automatically by default (see sdk.auto_data_source_dp_creation_upon_source_aligned_dp_creation)
        duas = []
        for membership in dp_memberships:
            if "DP_SERVICE_ACCOUNT" in membership["member"]:
                purpose = "Consuming data product"
                consumer_data_product_id = service_account_to_data_product_id.get(membership["member"])
            else:
                purpose = "Consuming application"
                # Create application dp using service_account_to_application_info_map
                application_dp_spec = {
                    "name": service_account_to_application_info_map.get(membership["member"])["name"],
                    "domain": data_product["domain"],
                    "customProperties": [{
                        "property": "dataProductTier",
                        "value": "application"
                    }]
                }
                # Step 7-8: create application data product (to show data product consumers)
                application_dp = await sdk.put_data_product(application_dp_spec)
                consumer_data_product_id = application_dp["id"]

            dua = {
                "info": {
                    "active": True,
                    "purpose": purpose,
                    "startDate": membership["membershipStartDate"]
                },
                "consumer": {
                    "dataProductId": consumer_data_product_id
                }
            }
            duas.append(dua)
        if len(duas) > 0:
            dp_to_patch = {
                "id": data_product["id"],
                "customProperties": [{
                    "property":"dataUsageAgreements",
                    "value": duas
                }]
            }
            # Step 9-10: Patch data products with data usage agreements
            patched_data_product = await sdk.patch_data_product(dp_to_patch)

    # Assert discovered data products data contracts and data usage agreements are as expected
    discover = await sdk.discover()
    assert len(discover) == 9
    
    # Maps for easy lookup
    dps_by_name = {dp["name"]: dp for dp in discover if dp.get("kind") == "DataProduct"}
    dcs_by_product = {dc["dataProduct"]: dc for dc in discover if dc.get("kind") == "DataContract"}
    dua_by_consuming_dp_id = {dua["consumer"]["dataProductId"] : dua for dua in discover if "dataUsageAgreementSpecification" in dua}
    
    def is_dp_tier(spec, tier):
        # Extract custom properties from spec
        custom_properties = spec.get("customProperties", [])
        # get dataProductTier custom property
        data_product_tier = [prop for prop in custom_properties if prop.get("property") == "dataProductTier"]
        # verify the dataProductTier custom property
        return len(data_product_tier) == 1 and data_product_tier[0]["value"] == tier

    # Check 4 data products exist
    # Source Aligned data product 
    assert DP1_BUSINESS_NAME in dps_by_name # SAP FI
    assert is_dp_tier(dps_by_name[DP1_BUSINESS_NAME], "sourceAligned") 
    # dataSource data product (auto generated to visualise SADP source) 
    data_source_data_product_name = DATA_SOURCE_DATA_PRODUCT_NAME
    assert data_source_data_product_name  in dps_by_name # "SAP FI data source"
    assert is_dp_tier(dps_by_name[data_source_data_product_name], "dataSource") 
    # Curated data product
    assert DP2_BUSINESS_NAME in dps_by_name # Accounts Receivables Ledger
    assert is_dp_tier(dps_by_name[DP2_BUSINESS_NAME], "curated") 
    # Application data product (created by client to visualise application consumers)
    assert APPLICATION_DATA_PRODUCT_NAME in dps_by_name # Finance 360
    assert is_dp_tier(dps_by_name[APPLICATION_DATA_PRODUCT_NAME], "application") 

    # Check 2 data contracts exist for sourceAligned and curated data products, and that these have schemas
    assert len(dcs_by_product) == 2
    assert DP1_BUSINESS_NAME in dcs_by_product
    assert "schema" in dcs_by_product[DP1_BUSINESS_NAME]
    assert DP2_BUSINESS_NAME in dcs_by_product
    assert "schema" in dcs_by_product[DP2_BUSINESS_NAME]

    # Check discovered dataUsageAgreementSpecifications 
    assert len(dua_by_consuming_dp_id) == 3 
    # dataSource->sourceAligned
    data_source_data_product_name = DATA_SOURCE_DATA_PRODUCT_NAME
    producer_dp_id = dps_by_name[data_source_data_product_name]["id"]
    consumer_dp_id = dps_by_name[DP1_BUSINESS_NAME]["id"]
    purpose = "Data Source replication"
    assert dua_by_consuming_dp_id[consumer_dp_id]["info"]["purpose"] == purpose
    assert dua_by_consuming_dp_id[consumer_dp_id]["provider"]["dataProductId"] == producer_dp_id
    assert dua_by_consuming_dp_id[consumer_dp_id]["consumer"]["dataProductId"] == consumer_dp_id
    # sourceAligned->curated
    producer_dp_id = dps_by_name[DP1_BUSINESS_NAME]["id"]
    consumer_dp_id = dps_by_name[DP2_BUSINESS_NAME]["id"]
    purpose = "Consuming data product"
    assert dua_by_consuming_dp_id[consumer_dp_id]["info"]["purpose"] == purpose
    assert dua_by_consuming_dp_id[consumer_dp_id]["provider"]["dataProductId"] == producer_dp_id
    assert dua_by_consuming_dp_id[consumer_dp_id]["consumer"]["dataProductId"] == consumer_dp_id
    # curated->application
    producer_dp_id = dps_by_name[DP2_BUSINESS_NAME]["id"]
    consumer_dp_id = dps_by_name[APPLICATION_DATA_PRODUCT_NAME]["id"]
    purpose = "Consuming application"
    assert dua_by_consuming_dp_id[consumer_dp_id]["info"]["purpose"] == purpose
    assert dua_by_consuming_dp_id[consumer_dp_id]["provider"]["dataProductId"] == producer_dp_id
    assert dua_by_consuming_dp_id[consumer_dp_id]["consumer"]["dataProductId"] == consumer_dp_id