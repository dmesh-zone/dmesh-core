"""CLI integration tests — Data Contracts.

Happy path: dm put dc → dm list dcs → dm get dc → update → verify DB.
Edge cases: invalid dp, not found, invalid dc id.
"""
import yaml
import pytest
from .conftest import db_query, run, dp_yaml, dc_yaml

@pytest.fixture
def finance_dp(cli, db, tmp_path):
    """Create a finance/transactions dp and return its id."""
    p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "transactions"})
    result = run(cli, "put", "dp", str(p))
    assert result.exit_code == 0, result.output
    return result.output.strip()

class TestDataContractCLICRUD:

    def test_put_dc_with_domain_dp_name(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path)
        result = run(cli, "put", "dc", str(p),
                     "--domain", "finance", "--dp_name", "transactions")
        print(f"[DC ID] {result.output.strip()}")

        assert result.exit_code == 0
        dc_id = result.output.strip()
        assert len(dc_id) == 36

        rows = db_query(db, "SELECT id, data_product_id FROM data_contracts")
        print(f"[DB] {rows}")
        assert len(rows) == 1
        assert str(rows[0]["data_product_id"]) == finance_dp

    def test_put_dc_with_dp_yaml(self, cli, db, tmp_path, finance_dp):
        dp_p = dp_yaml(tmp_path, spec={"apiVersion": "v1.0.0", "domain": "finance", "name": "transactions"})
        dc_p = dc_yaml(tmp_path, "dc2")
        result = run(cli, "put", "dc", str(dc_p), "--dp", str(dp_p))

        assert result.exit_code == 0
        dc_id = result.output.strip()
        assert len(dc_id) == 36

    def test_put_dc_with_domain_dp_name_version(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path, "dc3")
        result = run(cli, "put", "dc", str(p),
                     "--domain", "finance", "--dp_name", "transactions",
                     "--dp_version", "v1.0.0")
        assert result.exit_code == 0

    def test_list_dcs_by_domain(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path)
        run(cli, "put", "dc", str(p), "--domain", "finance", "--dp_name", "transactions")

        result = run(cli, "list", "dcs", "--domain", "finance")
        assert result.exit_code == 0
        assert "finance" in result.output
        assert "transactions" in result.output

    def test_list_dcs_by_domain_dp_name(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path)
        run(cli, "put", "dc", str(p), "--domain", "finance", "--dp_name", "transactions")

        result = run(cli, "list", "dcs", "--domain", "finance", "--dp_name", "transactions")
        assert result.exit_code == 0
        assert "transactions" in result.output

    def test_list_dcs_by_domain_dp_name_version(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path)
        run(cli, "put", "dc", str(p), "--domain", "finance", "--dp_name", "transactions")

        result = run(cli, "list", "dcs", "--domain", "finance",
                     "--dp_name", "transactions", "--dp_version", "v1.0.0")
        assert result.exit_code == 0
        assert "v1.0.0" in result.output

    def test_get_dc_by_id_writes_yaml(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path)
        create_result = run(cli, "put", "dc", str(p),
                            "--domain", "finance", "--dp_name", "transactions")
        dc_id = create_result.output.strip()

        result = run(cli, "get", "dc", dc_id, "-o", "file")
        assert result.exit_code == 0
        out_file = result.output.strip()
        print(f"[OUTPUT FILE] {out_file}")
        assert "finance_transactions_v1.0.0" in out_file
        assert dc_id in out_file

        import os
        if os.path.exists(out_file):
            spec = yaml.safe_load(open(out_file).read())
            assert spec["id"] == dc_id
            os.unlink(out_file)

    def test_update_dc_with_valid_id(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path)
        create_result = run(cli, "put", "dc", str(p),
                            "--domain", "finance", "--dp_name", "transactions")
        dc_id = create_result.output.strip()

        updated_spec = {"id": dc_id, "apiVersion": "v3.1.0", "kind": "DataContract",
                   "status": "active", "version": "v1.0.0"}
        p2 = dc_yaml(tmp_path, "dc_updated", spec=updated_spec)
        result = run(cli, "put", "dc", str(p2))
        assert result.exit_code == 0

        rows = db_query(db, "SELECT specification->>'status' AS status FROM data_contracts WHERE id = %s", [dc_id])
        print(f"[DB after update] {rows}")
        assert rows[0]["status"] == "active"

class TestDataContractCLIEdgeCases:

    def test_put_dc_with_invalid_dp_fails(self, cli, db, tmp_path):
        p = dc_yaml(tmp_path)
        result = run(cli, "put", "dc", str(p),
                     "--domain", "finance", "--dp_name", "nosuchdp")
        assert result.exit_code != 0
        assert "no data product found" in result.output.lower()

    def test_put_dc_without_parent_fails(self, cli, db, tmp_path):
        p = dc_yaml(tmp_path)
        result = run(cli, "put", "dc", str(p))
        assert result.exit_code != 0

    def test_update_dc_with_invalid_id_fails(self, cli, db, tmp_path):
        bad = {"id": "00000000-0000-0000-0000-000000000000",
               "apiVersion": "v3.1.0", "kind": "DataContract",
               "status": "draft", "version": "v1.0.0"}
        p = dc_yaml(tmp_path, "bad_dc", spec=bad)
        result = run(cli, "put", "dc", str(p))
        assert result.exit_code != 0
        assert "not found" in result.output.lower()

    def test_get_dc_nonexistent_fails(self, cli, db, tmp_path):
        result = run(cli, "get", "dc", "00000000-0000-0000-0000-000000000000")
        assert result.exit_code != 0
        assert "not found" in result.output.lower()

    def test_put_dc_rejects_invalid_spec_property(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path, spec={"apiVersion": "v3.1.0", "domain": "finance", "dp_name": "transactions", "invalid": "invalid"})
        result = run(cli, "put", "dc", str(p), "--domain", "finance", "--dp_name", "transactions")

        assert result.exit_code != 0
        assert "additional properties are not allowed" in result.output.lower()

    def test_put_dc_rejects_invalid_spec_property_on_update(self, cli, db, tmp_path, finance_dp):
        # 1. Create valid DC
        p1 = dc_yaml(tmp_path, "dc_valid")
        res1 = run(cli, "put", "dc", str(p1), "--domain", "finance", "--dp_name", "transactions")
        assert res1.exit_code == 0
        dc_id = res1.output.strip()

        # 2. Try to update with invalid property
        bad_spec = {"id": dc_id, "apiVersion": "v3.1.0", "kind": "DataContract",
                   "status": "draft", "version": "v1.0.0", "invalid": "prop"}
        p2 = dc_yaml(tmp_path, "dc_invalid", spec=bad_spec)
        res2 = run(cli, "put", "dc", str(p2))

        assert res2.exit_code != 0
        assert "additional properties are not allowed" in res2.output.lower()

    def test_delete_dc_removes_from_db(self, cli, db, tmp_path, finance_dp):
        p = dc_yaml(tmp_path, spec={"apiVersion": "v3.1.0"})
        res = run(cli, "put", "dc", str(p), "--domain", "finance", "--dp_name", "transactions")
        dc_id = res.output.strip()

        del_res = run(cli, "delete", "dc", dc_id)
        assert del_res.exit_code == 0
        assert f"Data contract {dc_id} deleted" in del_res.output

        rows = db_query(db, "SELECT id FROM data_contracts WHERE id = %s", [dc_id])
        assert len(rows) == 0

    def test_put_dc_bind_by_id(self, cli, db, tmp_path, finance_dp):
        # 1. Get DP ID from fixture
        dp_id = finance_dp

        # 2. Create DC using DP ID
        p = dc_yaml(tmp_path, spec={"apiVersion": "v3.1.0"})
        res = run(cli, "put", "dc", str(p), "--dp", dp_id)
        assert res.exit_code == 0
        dc_id = res.output.strip()

        # 3. Verify it was actually created
        get_res = run(cli, "get", "dc", dc_id)
        assert get_res.exit_code == 0
        assert dc_id in get_res.output
