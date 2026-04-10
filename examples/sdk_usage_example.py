import asyncio
import selectors
from dmesh.sdk import AsyncSDK, RepositoryFactory, get_settings

async def main():
    # Load settings from config service
    settings = get_settings()

    # Create a PostgreSQL repository factory using settings
    factory = RepositoryFactory().create_from_settings(settings)
    
    # Open the connection pool (Mandatory for async Postgres pool)
    await factory.open()
    
    try:
        # Initialize AsyncSDK with the factory
        sdk = AsyncSDK(factory)
        
        # Upsert Data Product (idempotent)
        spec = {"domain": "marketing", "name": "analytics", "version": "v1.1.0"}
        dp = await sdk.put_data_product(spec, include_metadata=True)
        
        print(f"Upserted Data Product: {dp.id}")
        print(f"Current Status: {dp.specification.get('status')}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\n>>> Ensure your postgres instance is running:")
        print("> docker-compose up -d")
    finally:
        # Close the connection pool
        await factory.close()

if __name__ == "__main__":
    # Ensure correct loop factory for Windows if needed, though run() usually handles it
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))