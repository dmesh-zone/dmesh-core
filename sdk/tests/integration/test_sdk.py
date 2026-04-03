import pytest
import os
from open_data_mesh_sdk import OpenDataMesh
from open_data_mesh_sdk.persistency.sqlite import SQLiteRepository
from open_data_mesh_sdk.core.models import DataProduct, DataContract

@pytest.fixture
def odm(tmp_path):
    db_path = str(tmp_path / "test_client.db")
    repo = SQLiteRepository(db_path)
    client = OpenDataMesh(repo)
    yield client

# Data Product Tests
def odm_create_dp_valid_test(odm):
    spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "status": "draft", "version": "v1.0.0"}
    dp = odm.create_dp(spec, domain="finance", name="ledger")
    
    # Assert return value
    assert dp.domain == "finance"
    assert dp.name == "ledger"
    assert dp.id is not None
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_product(dp.id)
    assert persisted is not None
    assert persisted.domain == "finance"
    assert persisted.name == "ledger"

def odm_update_dp_valid_test(odm):
    spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "domain": "dom", "name": "nam", "version": "v1.0.0"}
    dp = odm.create_dp(spec)
    dp_id = dp.id
    
    update_spec = {"id": dp_id, "status": "active", "domain": "dom", "name": "nam", "version": "v1.0.0", "apiVersion": "v1.0.0"}
    updated = odm.update_dp(update_spec)
    
    # Assert return value
    assert updated.specification["status"] == "active"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_product(dp_id)
    assert persisted.specification["status"] == "active"

def odm_get_dp_by_id_test(odm):
    spec = {"domain": "f", "name": "n", "version": "v"}
    created = odm.create_dp(spec)
    fetched = odm.get_dp(id=created.id)
    
    assert fetched.id == created.id
    
    # Verify it matches what's in repo
    persisted = odm._svc.repository.get_data_product(created.id)
    assert fetched.id == persisted.id

def odm_get_dp_by_domain_name_test(odm):
    odm.create_dp({"domain": "f", "name": "n", "version": "v1.0.0"})
    fetched = odm.get_dp(domain="f", name="n")
    
    assert fetched.domain == "f"
    assert fetched.name == "n"
    
    # Verify repo has it
    results = odm._svc.repository.list_data_products(domain="f", name="n")
    assert len(results) == 1
    assert results[0].id == fetched.id

def odm_get_dp_not_found_test(odm):
    assert odm.get_dp(id="missing") is None

def odm_list_dps_filter_test(odm):
    odm.create_dp({"domain": "d1", "name": "n1", "version": "v1.0.0"})
    odm.create_dp({"domain": "d2", "name": "n2", "version": "v1.0.0"})
    
    d1s = odm.list_dps(domain="d1")
    assert len(d1s) == 1
    assert d1s[0].domain == "d1"
    
    # Verify repo state
    all_repo = odm._svc.repository.list_data_products()
    assert len(all_repo) == 2

def odm_delete_dp_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    assert odm.delete_dp(dp.id) is True
    
    # Assert return value
    assert odm.get_dp(id=dp.id) is None
    
    # Assert persistency state
    assert odm._svc.repository.get_data_product(dp.id) is None

# Data Contract Tests
def odm_create_dc_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    dc = odm.create_dc({"info": {"title": "c"}}, dp_id=dp.id)
    
    assert dc.data_product_id == dp.id
    assert dc.id is not None
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_contract(dc.id)
    assert persisted is not None
    assert persisted.data_product_id == dp.id

def odm_update_dc_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    dc = odm.create_dc({"info": {"title": "c"}}, dp_id=dp.id)
    
    update_spec = {"id": dc.id, "info": {"title": "updated"}, "apiVersion": "v3.1.0"}
    updated = odm.update_dc(update_spec)
    
    assert updated.specification["info"]["title"] == "updated"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_contract(dc.id)
    assert persisted.specification["info"]["title"] == "updated"

def odm_get_dc_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    dc = odm.create_dc({}, dp_id=dp.id)
    fetched = odm.get_dc(dc.id)
    
    assert fetched.id == dc.id
    
    # Verify repo
    persisted = odm._svc.repository.get_data_contract(dc.id)
    assert persisted.id == fetched.id

def odm_list_dcs_by_domain_name_test(odm):
    dp = odm.create_dp({"domain": "finance", "name": "ledger", "version": "v1"})
    odm.create_dc({"info": {"title": "c1"}}, dp_id=dp.id)
    odm.create_dc({"info": {"title": "c2"}}, dp_id=dp.id)
    
    dcs = odm.list_dcs(domain="finance", dp_name="ledger")
    assert len(dcs) == 2
    
    # Verify repo
    repo_dcs = odm._svc.repository.list_data_contracts(dp_id=dp.id)
    assert len(repo_dcs) == 2

def odm_delete_dc_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    dc = odm.create_dc({}, dp_id=dp.id)
    assert odm.delete_dc(dc.id) is True
    
    # Assert return value
    assert odm.get_dc(dc.id) is None
    
    # Assert persistency state
    assert odm._svc.repository.get_data_contract(dc.id) is None

# Discovery Tests
def odm_discover_by_id_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    odm.create_dc({}, dp_id=dp.id)
    
    results = odm.discover(dp_id=dp.id)
    assert len(results) == 2 # 1 DP + 1 DC
    
    # Verify repo state
    repo_dp = odm._svc.repository.get_data_product(dp.id)
    repo_dcs = odm._svc.repository.list_data_contracts(dp_id=dp.id)
    assert repo_dp is not None
    assert len(repo_dcs) == 1

def odm_discover_by_domain_name_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    odm.create_dc({}, dp_id=dp.id)
    
    results = odm.discover(domain="d", name="n")
    assert len(results) == 2
    
    # Verify repo
    repo_dps = odm._svc.repository.list_data_products(domain="d", name="n")
    assert len(repo_dps) == 1

def odm_discover_id_not_found_test(odm):
    results = odm.discover(dp_id="nonexistent")
    assert results == []
    
    # Verify repo is empty if needed (actually it shouldn't have changed)
    assert len(odm._svc.repository.list_data_products()) == 0
