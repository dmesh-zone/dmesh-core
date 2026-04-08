import argparse
from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.core.service import DMeshService

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
    
    # DataMeshService requires granular repositories (Sync)
    dp_repo = factory.get_data_product_repository()
    dc_repo = factory.get_data_contract_repository()
    service = DMeshService(dp_repo, dc_repo)
    
    # Define the Data Product
    spec = {"domain": "finance", "name": "ledger"}
    
    try:
        # Create Data Product
        dp = service.put_data_product(spec)
        db_name = "PostgreSQL" if args.db == "postgres_sync" else "In-Memory"
        print(f"Persisted to {db_name} (Sync): {dp.id}")
        print(f"Data Product Spec: {dp.specification}")
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
