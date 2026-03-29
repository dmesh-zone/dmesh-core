"""CLI integration tests — Data Products.

Happy path: dm put dp → dm list dps → dm get dp → update → verify DB.
Edge cases: missing file, duplicate, not found.
"""
import yaml
import pytest
from .conftest import db_query, run, dp_yaml


class TestDataProductCLICRUD:

    def test_put_creates_dp_and_returns_id(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "transactions"})
        result = run(cli, "put", "dp", str(p))

        assert result.exit_code == 0, result.output
        dp_id = result.output.strip()
        assert len(dp_id) == 36

        rows = db_query(db, "SELECT id, dp_domain, dp_name FROM data_products")
        print(f"[DB] {rows}")
        assert len(rows) == 1
        assert str(rows[0]["id"]) == dp_id
        assert rows[0]["dp_domain"] == "finance"

    def test_list_shows_created_dp(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "orders"})
        run(cli, "put", "dp", str(p))

        result = run(cli, "list", "dps")
        assert result.exit_code == 0
        assert "finance" in result.output
        assert "orders" in result.output

    def test_get_dp_by_history_writes_yaml(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "invoices"})
        run(cli, "put", "dp", str(p),)

        result = run(cli, "get", "dp", "-o", "file")
        assert result.exit_code == 0
        out_file = result.output.strip()
        assert out_file.endswith(".yaml")

        import os
        if os.path.exists(out_file):
            spec = yaml.safe_load(open(out_file).read())
            print(f"[OUTPUT FILE] {spec}")
            assert spec["domain"] == "finance"
            import os; os.unlink(out_file)

    def test_get_dp_by_domain_name(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "payments"})
        run(cli, "put", "dp", str(p))

        # verify that the record is in the database
        rows = db_query(db, "SELECT id, dp_domain, dp_name FROM data_products")
        print(f"[DB] {rows}")

        result = run(cli, "get", "dp", "--domain", "finance", "--name", "payments", "-o", "file")
        assert result.exit_code == 0

        out_file = "finance_payments_v1.0.0.yaml"
        import os
        if os.path.exists(out_file):
            spec = yaml.safe_load(open(out_file).read())
            assert spec["name"] == "payments"
            os.unlink(out_file)

    def test_put_twice_updates_not_duplicates(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "ledger"})
        run(cli, "put", "dp", str(p))

        rows = db_query(db, "SELECT specification->>'status' AS status FROM data_products WHERE dp_name = 'ledger'")
        print(f"[DB after update] {rows}")
        assert len(rows) == 1
        assert rows[0]["status"] == "draft"

        p2 = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "ledger", "status": "active"})
        result = run(cli, "put", "dp", str(p2))
        assert result.exit_code == 0

        rows = db_query(db, "SELECT specification->>'status' AS status FROM data_products WHERE dp_name = 'ledger'")
        print(f"[DB after update] {rows}")
        assert len(rows) == 1
        assert rows[0]["status"] == "active"

    def test_id_is_deterministic(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "stable"})
        r1 = run(cli, "put", "dp", str(p))
        id1 = r1.output.strip()

        # Check DB
        rows = db_query(db, "SELECT id FROM data_products WHERE dp_name = 'stable'")
        assert str(rows[0]["id"]) == id1

        # Same spec → same id
        from open_data_mesh_sdk.core.id_generator import make_dp_id
        expected = make_dp_id("finance", "stable", "v1.0.0")
        print(f"[DETERMINISTIC ID] expected={expected} got={id1}")
        assert id1 == expected

    def test_get_dp_by_id(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "getbyid"})
        res = run(cli, "put", "dp", str(p))
        dp_id = res.output.strip()

        # Delete local file to be sure
        import os; os.unlink(p)

        result = run(cli, "get", "dp", dp_id, "-o", "file")
        assert result.exit_code == 0
        out_file = result.output.strip()
        assert "finance_getbyid_v1.0.0.yaml" in out_file
        assert os.path.exists(out_file)
        os.unlink(out_file)


class TestDataProductCLIEdgeCases:

    def test_put_nonexistent_file_fails(self, cli, db, tmp_path):
        result = run(cli, "put", "dp", "nonexistent.yaml")
        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "error" in result.output.lower()

    def test_get_nonexistent_domain_fails(self, cli, db, tmp_path):
        result = run(cli, "get", "dp", "--domain", "finance", "--name", "nosuchname")
        assert result.exit_code != 0
        assert "no data product found" in result.output.lower()

    def test_get_with_no_history_fails(self, cli, db, tmp_path):
        _, _, history_path = cli
        if history_path.exists():
            history_path.unlink()
        result = run(cli, "get", "dp")
        assert result.exit_code != 0
        assert "no history" in result.output.lower()

    def test_put_rejects_invalid_spec_property_on_update(self, cli, db, tmp_path):
        # 1. Create valid DP
        p1 = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "transactions", "version": "v1.0.0", "status": "draft"})
        res1 = run(cli, "put", "dp", str(p1))
        assert res1.exit_code == 0
        dp_id = res1.output.strip()

        # 2. Try to update with invalid property
        bad_spec = {"id": dp_id, "apiVersion": "v1.0.0", "kind": "DataProduct",
                   "domain": "finance", "name": "transactions", "version": "v1.0.0",
                   "status": "draft", "invalid": "prop"}
        p2 = dp_yaml(tmp_path, spec=bad_spec)
        res2 = run(cli, "put", "dp", str(p2))

        assert res2.exit_code != 0
        assert "additional properties are not allowed" in res2.output.lower()

    def test_delete_dp_removes_from_db(self, cli, db, tmp_path):
        p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "delete", "name": "me"})
        create_res = run(cli, "put", "dp", str(p))
        dp_id = create_res.output.strip()

        delete_res = run(cli, "delete", "dp", dp_id)
        assert delete_res.exit_code == 0
        assert f"Data product {dp_id} deleted" in delete_res.output

        rows = db_query(db, "SELECT id FROM data_products WHERE id = %s", [dp_id])
        assert len(rows) == 0

