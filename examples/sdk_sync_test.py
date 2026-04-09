import argparse
from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk import SyncSDK

def main():
    parser = argparse.ArgumentParser(description="Synchronous SDK Test")
    parser.add_argument(
        "--db", 
        choices=["memory_sync", "postgres_sync"], 
        default="memory_sync",
        help="Database type (memory_sync or postgres_sync)"
    )
    args = parser.parse_args()

    # Load settings (only strictly needed for postgres_sync, but good to have)
    settings = get_settings()

    # Create repository factory
    factory = RepositoryFactory().create_from_settings(settings, db_type=args.db)
    
    # Initialize Sync SDK with factory
    dmesh = SyncSDK(factory)
    
    # Define the Data Product
    spec = {"domain": "finance", "name": "ledger", "version": "v1.0.0"}
    
    try:
        # Register/Update Data Product (idempotent)
        dp = dmesh.put_data_product(spec, include_metadata=True)
        db_name = "PostgreSQL" if args.db == "postgres_sync" else "In-Memory"
        
        print(f"[{db_name}] Successfully upserted Data Product")
        print(f"ID: {dp.id}")
        print(f"Domain: {dp.domain}, Name: {dp.name}")
        
    except Exception as e:
        if args.db == "postgres_sync":
            print("\nERROR: Failed to connect to PostgreSQL.")
            print(">>> To run your postgres docker instance run:")
            print("> docker-compose up -d")
            print(f"Details: {e}")
        else:
            raise e

if __name__ == "__main__":
    main()
