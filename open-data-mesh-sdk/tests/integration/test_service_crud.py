import os
import pytest
from unittest.mock import MagicMock, patch
from open_data_mesh_sdk.core.service import DataMeshService
from open_data_mesh_sdk.persistency.sqlite import SQLiteRepository
import open_data_mesh_sdk.core.validator as sdk_validator

@pytest.fixture
def service(tmp_path):
    db_path = str(tmp_path / "test_service.db")
    repo = SQLiteRepository(db_path)
    svc = DataMeshService(repo)
    
    # Mock validation requests per spec
    def _mock_get(url, **kwargs):
        m = MagicMock()
        m.status_code = 200
        m.json.return_value = {
            "type": "object",
            "additionalProperties": True, # Allow other properties for now in mock
            "required": ["apiVersion", "id"],
            "properties": {
                "apiVersion": {"type": "string"},
                "id": {"type": "string"}
            }
        }
        return m

    with patch.object(sdk_validator.requests, "get", side_effect=_mock_get):
        yield svc

def test_service_data_product_crud_idempotent(service):
    spec = {"domain": "finance", "name": "ledger"}
    
    # 1. Create (idempotent PUT)
    dp = service.put_data_product(spec)
    assert dp.domain == "finance"
    assert dp.name == "ledger"
    assert dp.specification["status"] == "draft"
    
    dp_id = dp.id
    
    # 2. Update (idempotent PUT)
    updated_spec = {**spec, "status": "active"}
    updated = service.put_data_product(updated_spec)
    assert updated.id == dp_id
    assert updated.specification["status"] == "active"
    
    # 3. List
    results = service.list_data_products(domain="finance")
    assert len(results) == 1
    assert results[0].id == dp_id
    
    results = service.list_data_products(domain="finance", name="ledger")
    assert len(results) == 1
    assert results[0].id == dp_id

    results = service.list_data_products(domain="finance", name="ledger", version="v1.0.0")
    assert len(results) == 1
    assert results[0].id == dp_id

    results = service.list_data_products(domain="nonexistent")
    assert len(results) == 0

    # 4. Get
    fetched = service.get_data_product(dp_id)
    assert fetched.id == dp_id
    
    # 5. Delete
    service.delete_data_product(dp_id)
    assert service.get_data_product(dp_id) is None

def test_service_data_contract_crud(service):
    # Setup parent DP
    dp = service.put_data_product({"domain": "finance", "name": "payments"})
    dp_id = dp.id
    
    dc_spec = {"apiVersion": "v1.0.0", "info": {"title": "Raw Payments"}}
    
    # 1. Create DC
    dc = service.put_data_contract(dp_id, dc_spec)
    assert dc.data_product_id == dp_id
    dc_id = dc.id
    
    # 2. Update DC
    updated_spec = {**dc_spec, "info": {"title": "Updated Payments"}, "id": dc_id}
    updated = service.put_data_contract(dp_id, updated_spec)
    assert updated.id == dc_id
    assert updated.specification["info"]["title"] == "Updated Payments"
    
    # 3. List DCs
    dcs = service.list_data_contracts(dp_id=dp_id)
    assert len(dcs) == 1
    assert dcs[0].id == dc_id
    
    # 4. Get DC
    fetched = service.get_data_contract(dc_id)
    assert fetched.id == dc_id
    
    # 5. Delete DC
    service.delete_data_contract(dc_id)
    assert service.get_data_contract(dc_id) is None
