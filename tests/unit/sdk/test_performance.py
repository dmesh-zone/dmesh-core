import time
import pytest
from dmesh.sdk import AsyncSDK
from dmesh.sdk.persistency.factory import InMemoryRepositoryFactory

@pytest.mark.asyncio
async def test_create_1000_data_products_performance():
    """
    Performance test to time the creation of 100 data products using the SDK
    with an in-memory repository to measure pure SDK overhead.
    """
    factory = InMemoryRepositoryFactory()
    sdk = AsyncSDK(factory)
    
    start_time = time.perf_counter()
    
    for i in range(1000):
        spec = {"domain": "performance", "name": f"dp_{i}"}
        await sdk.put_data_product(spec)
        
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    print(f"\nTime to create 1000 data products (in-memory): {elapsed:.4f} seconds")
    
    # Verify that the 1000 data products were created
    dps = await sdk.list_data_products(domain="performance")
    assert len(dps) == 1000

@pytest.mark.asyncio
async def test_create_1000_data_contracts_performance():
    """
    Performance test to time the creation of 100 data contracts using the SDK
    with an in-memory repository to measure pure SDK overhead.
    """
    factory = InMemoryRepositoryFactory()
    sdk = AsyncSDK(factory)
    
    # Pre-create 1000 data products
    dp_ids = []
    for i in range(1000):
        dp = await sdk.put_data_product({"domain": "performance_dc", "name": f"dp_{i}"})
        dp_ids.append(dp["id"])

    start_time = time.perf_counter()
    
    for i, dp_id in enumerate(dp_ids):
        # Create 1 data contract per data product
        spec = {"version": "v1.0.0"}
        await sdk.put_data_contract(spec, dp_id=dp_id)
        
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    print(f"\nTime to create 1000 data contracts (in-memory): {elapsed:.4f} seconds")
