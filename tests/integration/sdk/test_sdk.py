import pytest
from uuid import UUID
from typing import List, Optional
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk import (
    create_dp, update_dp, get_dp, list_dps, delete_dp,
    create_dc, update_dc, patch_dc, get_dc, list_dcs, delete_dc,
    discover, DataProductValidationError, DataContractValidationError
)

class AsyncMemoryDataProductRepository:
    def __init__(self):
        self.products = {}

    async def get(self, id: UUID) -> Optional[DataProduct]:
        return self.products.get(id)

    async def save(self, product: DataProduct) -> None:
        self.products[UUID(product.id)] = product

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        results = list(self.products.values())
        if domain: results = [p for p in results if p.domain == domain]
        if name: results = [p for p in results if p.name == name]
        return results

    async def delete(self, id: UUID) -> bool:
        if id in self.products:
            del self.products[id]
            return True
        return False

class AsyncMemoryDataContractRepository:
    def __init__(self):
        self.contracts = {}

    async def get(self, id: UUID) -> Optional[DataContract]:
        return self.contracts.get(id)

    async def save(self, contract: DataContract) -> None:
        self.contracts[UUID(contract.id)] = contract

    async def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        results = list(self.contracts.values())
        if dp_id: results = [c for c in results if c.data_product_id == dp_id]
        return results

    async def delete(self, id: UUID) -> bool:
        if id in self.contracts:
            del self.contracts[id]
            return True
        return False

@pytest.fixture
def repos():
    return AsyncMemoryDataProductRepository(), AsyncMemoryDataContractRepository()

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
