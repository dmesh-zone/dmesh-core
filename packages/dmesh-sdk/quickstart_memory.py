import asyncio
from dmesh.sdk import AsyncSDK, RepositoryFactory

async def main():
    # Initialize an In-Memory repository for testing
    factory = RepositoryFactory().create(db_type="memory")
    
    # Use the SDK as an asynchronous context manager
    async with AsyncSDK(factory) as sdk:
        # Register a data product (idempotent)
        dp_spec = {
            "domain": "finance",
            "name": "ledger"
        }

        dp = await sdk.put_data_product(dp_spec)
        stored_dp = await sdk.get_data_product(dp['id'])
        print(f"Registered Data Product ID: {stored_dp['id']}")
        print(f"Data Product: {stored_dp}")
        dc_spec = {}
        dc = await sdk.put_data_contract(dc_spec, stored_dp['id'])
        stored_dc = await sdk.get_data_contract(dc['id'])
        print(f"Registered Data Contract ID: {stored_dc['id']}")
        print(f"Data Contract: {stored_dc}")

if __name__ == "__main__":
    asyncio.run(main())