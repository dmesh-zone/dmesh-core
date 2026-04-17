import pytest
from typing import Any
import uuid
from dmesh.sdk import AsyncSDK
from dmesh.sdk.core.id_generator import set_generator, DefaultIDGenerator, IDGenerator
from dmesh.sdk.persistency.factory import RepositoryFactory

# Fixed namespace for custom test IDs
CUSTOM_NS = uuid.UUID("12345678-1234-5678-1234-567812345678")

class DottedIDGenerator:
    """Custom ID generator that returns UUIDs derived from dot concatenation."""
    def make_dp_id(self, spec: dict[str, Any]) -> uuid.UUID:
        domain = spec.get("domain", "unknown")
        name = spec.get("name", "unknown")
        return uuid.uuid5(CUSTOM_NS, f"{domain}.{name}")

    def make_dc_id(self, spec: dict[str, Any]) -> uuid.UUID:
        domain = spec.get("domain", "unknown")
        data_product = spec.get("dataProduct", "unknown")
        return uuid.uuid5(CUSTOM_NS, f"{domain}.{data_product}")

    def make_dua_id(self, spec: dict[str, Any]) -> uuid.UUID:
        provider_id = spec.get("provider", {}).get("dataProductId", "unknown")
        consumer_id = spec.get("consumer", {}).get("dataProductId", "unknown")
        return uuid.uuid5(CUSTOM_NS, f"{provider_id}->{consumer_id}")

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
    
    # Verify custom ID (uuid5 derived from domain.name)
    assert dp["id"] == str(uuid.uuid5(CUSTOM_NS, "finance.ledger"))
    
    # 3. Create Data Contract
    dc_spec = {}
    dc = await sdk.put_data_contract(dc_spec, dp_id=dp["id"])
    
    # Verify custom ID (uuid5 derived from domain.dataProduct)
    assert dc["id"] == str(uuid.uuid5(CUSTOM_NS, "finance.ledger"))

class CustomDPOnlyGenerator(DefaultIDGenerator):
    """Overrides only DP ID generation, uses default for DC."""
    def make_dp_id(self, spec: dict[str, Any]) -> uuid.UUID:
        return uuid.UUID("00000000-0000-0000-0000-000000000001")

@pytest.mark.asyncio
async def test_product_id_generator_override(factory):
    # Create SDK with product ID override only
    sdk = AsyncSDK(factory, id_generator=CustomDPOnlyGenerator())
    
    # 1. DP uses custom logic
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    assert dp["id"] == str(uuid.UUID("00000000-0000-0000-0000-000000000001"))
    
    # 2. DC uses DEFAULT logic (UUID5)
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    assert isinstance(dc["id"], str)

class CustomDCOnlyGenerator(DefaultIDGenerator):
    """Overrides only DC ID generation, uses default for DP."""
    def make_dc_id(self, spec: dict[str, Any]) -> uuid.UUID:
        return uuid.uuid5(CUSTOM_NS, f"custom-dc-{spec.get('_dc_index')}")

@pytest.mark.asyncio
async def test_contract_id_generator_override(factory):
    # Create SDK with contract ID override only
    sdk = AsyncSDK(factory, id_generator=CustomDCOnlyGenerator())
    
    # 1. DP uses DEFAULT logic (UUID5)
    dp = await sdk.put_data_product({"domain": "d", "name": "n"})
    assert isinstance(dp["id"], str)
    
    # 2. DC uses custom logic
    dc = await sdk.put_data_contract({}, dp_id=dp["id"])
    assert dc["id"] == str(uuid.uuid5(CUSTOM_NS, "custom-dc-0"))

@pytest.mark.asyncio
async def test_dua_id_generator_hook(factory):
    # 1. Create SDK with custom generator
    sdk = AsyncSDK(factory, id_generator=DottedIDGenerator())
    
    # 2. Prepare scenario for DUA expansion
    consumer_uuid = "00000000-0000-0000-0000-0000000000c1"
    provider_dp = await sdk.put_data_product({"domain": "p", "name": "pn", "customProperties": [
        {"property": "dataUsageAgreements", "value": [{"consumer": {"dataProductId": consumer_uuid}}]}
    ]})
    
    # 3. Discover (will trigger expansion and thus make_dua_id)
    results = await sdk.discover()
    
    # Verify DUA has custom ID
    duas = [r for r in results if "dataUsageAgreementSpecification" in r]
    assert len(duas) == 1
    expected_dua_id = uuid.uuid5(CUSTOM_NS, f"{provider_dp['id']}->{consumer_uuid}")
    assert duas[0]["id"] == str(expected_dua_id)
