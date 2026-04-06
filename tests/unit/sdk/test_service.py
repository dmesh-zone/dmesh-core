import pytest
from unittest.mock import patch
from dmesh.sdk.core.service import DataMeshService
from dmesh.sdk.persistency.in_memory import InMemoryRepository

@pytest.fixture
def service():
    repo = InMemoryRepository()
    return DataMeshService(repo)

@patch("dmesh.sdk.core.service.validate_spec")
def test_create_data_product(mock_validate, service):
    spec = {
        "apiVersion": "v1.0.0",
        "domain": "test",
        "name": "product-1",
        "version": "1.0.0"
    }
    dp = service.create_data_product(spec)
    assert dp.id is not None
    assert dp.domain == "test"
    assert dp.name == "product-1"
    assert dp.version == "1.0.0"
    mock_validate.assert_called_once()

@patch("dmesh.sdk.core.service.validate_spec")
def test_put_data_product_idempotent(mock_validate, service):
    # First creation
    spec = {
        "apiVersion": "v1.0.0",
        "domain": "sales",
        "name": "monthly",
        "description": "old"
    }
    dp1 = service.put_data_product(spec)
    
    # Second call should update
    spec_updated = {
        "apiVersion": "v1.0.0",
        "domain": "sales",
        "name": "monthly",
        "description": "new"
    }
    dp2 = service.put_data_product(spec_updated)
    
    assert dp1.id == dp2.id
    assert dp2.specification["description"] == "new"
    
    # Listing should show only one
    items = service.list_data_products()
    assert len(items) == 1

def test_create_data_contract_parent_not_found(service):
    spec = {"apiVersion": "v1.0.0", "name": "contract"}
    with pytest.raises(ValueError, match="Parent Data Product non-existent not found"):
        service.create_data_contract("non-existent", spec)

@patch("dmesh.sdk.core.service.validate_spec")
def test_data_contract_generation(mock_validate, service):
    # Setup Data Product
    dp = service.create_data_product({"apiVersion": "v1.0.0", "domain": "d1", "name": "n1"})
    
    # Create two contracts
    dc1 = service.create_data_contract(dp.id, {"apiVersion": "v1.0.0", "name": "c1"})
    dc2 = service.create_data_contract(dp.id, {"apiVersion": "v1.0.0", "name": "c2"})
    
    assert dc1.id != dc2.id
    assert dc1.data_product_id == dp.id
    assert dc2.data_product_id == dp.id
