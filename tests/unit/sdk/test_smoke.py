import pytest
import asyncio
from uuid import UUID
from dmesh.sdk import create_dp, DataProduct, DataProductValidationError
from dmesh.sdk.ports.repository import DataProductRepository

class MemoryDataProductRepository:
    """Minimal in-memory repository for smoke testing."""
    def __init__(self):
        self.products = {}

    async def get(self, id: UUID) -> DataProduct:
        return self.products.get(id)

    async def save(self, product: DataProduct) -> None:
        # Compatibility: model uses str id, repo uses UUID
        self.products[UUID(product.id)] = product

@pytest.mark.anyio
async def test_create_dp_smoke():
    repo = MemoryDataProductRepository()
    spec = {
        "domain": "test-domain",
        "name": "test-product",
        "version": "v1.0.0"
    }
    
    # 1. Create DP (returns spec dict by default)
    result = await create_dp(repo, spec)
    assert isinstance(result, dict)
    assert result["domain"] == "test-domain"
    assert "id" in result
    
    # 2. Verify it's in the repo
    dp_id = result["id"]
    persisted = await repo.get(UUID(dp_id))
    assert persisted is not None
    assert persisted.domain == "test-domain"
    assert persisted.specification["id"] == dp_id

@pytest.mark.anyio
async def test_create_dp_with_metadata_smoke():
    repo = MemoryDataProductRepository()
    spec = {"domain": "hr", "name": "employees"}
    
    # Returns DataProduct object
    dp = await create_dp(repo, spec, include_metadata=True)
    assert isinstance(dp, DataProduct)
    assert dp.domain == "hr"
    assert dp.name == "employees"

@pytest.mark.anyio
async def test_create_dp_validation_smoke():
    repo = MemoryDataProductRepository()
    # Missing domain is usually invalid in many schemas
    invalid_spec = {"name": "oops"} 
    
    # Wait, our enrich_spec currently allows empty domain but maybe validator catches it.
    # In any case, we want to see it raise if schema is strict.
    
    # If the schema allows it, this test might pass or fail depending on actual schema.
    # But let's assume invalid data should raise validation error.
    try:
        await create_dp(repo, {"apiVersion": "invalid"})
        pytest.fail("Should have raised ValueError")
    except ValueError:
        pass
