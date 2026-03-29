"""WS integration tests — Data Products.

Happy path: full CRUD lifecycle.
Edge cases: duplicate, not found, validation errors.

Each test prints inputs/outputs for reviewer visibility.
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


# ===========================================================================
# Happy path — full CRUD
# ===========================================================================

class TestDataProductCRUD:

    def test_create_returns_spec_with_id(self, ws, db):
        log("INPUT", {"domain": "finance", "name": "transactions"})
        resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        body = resp.json()
        log("RESPONSE", {"status": resp.status_code, "body": body})

        assert resp.status_code == 201
        # Body is DataProductResponse — spec is nested under 'specification'
        spec = body.get("specification") or body
        dp_id = body.get("id") or spec.get("id")
        assert dp_id is not None
        assert spec.get("domain") == "finance"
        assert spec.get("name") == "transactions"
        assert spec.get("status") == "draft"
        assert spec.get("version") == "v1.0.0"

        rows = db_query(db, "SELECT id, dp_domain, dp_name, dp_version FROM data_products")
        log("DB state", rows)
        assert len(rows) == 1
        assert rows[0]["dp_domain"] == "finance"

    def test_list_returns_specs(self, ws, db):
        ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        resp = ws.get(f"/{BASE_PATH}/dps")
        log("LIST response", {"status": resp.status_code, "count": len(resp.json())})

        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 1
        assert items[0]["domain"] == "finance"

    def test_list_filter_by_domain_name_version(self, ws, db):
        ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        ws.post(f"/{BASE_PATH}/dps", json={**DP_SPEC, "name": "orders"})
        resp = ws.get(f"/{BASE_PATH}/dps", params={"domain": "finance", "name": "transactions", "version": "v1.0.0"})
        log("FILTERED LIST", {"status": resp.status_code, "body": resp.json()})

        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 1
        assert items[0]["name"] == "transactions"

    def test_get_by_id_returns_spec_with_headers(self, ws, db):
        create_resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        dp_id = create_resp.json()["id"]

        resp = ws.get(f"/{BASE_PATH}/dps/{dp_id}")
        log("GET by id", {"status": resp.status_code, "headers": dict(resp.headers), "body": resp.json()})

        assert resp.status_code == 200
        assert resp.json()["id"] == dp_id
        assert resp.headers["X-DP-ID"] == dp_id
        assert "X-DP-Created-At" in resp.headers
        assert "X-DP-Updated-At" in resp.headers

    def test_update_changes_status(self, ws, db):
        create_resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        dp_id = (create_resp.json().get("specification") or create_resp.json()).get("id") or create_resp.json()["id"]

        updated = {**DP_SPEC, "status": "active"}
        log("UPDATE INPUT", updated)
        resp = ws.put(f"/{BASE_PATH}/dps/{dp_id}", json=updated)
        body = resp.json()
        log("UPDATE RESPONSE", {"status": resp.status_code, "body": body})

        assert resp.status_code == 200
        spec = body.get("specification") or body
        assert spec.get("status") == "active"

        rows = db_query(db, "SELECT specification->>'status' AS status FROM data_products WHERE id = %s", [dp_id])
        log("DB state after update", rows)
        assert rows[0]["status"] == "active"

    def test_delete_removes_from_db(self, ws, db):
        create_resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        dp_id = create_resp.json()["id"]

        resp = ws.delete(f"/{BASE_PATH}/dps/{dp_id}")
        log("DELETE", {"status": resp.status_code})
        assert resp.status_code == 204

        rows = db_query(db, "SELECT id FROM data_products WHERE id = %s", [dp_id])
        log("DB state after delete", rows)
        assert len(rows) == 0

    def test_id_is_deterministic(self, ws, db):
        """Same domain/name/version always produces the same id."""
        r1 = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        id1 = (r1.json().get("specification") or r1.json()).get("id") or r1.json()["id"]
        ws.delete(f"/{BASE_PATH}/dps/{id1}")

        r2 = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        id2 = (r2.json().get("specification") or r2.json()).get("id") or r2.json()["id"]
        log("DETERMINISTIC IDs", {"id1": id1, "id2": id2})
        assert id1 == id2

    def test_response_id_matches_spec_id(self, ws, db):
        """data_products.id must always equal specification.id."""
        resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        spec = resp.json()
        dp_id = spec["id"]

        get_resp = ws.get(f"/{BASE_PATH}/dps/{dp_id}")
        log("ID consistency check", {"spec.id": spec["id"], "X-DP-ID": get_resp.headers.get("X-DP-ID")})
        assert get_resp.headers["X-DP-ID"] == spec["id"]

        rows = db_query(db, "SELECT id FROM data_products WHERE id = %s", [dp_id])
        assert str(rows[0]["id"]) == dp_id


# ===========================================================================
# Edge cases
# ===========================================================================

class TestDataProductEdgeCases:

    def test_duplicate_domain_name_version_returns_409(self, ws, db):
        ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        resp = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        log("DUPLICATE", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 409

    def test_get_nonexistent_returns_404(self, ws, db):
        resp = ws.get(f"/{BASE_PATH}/dps/00000000-0000-0000-0000-000000000000")
        log("NOT FOUND", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, ws, db):
        resp = ws.delete(f"/{BASE_PATH}/dps/00000000-0000-0000-0000-000000000000")
        log("DELETE NOT FOUND", {"status": resp.status_code})
        assert resp.status_code == 404

    def test_validation_rejects_invalid_api_version(self, ws, db):
        bad_spec = {**DP_SPEC, "apiVersion": "v99.0.0"}
        resp = ws.post(f"/{BASE_PATH}/dps", json=bad_spec)
        log("SCHEMA VALIDATION", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 422

    def test_missing_required_fields_returns_422(self, ws, db):
        resp = ws.post(f"/{BASE_PATH}/dps", json={"domain": "finance"})
        log("MISSING FIELDS", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 422

    def test_list_empty_returns_empty_array(self, ws, db):
        resp = ws.get(f"/{BASE_PATH}/dps")
        log("EMPTY LIST", {"status": resp.status_code, "body": resp.json()})
        assert resp.status_code == 200
        assert resp.json() == []

    def test_post_invalid_spec_property_fails(self, ws, db):
        bad_spec = {**DP_SPEC, "invalid": "property"}
        log("INPUT", bad_spec)
        resp = ws.post(f"/{BASE_PATH}/dps", json=bad_spec)
        log("RESPONSE", {"status": resp.status_code, "body": resp.json()})

        assert resp.status_code == 422
        assert "Additional properties are not allowed" in resp.json()["detail"]

    def test_put_invalid_spec_property_fails(self, ws, db):
        # 1. Create valid DP
        resp1 = ws.post(f"/{BASE_PATH}/dps", json=DP_SPEC)
        assert resp1.status_code == 201
        dp_id = resp1.json()["id"]

        # 2. Try to update with invalid property
        bad_spec = {**DP_SPEC, "id": dp_id, "invalid": "property"}
        log("UPDATE INPUT", bad_spec)
        resp2 = ws.put(f"/{BASE_PATH}/dps/{dp_id}", json=bad_spec)
        log("UPDATE RESPONSE", {"status": resp2.status_code, "body": resp2.json()})

        assert resp2.status_code == 422
        assert "Additional properties are not allowed" in resp2.json()["detail"]
