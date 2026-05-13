import time
import pytest

# Mark all tests in this file as performance tests
pytestmark = pytest.mark.performance

@pytest.mark.asyncio
async def test_create_1000_data_products_performance(sdk):
    """
    Performance test to time the creation of 1000 data products.
    """
    start_time = time.perf_counter()
    
    for i in range(1000):
        spec = {"domain": "performance", "name": f"dp_{i}"}
        await sdk.put_data_product(spec)
        
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    print(f"\nTime to create 1000 data products: {elapsed:.4f} seconds")
    
    # Verify that the 1000 data products were created
    dps = await sdk.list_data_products(domain="performance")
    assert len(dps) == 1000

    assert elapsed < 30, "Creation of 1000 data products must take less than 30 seconds" 

@pytest.mark.asyncio
async def test_create_1000_data_contracts_performance(sdk):
    """
    Performance test to time the creation of 1000 data contracts.
    """
    # Pre-create 1000 data products
    dp_ids = []
    for i in range(1000):
        dp = await sdk.put_data_product({"domain": "performance_dc", "name": f"dp_{i}"})
        dp_ids.append(dp["id"])

    start_time = time.perf_counter()
    
    for i, dp_id in enumerate(dp_ids):
        spec = {"version": "v1.0.0"}
        await sdk.put_data_contract(spec, dp_id=dp_id)
        
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    print(f"\nTime to create 1000 data contracts: {elapsed:.4f} seconds")

    assert elapsed < 30, "Creation of 1000 data contracts must take less than 30 seconds"
