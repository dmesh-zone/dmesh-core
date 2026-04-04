import jsonschema
import pytest
import os
from open_data_mesh_sdk import OpenDataMesh
from open_data_mesh_sdk.persistency.sqlite import SQLiteRepository
from open_data_mesh_sdk.core.models import DataProduct, DataContract
from open_data_mesh_sdk.core.exceptions import DataProductValidationError, DataContractValidationError

@pytest.fixture
def odm(tmp_path):
    db_path = str(tmp_path / "test_client.db")
    repo = SQLiteRepository(db_path)
    client = OpenDataMesh(repo)
    yield client

# Data Product Tests
def odm_create_dp_valid_minimum_input_test(odm):
    spec = {"domain": "finance", "name": "ledger"}
    dp = odm.create_dp(spec)
    
    # Assert return value
    assert dp["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"
    assert dp["apiVersion"] == "v1.0.0"
    assert dp["kind"] == "DataProduct"
    assert dp["status"] == "draft"
    assert dp["version"] == "v1.0.0"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_product(dp["id"])
    assert persisted is not None
    assert persisted.id == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert persisted.domain == "finance"
    assert persisted.name == "ledger"
    assert persisted.specification["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert persisted.specification["domain"] == "finance"
    assert persisted.specification["name"] == "ledger"
    assert persisted.specification["apiVersion"] == "v1.0.0"
    assert persisted.specification["kind"] == "DataProduct"
    assert persisted.specification["status"] == "draft"
    assert persisted.specification["version"] == "v1.0.0"

def odm_create_dp_valid_more_input_test(odm):
    spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "status": "draft", "version": "v1.0.0"}
    dp = odm.create_dp(spec, domain="finance", name="ledger")
    
    # Assert return value
    assert dp["id"] == 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'
    assert dp["domain"] == "finance"
    assert dp["name"] == "ledger"
    assert dp["apiVersion"] == "v1.0.0"
    assert dp["kind"] == "DataProduct"
    assert dp["status"] == "draft"
    assert dp["version"] == "v1.0.0"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_product(dp["id"])
    assert persisted is not None
    assert persisted.domain == "finance"
    assert persisted.name == "ledger"
    assert persisted.specification["apiVersion"] == "v1.0.0"
    assert persisted.specification["kind"] == "DataProduct"
    assert persisted.specification["status"] == "draft"
    assert persisted.specification["version"] == "v1.0.0"

def odm_create_dp_invalid_property_test(odm):
    spec = {"domain": "finance", "name": "ledger", "invalid": "property"}
    with pytest.raises(DataProductValidationError) as exc:
        odm.create_dp(spec)
    assert "Invalid Data Product specification: Additional properties are not allowed ('invalid' was unexpected)" in str(exc.value)
    
def odm_update_dp_valid_test(odm):
    spec = {"domain": "finance", "name": "ledger"}
    dp = odm.create_dp(spec)
    dp_id = dp["id"]

    # get dp
    fetched = odm.get_dp(id=dp_id)
    assert fetched["status"] == "draft"
    
    # update dp
    spec_to_update = fetched.copy()
    spec_to_update["status"] = "active"
    updated = odm.update_dp(spec_to_update)
    
    # Assert return value
    assert updated["status"] == "active"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_product(dp_id)
    assert persisted.specification["status"] == "active"


def odm_get_dp_by_id_test(odm):
    spec = {"domain": "f", "name": "n"}
    created = odm.create_dp(spec)
    fetched = odm.get_dp(id=created["id"])
    
    assert isinstance(fetched, dict)
    assert fetched["id"] == created["id"]
    
    # Verify it matches what's in repo
    persisted = odm._svc.repository.get_data_product(created["id"])
    assert fetched["id"] == persisted.id

def odm_get_dp_by_domain_name_test(odm):
    odm.create_dp({"domain": "f", "name": "n"})
    fetched = odm.get_dp(domain="f", name="n")
    
    assert fetched[0]["domain"] == "f"
    assert fetched[0]["name"] == "n"
    
    # Verify repo has it
    results = odm._svc.repository.list_data_products(domain="f", name="n")
    assert len(results) == 1
    assert results[0].id == fetched[0]["id"]

def odm_get_dp_not_found_test(odm):
    assert odm.get_dp(id="missing") is None

def odm_list_dps_filter_test(odm):
    odm.create_dp({"domain": "d1", "name": "n1"})
    odm.create_dp({"domain": "d2", "name": "n2"})
    
    d1s = odm.list_dps(domain="d1")
    assert len(d1s) == 1
    assert d1s[0]["domain"] == "d1"
    
    # Verify repo state
    all_repo = odm._svc.repository.list_data_products()
    assert len(all_repo) == 2

def odm_delete_dp_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    assert odm.delete_dp(dp["id"]) is True
    
    # Assert return value
    assert odm.get_dp(id=dp["id"]) is None
    
    # Assert persistency state
    assert odm._svc.repository.get_data_product(dp["id"]) is None

# Data Contract Tests
def odm_create_dc_valid_minimum_input_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n"})
    dc = odm.create_dc({}, dp_id=dp["id"])
    
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    assert dc["kind"] == "DataContract"
    assert dc["apiVersion"] == "v3.1.0"
    assert dc["status"] == "draft"
    assert dc["version"] == "v1.0.0"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_contract(dc["id"])
    assert persisted is not None
    assert persisted.data_product_id == dp["id"]

def odm_create_dc_invalid_property_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n"})
    spec = {"invalid": "property"}
    with pytest.raises(DataContractValidationError) as exc:
        odm.create_dc(spec, dp_id=dp["id"])
    assert "Invalid Data Contract specification: Additional properties are not allowed ('invalid' was unexpected)" in str(exc.value)

def odm_update_dc_valid_more_input_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n"})
    dc = odm.create_dc({"dataProduct": "n"}, dp_id=dp["id"])
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    
    # get dp
    updated_spec = odm.get_dc(dc["id"])
    updated_spec["dataProduct"] = "m"
    updated = odm.update_dc(updated_spec)
    
    assert updated["dataProduct"] == "m"
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_contract(dc["id"])
    assert persisted.specification["dataProduct"] == "m"

def odm_update_dc_valid_removes_dropped_properties_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n"})
    dc = odm.create_dc({"dataProduct": "n"}, dp_id=dp["id"])
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    
    # get dp
    updated_spec = odm.get_dc(dc["id"])
    updated_spec["status"] = "active"
    del updated_spec["dataProduct"]
    updated = odm.update_dc(updated_spec)
    
    assert "dataProduct" not in updated
    
    # Assert persistency state
    persisted = odm._svc.repository.get_data_contract(dc["id"])
    assert persisted.specification["status"] == "active"
    assert "dataProduct" not in persisted.specification
    
def odm_patch_dc_valid_patching_schema_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n"})
    custom_property_1 = {"property": "p1", "value": "v1"}
    custom_property_2 = {"property": "p2", "value": "v2"}
    dc = odm.create_dc({"dataProduct": "n", "status": "proposed",
                        "customProperties": [custom_property_1]}, dp_id=dp["id"])
    assert dc["id"] == 'c9ca57c1-8c75-512d-8c4f-debcc082003f'
    assert dc["status"] == "proposed"
    assert dc["dataProduct"] == "n"
    assert dc["customProperties"] == [custom_property_1]

    schema_array = [{"name": "table", "properties": [{"name": "id", "logicalType": "string"}, {"name": "age", "logicalType": "integer"}]}]
    patching_input = {"id": dc["id"], "status": "active", "schema": schema_array, "customProperties": [custom_property_2]}
    patched = odm.patch_dc(patching_input)
    
    assert patched["status"] == "active"
    assert patched["schema"] == schema_array
    assert patched["customProperties"][0] == custom_property_1
    assert patched["customProperties"][1] == custom_property_2

    # Assert persistency state
    persisted = odm._svc.repository.get_data_contract(dc["id"])
    assert persisted.specification["status"] == "active"
    assert persisted.specification["schema"] == schema_array
    assert persisted.specification["dataProduct"] == "n"
    assert persisted.specification["customProperties"][0] == custom_property_1
    assert persisted.specification["customProperties"][1] == custom_property_2

def odm_get_dc_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    dc = odm.create_dc({}, dp_id=dp["id"])
    fetched = odm.get_dc(dc["id"])
    
    assert isinstance(fetched, dict)
    assert fetched["id"] == dc["id"]
    
    # Verify repo
    persisted = odm._svc.repository.get_data_contract(dc["id"])
    assert persisted.id == fetched["id"]

def odm_list_dcs_by_domain_name_test(odm):
    dp = odm.create_dp({"domain": "finance", "name": "ledger", "version": "v1"})
    odm.create_dc({"dataProduct": "ledger"}, dp_id=dp["id"])
    odm.create_dc({"dataProduct": "ledger"}, dp_id=dp["id"])
    
    dcs = odm.list_dcs(domain="finance", dp_name="ledger")
    assert len(dcs) == 2
    
    # Verify repo
    repo_dcs = odm._svc.repository.list_data_contracts(dp_id=dp["id"])
    assert len(repo_dcs) == 2

def odm_delete_dc_valid_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    dc = odm.create_dc({}, dp_id=dp["id"])
    assert odm.delete_dc(dc["id"]) is True
    
    # Assert return value
    assert odm.get_dc(dc["id"]) is None
    
    # Assert persistency state
    assert odm._svc.repository.get_data_contract(dc["id"]) is None

# Discovery Tests
def odm_discover_by_id_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    odm.create_dc({}, dp_id=dp["id"])
    
    results = odm.discover(dp_id=dp["id"])
    assert len(results) == 2 # 1 DP + 1 DC
    
    # Verify repo state
    repo_dp = odm._svc.repository.get_data_product(dp["id"])
    repo_dcs = odm._svc.repository.list_data_contracts(dp_id=dp["id"])
    assert repo_dp is not None
    assert len(repo_dcs) == 1

def odm_discover_by_domain_name_test(odm):
    dp = odm.create_dp({"domain": "d", "name": "n", "version": "v"})
    odm.create_dc({}, dp_id=dp["id"])
    
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
