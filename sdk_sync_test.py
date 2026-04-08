from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.factory import RepositoryFactory
from dmesh.sdk.core.service import DMeshService

def main():
    # Load settings from config service
    settings = get_settings()

    # Create a synchronous PostgreSQL repository factory using settings
    factory = RepositoryFactory().create_from_settings(settings, db_type="postgres_sync")
    
    # DataMeshService requires granular repositories (Sync)
    dp_repo = factory.get_data_product_repository()
    dc_repo = factory.get_data_contract_repository()
    service = DMeshService(dp_repo, dc_repo)
    
    # Create Data Product (Synchronously)
    spec = {"domain": "sync-marketing", "name": "sync-analytics"}
    try:
        dp = service.put_data_product(spec)
        print(f"Persisted to Postgres (Sync): {dp.id}")
        print(f"Data Product Spec: {dp.specification}")
    except Exception as e:
        print("\nERROR: Failed to connect to PostgreSQL.")
        print(">>> Is your postgres docker instance running?")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()
