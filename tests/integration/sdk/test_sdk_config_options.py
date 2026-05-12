import pytest
from uuid import UUID
from testcontainers.postgres import PostgresContainer
from dmesh.sdk import AsyncSDK
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.persistency.postgres import PostgresSchema

# Fixtures are now provided by conftest.py


@pytest.mark.asyncio
async def test_sdk_auto_data_source_dp_created_upon_source_aligned_dp_creation(sdk):
    spec = {"domain": "finance", "name": "ledger", 
        "customProperties": [
            {"property": "dataProductTier", "value": "sourceAligned"},
            {"property": "dataSourceTechnology", "value": "sap"}
        ]
    }
    # Assert auto creation upon source aligned dp creation default configuration is true
    assert sdk.auto_data_source_dp_creation_upon_source_aligned_dp_creation == True

    dp = await sdk.put_data_product(spec)
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"

    expected_data_source_dp_name = dp["name"] + " data source"
    dp_list = await sdk.list_data_products(domain=dp["domain"], name=expected_data_source_dp_name)
    assert len(dp_list) == 1
    data_source_dp = dp_list[0]
    assert data_source_dp["name"] == "ledger data source"
    
    custom_properties = {p["property"]: p["value"] for p in data_source_dp["customProperties"]}
    assert custom_properties["dataProductTier"] == "dataSource"
    assert custom_properties["dataUsageAgreements"] == [{
        "info": {
            "active": True,
            "purpose": "Data Source replication"
        },
        "consumer": {"dataProductId": dp["id"]}
    }]
    assert custom_properties["technology"] == "sap"

@pytest.mark.asyncio
async def test_sdk_auto_data_source_dp_not_created_if_auto_data_source_dp_creation_is_disabled(sdk):
    spec = {"domain": "finance", "name": "ledger", 
        "customProperties": [
            {"property": "dataProductTier", "value": "sourceAligned"}
        ]
    }
    # Disable auto data source dp creation
    sdk.auto_data_source_dp_creation_upon_source_aligned_dp_creation = False 

    dp = await sdk.put_data_product(spec)
    dp_list = await sdk.list_data_products(domain=dp["domain"])
    # Should only have the one we created
    assert len(dp_list) == 1

@pytest.mark.asyncio
async def test_sdk_auto_data_source_dp_not_created_if_not_source_aligned(sdk):
    spec = {"domain": "finance", "name": "ledger", 
        "customProperties": [
            {"property": "dataProductTier", "value": "curated"}
        ]
    }
    assert sdk.auto_data_source_dp_creation_upon_source_aligned_dp_creation == True

    await sdk.put_data_product(spec)
    dp_list = await sdk.list_data_products(domain="finance")
    assert len(dp_list) == 1

@pytest.mark.asyncio
async def test_sdk_expand_port_adapters(sdk):
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
async def test_sdk_expand_port_adapters_disabled(sdk):
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

@pytest.mark.asyncio
async def test_sdk_enrich_output_ports(factory):
    sdk = AsyncSDK(factory)
    sdk.enrich_output_ports = True
    sdk.single_data_contract_per_product = True
    
    dp_spec = {
        "domain": "test",
        "name": "enrich_test",
        "outputPorts": [{"name": "port1"}]
    }
    dp = await sdk.put_data_product(dp_spec)
    
    port = dp["outputPorts"][0]
    assert "contractId" in port
    assert "version" in port
    assert port["version"] == "v1"

@pytest.mark.asyncio
async def test_sdk_auto_data_product_id_in_data_contract(sdk):
    # Test True (default)
    assert sdk.auto_data_product_id_in_data_contract is True
    dp = await sdk.put_data_product({"domain": "test", "name": "dp1"})
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    
    cp_dict = {prop["property"]: prop["value"] for prop in dc.get("customProperties", [])}
    assert cp_dict["dataProductId"] == dp["id"]

    # Test False
    sdk.auto_data_product_id_in_data_contract = False
    dc2 = await sdk.put_data_contract({}, dp_id=dp["id"])
    cp_dict2 = {prop["property"]: prop["value"] for prop in dc2.get("customProperties", [])}
    assert "dataProductId" not in cp_dict2

@pytest.mark.asyncio
async def test_sdk_single_data_contract_per_product(sdk, dc_repo):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    
    # Test True (default)
    sdk.single_data_contract_per_product = True
    dc1 = await sdk.put_data_contract({}, dp_id=dp["id"])
    dc2 = await sdk.put_data_contract({"status": "active"}, dp_id=dp["id"])
    
    assert dc1["id"] == dc2["id"]
    assert dc2["status"] == "active"
    
    dcs = await dc_repo.list(dp_id=UUID(dp["id"]))
    assert len(dcs) == 1

@pytest.mark.asyncio
async def test_sdk_multiple_data_contract_per_product(sdk, dc_repo):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    
    # Test False
    sdk.single_data_contract_per_product = False
    dc1 = await sdk.put_data_contract({}, dp_id=dp["id"])
    dc2 = await sdk.put_data_contract({"status": "active"}, dp_id=dp["id"])
    
    assert dc1["id"] != dc2["id"]
    
    dcs = await dc_repo.list(dp_id=UUID(dp["id"]))
    assert len(dcs) == 2

@pytest.mark.asyncio
async def test_sdk_multiple_data_contract_per_product_via_config(factory, dc_repo, monkeypatch):
    # Multiple contracts allowed via environment variable
    monkeypatch.setenv("DMESH_SDK__SINGLE_DATA_CONTRACT_PER_PRODUCT", "false")
    # Need to provide a dummy password because DatabaseSettings has it as a required field
    monkeypatch.setenv("DMESH_DB__PASSWORD", "dummy")
    
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
    
    # Verify we have 2 contracts in repo
    dcs = await dc_repo.list(dp_id=UUID(dp["id"]))
    assert len(dcs) == 2

@pytest.mark.asyncio
async def test_sdk_default_status(factory):
    sdk = AsyncSDK(factory)
    sdk.data_product_status_default = "pending"
    sdk.data_contract_status_default = "draft"
    
    dp = await sdk.put_data_product({"domain": "test", "name": "dp1"}, include_metadata=True)
    assert dp.specification["status"] == "pending"
    
    dc = await sdk.put_data_contract({"schema": []}, dp_id=str(dp.id), include_metadata=True)
    assert dc.specification["status"] == "draft"
