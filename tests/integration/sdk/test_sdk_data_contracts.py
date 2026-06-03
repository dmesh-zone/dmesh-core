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

# Data Contract Tests
@pytest.mark.asyncio
async def test_dc_enrich_data_contract_spec_empty_spec(sdk, dc_repo):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    dc = await sdk.enrich_data_contract({}, dp_id=dp["id"])
    
    assert dc["id"] == str(sdk.id_generator.make_dc_id({**dc, "_dc_index": 0}))
    assert dc["kind"] == "DataContract"
    assert dc["apiVersion"] == "v3.1.0"
    assert dc["status"] == sdk.data_contract_status_default
    assert dc["version"] == "v1.0.0"
    assert dc["domain"] == "d"
    assert dc["dataProduct"] == "n"

@pytest.mark.asyncio
async def test_create_dc_valid_minimum_input(sdk, dc_repo):
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    
    assert dc["id"] == str(sdk.id_generator.make_dc_id({**dc, "_dc_index": 0}))
    assert dc["kind"] == "DataContract"
    assert dc["apiVersion"] == "v3.1.0"
    assert dc["status"] == sdk.data_contract_status_default
    assert dc["version"] == "v1.0.0"
    assert dc["domain"] == "d"
    assert dc["dataProduct"] == "n"
    
    # Assert persistency state
    persisted = await dc_repo.get(UUID(dc["id"]))
    assert persisted is not None
    assert persisted.data_product_id == UUID(dp["id"])

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
    assert dc["id"] == str(sdk.id_generator.make_dc_id({**dc, "_dc_index": 0}))
    
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
    # we expect custom_property_1 AND the auto-injected dataProductId
    assert any(p == custom_property_1 for p in dc["customProperties"])
    assert any(p.get("property") == "dataProductId" for p in dc["customProperties"])

    schema_array = [{"name": "table", "properties": [{"name": "id", "logicalType": "string"}, {"name": "age", "logicalType": "integer"}]}]
    patching_input = {"id": dc["id"], "status": "active", "schema": schema_array, "customProperties": [custom_property_2]}
    patched = await sdk.patch_data_contract(patching_input)
    
    assert patched["status"] == "active"
    assert patched["schema"] == schema_array
    assert any(p == custom_property_1 for p in patched["customProperties"])
    assert any(p == custom_property_2 for p in patched["customProperties"])
    assert any(p.get("property") == "dataProductId" for p in patched["customProperties"])

@pytest.mark.asyncio
async def test_delete_dc_valid(sdk):
    dp = await sdk.put_data_product({"domain": "d", "name": "n", "version": "v"})
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    assert await sdk.delete_data_contract(dc["id"]) is True
    assert await sdk.get_data_contract(id=dc["id"]) is None
