import pytest
from typing import Any
from dmesh.sdk import AsyncSDK
from dmesh.sdk.core.id_generator import set_generator, DefaultIDGenerator, IDGenerator
from dmesh.sdk.persistency.factory import RepositoryFactory

class DottedIDGenerator:
    """Custom ID generator that uses dot concatenation as requested."""
    def make_dp_id(self, spec: dict[str, Any]) -> str:
        domain = spec.get("domain", "unknown")
        name = spec.get("name", "unknown")
        return f"{domain}.{name}"

    def make_dc_id(self, spec: dict[str, Any]) -> str:
        domain = spec.get("domain", "unknown")
        data_product = spec.get("dataProduct", "unknown")
        return f"{domain}.{data_product}"

@pytest.fixture
async def factory():
    factory = RepositoryFactory().create(db_type="memory")
    yield factory

@pytest.fixture
async def sdk(factory):
    return AsyncSDK(factory)

@pytest.mark.asyncio
async def test_custom_id_generator_hook(factory):
    # 1. Create SDK with custom generator
    sdk = AsyncSDK(factory, id_generator=DottedIDGenerator())
    
    # 2. Create Data Product
    dp_spec = {"domain": "finance", "name": "ledger"}
    dp = await sdk.put_data_product(dp_spec)
    
    # Verify custom ID (domain.name)
    assert dp["id"] == "finance.ledger"
    
    # 3. Create Data Contract
    dc_spec = {}
    dc = await sdk.put_data_contract(dc_spec, dp_id=dp["id"])
    
    # Verify custom ID (domain.dataProduct)
    assert dc["id"] == "finance.ledger"

class CustomDPOnlyGenerator(DefaultIDGenerator):
    """Overrides only DP ID generation, uses default for DC."""
    def make_dp_id(self, spec: dict[str, Any]) -> str:
        return "manual-dp-id"

@pytest.mark.asyncio
async def test_product_id_generator_override(factory):
    # Create SDK with product ID override only
    sdk = AsyncSDK(factory, id_generator=CustomDPOnlyGenerator())
    
    # 1. DP uses custom logic
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    assert dp["id"] == "manual-dp-id"
    
    # 2. DC uses DEFAULT logic (UUID5)
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    import uuid
    uuid.UUID(dc["id"]) # Should be a valid UUID5

class CustomDCOnlyGenerator(DefaultIDGenerator):
    """Overrides only DC ID generation, uses default for DP."""
    def make_dc_id(self, spec: dict[str, Any]) -> str:
        return f"custom-dc-{spec.get('_dc_index')}"

@pytest.mark.asyncio
async def test_contract_id_generator_override(factory):
    # Create SDK with contract ID override only
    sdk = AsyncSDK(factory, id_generator=CustomDCOnlyGenerator())
    
    # 1. DP uses DEFAULT logic (UUID5)
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    import uuid
    uuid.UUID(dp["id"]) # Should be a valid UUID5
    
    # 2. DC uses custom logic
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    assert dc["id"] == "custom-dc-0"
