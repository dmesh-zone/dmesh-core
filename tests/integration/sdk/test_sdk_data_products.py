from datetime import datetime
import pytest
from uuid import UUID
from typing import List, Optional
from testcontainers.postgres import PostgresContainer
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk import AsyncSDK, DataProductValidationError, DataContractValidationError
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.persistency.postgres import PostgresSchema

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
    assert dp["id"] == str(sdk.id_generator.make_dp_id(dp))
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"
    assert dp["apiVersion"] == "v1.0.0"
    assert dp["kind"] == "DataProduct"
    assert dp["status"] == sdk.data_product_status_default
    assert dp["version"] == "v1.0.0"
    
    # Assert persistency state
    persisted = await dp_repo.get(UUID(dp["id"]))
    assert persisted is not None
    assert persisted.id == sdk.id_generator.make_dp_id(dp)
    assert persisted.domain == "finance"
    assert persisted.name == "ledger"

@pytest.mark.asyncio
async def test_create_dp_valid_more_input(sdk):
    spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "status": "draft", "version": "v1.0.0"}
    dp = await sdk.put_data_product(spec, domain="finance", name="ledger")
    
    # Assert return value
    assert dp["id"] == str(sdk.id_generator.make_dp_id(dp))
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"

@pytest.mark.asyncio
async def test_create_dp_with_minimal_output_ports(sdk):
    spec = {"domain": "finance", "name": "ledger", "outputPorts": [{"name": "ledger"}, {"name": "transactions"}]}
    dp = await sdk.put_data_product(spec)
    
    # Assert return value
    assert dp["id"] == str(sdk.id_generator.make_dp_id(dp))
    assert dp["apiVersion"] == "v1.0.0"
    assert dp["kind"] == "DataProduct"
    assert dp["status"] == sdk.data_product_status_default
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
    dp_id = UUID(dp["id"])

    # get dp
    fetched = await sdk.get_data_product(id=dp_id)
    assert fetched["status"] == sdk.data_product_status_default
    
    # update dp
    spec_to_update = fetched.copy()
    spec_to_update["status"] = "proposed"
    updated = await sdk.put_data_product(spec_to_update)
    
    # Assert return value
    assert updated["status"] == "proposed"
    
    # Assert persistency state
    persisted = await dp_repo.get(dp_id)
    assert persisted.specification["status"] == "proposed"

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
async def test_enrich_dp_spec(sdk, dp_repo):
    input_spec = {"domain": "finance", "name": "ledger"}
    expected_enriched_spec = {
        "domain": "finance", 
        "name": "ledger", 
        "id": str(sdk.id_generator.make_dp_id(input_spec)), 
        "apiVersion": "v1.0.0", 
        "version": "v1.0.0", 
        "kind": "DataProduct", 
        "status": sdk.data_product_status_default
        }
    enriched_spec = await sdk.enrich_data_product_spec(input_spec)
    assert enriched_spec == expected_enriched_spec
    assert enriched_spec["domain"] == "finance"
    assert enriched_spec["name"] == "ledger"
    assert enriched_spec["id"] == str(sdk.id_generator.make_dp_id(enriched_spec))
    assert enriched_spec["apiVersion"] == "v1.0.0"
    assert enriched_spec["version"] == "v1.0.0"
    assert enriched_spec["kind"] == "DataProduct"
    assert enriched_spec["status"] == sdk.data_product_status_default

@pytest.mark.asyncio
async def test_patch_dp(sdk, dp_repo):
    spec = {
            "domain": "finance", 
            "name": "ledger", 
            "outputPorts": [{"name": "ledger"}, {"name": "transactions"}],
            "customProperties": [{
                "property":"dataProductTier",
                "value": "sourceAligned"
                }]
            }
    dp1 = await sdk.put_data_product(spec)

    # patch dp
    data_usage_agreement = {
        "info": {
            "active": True,
            "purpose": "Source aligned data product replication",
            "startDate": "2026-04-12"
        },
        "consumer": {
            "dataProductId": str(sdk.id_generator.make_dp_id({"domain": "hr", "name": "employees"}))
        }
    }
    dp2 = await sdk.patch_data_product({
        "status": "proposed",
        "customProperties": [{
            "property":"dataUsageAgreements",
            "value": [data_usage_agreement]
            }]
        }, id=UUID(dp1["id"]))
    # Check that outputPorts are preserved and both custom properties are present
    stored_dp = await dp_repo.get(UUID(dp2["id"]))
    dp3 = stored_dp.specification
    assert "outputPorts" in dp3
    # Assert custom properties in any order
    custom_props = dp3["customProperties"]
    props_dict = {p["property"]: p["value"] for p in custom_props}
    
    assert props_dict.get("dataProductTier") == "sourceAligned"
    assert props_dict.get("dataUsageAgreements") == [data_usage_agreement]

@pytest.mark.asyncio
async def test_get_dp_by_id(sdk):
    spec = {"domain": "f", "name": "n"}
    created = await sdk.put_data_product(spec)
    fetched = await sdk.get_data_product(id=UUID(created["id"]))
    
    assert isinstance(fetched, dict)
    assert str(fetched["id"]) == str(created["id"])

@pytest.mark.asyncio
async def test_get_dp_by_domain_name(sdk):
    await sdk.put_data_product({"domain": "f", "name": "n"})
    fetched = await sdk.list_data_products(domain="f", name="n")
    
    assert fetched[0]["domain"] == "f"
    assert fetched[0]["name"] == "n"

@pytest.mark.asyncio
async def test_get_dp_not_found(sdk):
    assert await sdk.get_data_product(id=UUID("ba781283-1f14-5db2-a3f3-ce330da2c6dd")) is None

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
    assert await sdk.delete_data_product(UUID(dp["id"])) is True
    assert await sdk.get_data_product(id=dp["id"]) is None

@pytest.mark.asyncio
async def test_validate_data_products(sdk):
    await sdk.put_data_product({"domain": "finance", "name": "ledger", "outputPorts": [{"name": "some-port"}]})
    
    # Temporarily set schema validation settings to None to avoid actual external file loading issues
    # But since we just want to test the wrapper method, we can test that it returns the validation object
    # The default validator with no schema should pass minimal dp.
    
    results = await sdk.validate_data_products(domain="finance")
    assert len(results) == 1
    assert results[0].domain == "finance"
    assert results[0].name == "ledger"
    assert results[0].valid is True
    assert results[0].error is None

@pytest.mark.asyncio
async def test_validate_data_products_invalid(sdk):
    spec = {
        "domain": "finance", 
        "name": "invalid-ledger",
        "outputPorts": [{"name": "some-port"}],
        "customProperties": [
            {"property": "dataProductTier", "value": "inexistent"}
        ]
    }
    await sdk.put_data_product(spec)
    
    from dmesh.sdk.config import get_settings
    settings = sdk.settings or get_settings()
    
    # Configure the SDK with the custom schema so that it validates the dataProductTier enum
    settings.sdk.custom_validation_data_product_schema = "examples/custom-validation/schemas/custom-odps-json-schema-v1.0.0.json"
    settings.sdk.custom_validation_properties_path = "examples/custom-validation/schemas/custom-properties"
    
    results = await sdk.validate_data_products(domain="finance", name="invalid-ledger")
    
    assert len(results) == 1
    assert results[0].domain == "finance"
    assert results[0].name == "invalid-ledger"
    assert results[0].valid is False
    assert results[0].error is not None
    assert "ERROR: Specification for data product invalid-ledger customProperty dataProductTier value has an invalid value" in results[0].error
    assert "inexistent" in results[0].error