"""WS integration tests — Data Contracts.

Happy path: full CRUD lifecycle linked to a data product.
Edge cases: invalid dp_id, not found, cascade delete.
"""
import os
import pytest
from .conftest import db_query, log

BASE_PATH = os.environ.get("WS_BASE_PATH", "odm")

DP_SPEC = {
    "apiVersion": "v1.0.0",
    "kind": "DataProduct",
    "domain": "finance",
    "name": "transactions",
    "version": "v1.0.0",
    "status": "draft",
}

DC_SPEC = {}  # minimal — all defaults applied by WS


@pytest.fixture
def dp_id(ws, db):
    """Create a data product and return its id."""
    resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
    assert resp.status_code == 201
    return resp.json()["id"]


# ===========================================================================
# Happy path — full CRUD
# ===========================================================================

class TestDataContractCRUD:

    def test_create_returns_spec_with_id(self, ws, db, dp_id):
        log("INPUT", {"dp_id": dp_id, "dc_spec": DC_SPEC})
        resp = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        log("RESPONSE", {"status": resp.status_code, "body": resp.json()})

        assert resp.status_code == 201
        spec = resp.json()
        assert "id" in spec
        assert spec["apiVersion"] == "v3.1.0"
        assert spec["status"] == "draft"

        rows = db_query(db, "SELECT id, data_product_id FROM data_contracts")
        log("DB state", rows)
        assert len(rows) == 1
        assert str(rows[0]["data_product_id"]) == dp_id

    def test_list_contracts_for_dp(self, ws, db, dp_id):
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)

        resp = ws.get(f"/{BASE_PATH}/dps/{dp_id}/dcs")
        log("LIST DCs", {"status": resp.status_code, "count": len(resp.json())})

        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_list_all_contracts_with_dp_info(self, ws, db, dp_id):
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)

        resp = ws.get(f"/{BASE_PATH}/dcs", params={"domain": "finance"})
        log("LIST ALL DCs", {"status": resp.status_code, "body": resp.json()})

        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 1
        assert items[0]["dp_domain"] == "finance"
        assert items[0]["dp_name"] == "transactions"
        assert "dc_id" in items[0]

    def test_get_by_id_returns_spec_with_headers(self, ws, db, dp_id):
        create_resp = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        dc_id = create_resp.json()["id"]

        resp = ws.get(f"/{BASE_PATH}/dcs/{dc_id}")
        log("GET DC by id", {"status": resp.status_code, "headers": dict(resp.headers), "body": resp.json()})

        assert resp.status_code == 200
        assert resp.headers["X-DC-ID"] == dc_id
        assert resp.headers["X-DC-DP-ID"] == dp_id
        assert resp.headers["X-DC-DP-Domain"] == "finance"
        assert resp.headers["X-DC-DP-Name"] == "transactions"

    def test_update_changes_status(self, ws, db, dp_id):
        create_resp = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        dc_id = create_resp.json()["id"]

        updated = {"apiVersion": "v3.1.0", "kind": "DataContract", "status": "active", "version": "v1.0.0"}
        log("UPDATE INPUT", updated)
        resp = ws.put(f"/{BASE_PATH}/dcs/{dc_id}", json=updated)
        log("UPDATE RESPONSE", {"status": resp.status_code, "body": resp.json()})

        assert resp.status_code == 200
        assert resp.json()["status"] == "active"

        rows = db_query(db, "SELECT specification->>'status' AS status FROM data_contracts WHERE id = %s", [dc_id])
        log("DB state after update", rows)
        assert rows[0]["status"] == "active"

    def test_delete_removes_from_db(self, ws, db, dp_id):
        create_resp = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        dc_id = create_resp.json()["id"]

        resp = ws.delete(f"/{BASE_PATH}/dcs/{dc_id}")
        log("DELETE DC", {"status": resp.status_code})
        assert resp.status_code == 204

        rows = db_query(db, "SELECT id FROM data_contracts WHERE id = %s", [dc_id])
        log("DB state after delete", rows)
        assert len(rows) == 0

    def test_cascade_delete_removes_contracts(self, ws, db, dp_id):
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)

        ws.delete(f"/{BASE_PATH}/dps/{dp_id}")
        rows = db_query(db, "SELECT id FROM data_contracts WHERE data_product_id = %s", [dp_id])
        log("DB after cascade delete", rows)
        assert len(rows) == 0

    def test_dc_id_is_deterministic(self, ws, db, dp_id):
        """DC id is deterministic: same dp + same dc_index → same id."""
        from app.id_generator import make_dc_id
        r = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        dc_id = r.json()["id"]

        expected = make_dc_id("finance", "transactions", "v1.0.0", 0)
        log("DC DETERMINISTIC ID", {"got": dc_id, "expected": expected})
        assert dc_id == expected

    def test_second_dc_gets_index_1(self, ws, db, dp_id):
        """Second DC for same DP gets dc_index=1."""
        from app.id_generator import make_dc_id
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        r2 = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        dc_id2 = r2.json()["id"]

        expected = make_dc_id("finance", "transactions", "v1.0.0", 1)
        log("SECOND DC ID", {"got": dc_id2, "expected": expected})
        assert dc_id2 == expected


# ===========================================================================
# Edge cases
# ===========================================================================

class TestDataContractEdgeCases:

    def test_create_with_invalid_dp_id_returns_404(self, ws, db):
        resp = ws.post(f"/{BASE_PATH}/dps/00000000-0000-0000-0000-000000000000/dcs", json=DC_SPEC)
        log("INVALID DP ID", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 404

    def test_get_nonexistent_returns_404(self, ws, db):
        resp = ws.get(f"/{BASE_PATH}/dcs/00000000-0000-0000-0000-000000000000")
        log("DC NOT FOUND", {"status": resp.status_code})
        assert resp.status_code == 404

    def test_update_nonexistent_returns_404(self, ws, db):
        resp = ws.put(f"/{BASE_PATH}/dcs/00000000-0000-0000-0000-000000000000",
                      json={"apiVersion": "v3.1.0", "kind": "DataContract", "status": "draft", "version": "v1.0.0"})
        log("UPDATE NOT FOUND", {"status": resp.status_code})
        assert resp.status_code == 404

    def test_list_filter_by_domain_dp_name_version(self, ws, db, dp_id):
        ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        resp = ws.get(f"/{BASE_PATH}/dcs", params={"domain": "finance", "dp_name": "transactions", "dp_version": "v1.0.0"})
        log("FILTERED DC LIST", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_create_dc_invalid_spec_fails(self, ws, db, dp_id):
        bad_spec = {"invalid": "property"}
        resp = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=bad_spec)
        log("CREATE DC INVALID", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 422
        assert "Additional properties are not allowed" in resp.json()["detail"]

    def test_update_dc_invalid_spec_fails(self, ws, db, dp_id):
        create_resp = ws.post(f"/{BASE_PATH}/dps/{dp_id}/dcs", json=DC_SPEC)
        dc_id = create_resp.json()["id"]

        bad_spec = {"apiVersion": "v3.1.0", "kind": "DataContract", "status": "draft", "version": "v1.0.0", "invalid": "prop"}
        resp = ws.put(f"/{BASE_PATH}/dcs/{dc_id}", json=bad_spec)
        log("UPDATE DC INVALID", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 422
        assert "Additional properties are not allowed" in resp.json()["detail"]
