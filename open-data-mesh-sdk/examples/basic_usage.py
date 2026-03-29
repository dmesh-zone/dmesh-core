import os
from open_data_mesh_sdk import DataMeshService, SQLiteRepository

def main():
    # Use a temporary SQLite database for the example
    db_path = "example_odm.db"
    
    # Clean up previous example run if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        
    print(f"Initializing SDK with SQLite at {db_path}...")
    repo = SQLiteRepository(db_path)
    service = DataMeshService(repo)
    
    # Define a Data Product Spec
    dp_spec = {
        "apiVersion": "v1.0.0",
        "kind": "DataProduct",
        "domain": "finance",
        "name": "revenue-report",
        "version": "1.0.0",
        "description": "Daily revenue reports for the finance domain"
    }
    
    # Create Data Product
    print("\nCreating Data Product...")
    dp = service.create_data_product(dp_spec)
    print(f"Successfully created Data Product with ID: {dp.id}")
    
    # Define a Data Contract Spec
    dc_spec = {
        "apiVersion": "v1.0.0",
        "kind": "DataContract",
        "name": "revenue-raw-schema",
        "description": "Validation schema for raw revenue events"
    }
    
    # Create Data Contract for the Data Product
    print("\nCreating Data Contract...")
    dc = service.create_data_contract(dp.id, dc_spec)
    print(f"Successfully created Data Contract with ID: {dc.id}")
    
    # List all data products
    print("\nListing all Data Products...")
    dps = service.list_data_products()
    for item in dps:
        print(f"- {item.domain}/{item.name} ({item.id})")
        
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    main()
