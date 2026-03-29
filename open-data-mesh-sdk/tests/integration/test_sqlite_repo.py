import os
import pytest
from open_data_mesh_sdk.persistency.sqlite import SQLiteRepository
from open_data_mesh_sdk.core.models import DataProduct

@pytest.fixture
def repo():
    db_path = "test_repo.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    r = SQLiteRepository(db_path)
    yield r
    
    if os.path.exists(db_path):
        os.remove(db_path)

def test_sqlite_dp_crud(repo):
    dp = DataProduct(id="test-id", specification={"name": "test", "domain": "d1", "apiVersion": "v1"})
    
    # Create
    created = repo.create_data_product(dp)
    assert created.id == "test-id"
    
    # Get
    fetched = repo.get_data_product("test-id")
    assert fetched.id == "test-id"
    assert fetched.specification["name"] == "test"
    
    # List
    items = repo.list_data_products(domain="d1")
    assert len(items) == 1
    assert items[0].id == "test-id"
    
    # Update
    dp.specification["name"] = "updated"
    updated = repo.update_data_product(dp)
    assert updated.specification["name"] == "updated"
    
    # Delete
    success = repo.delete_data_product("test-id")
    assert success is True
    assert repo.get_data_product("test-id") is None
