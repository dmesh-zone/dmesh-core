import asyncio
from dmesh.sdk import create_dp
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.config import get_settings

async def main():
    # Load settings from config service
    settings = get_settings()

    # Create a PostgreSQL repository factory using settings
    factory = RepositoryFactory().create_from_settings(settings)
    
    # Open the connection pool (Mandatory for async Postgres pool)
    await factory.open()
    
    try:
        repo = factory.get_data_product_repository()
        
        # Create Data Product (Requesting metadata to get an object with .id)
        dp = await create_dp(repo, {"domain": "marketing", "name": "analytics"})
        print(f"Created data product: {dp}")
    finally:
        # Close the connection pool
        await factory.close()

if __name__ == "__main__":
    import selectors
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))