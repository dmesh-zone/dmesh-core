import pytest
from assertpy import assert_that

@pytest.mark.asyncio
class TestApiIntegration:
    """
    Integration tests for the DMesh API endpoints.
    Uses httpx for requests and assertpy for fluent assertions.
    """
    
    async def test_health_check(self, api_client):
        """Verify the health check endpoint returns correctly."""
        # GIVEN / WHEN
        response = await api_client.get("/dmesh/health")
        
        # THEN
        assert_that(response.status_code).is_equal_to(200)
        data = response.json()
        assert_that(data).contains_key("status")
        assert_that(data["status"]).is_equal_to("ok")
        assert_that(data["db"]).is_equal_to("connected")
        assert_that(data).contains_key("platform")

    async def test_data_product_lifecycle(self, api_client):
        """Verify full lifecycle of a Data Product via API."""
        # 1. CREATE (GIVEN / WHEN)
        spec = {
            "domain": "finance", 
            "name": "ledger", 
            "version": "v1.0.0"
        }
        create_resp = await api_client.post("/dmesh/dps", json=spec)
        
        # THEN
        assert_that(create_resp.status_code).is_equal_to(201)
        dp = create_resp.json()
        dp_id = dp["id"]
        assert_that(dp["domain"]).is_equal_to("finance")
        assert_that(dp["name"]).is_equal_to("ledger")
        
        # 2. GET (WHEN)
        get_resp = await api_client.get(f"/dmesh/dps/{dp_id}")
        
        # THEN
        assert_that(get_resp.status_code).is_equal_to(200)
        assert_that(get_resp.json()["id"]).is_equal_to(dp_id)
        assert_that(get_resp.json()["name"]).is_equal_to("ledger")
        
        # 3. LIST (WHEN)
        list_resp = await api_client.get("/dmesh/dps")
        
        # THEN
        assert_that(list_resp.status_code).is_equal_to(200)
        items = list_resp.json()
        assert_that(items).is_type_of(list)
        assert_that(len(items)).is_equal_to(1)
        assert_that(items[0]["id"]).is_equal_to(dp_id)
        
        # 4. DELETE (WHEN)
        del_resp = await api_client.delete(f"/dmesh/dps/{dp_id}")
        
        # THEN
        assert_that(del_resp.status_code).is_equal_to(200)
        assert_that(del_resp.json()).is_equal_to({"status": "deleted"})
        
        # 5. VERIFY DELETED (WHEN)
        final_get = await api_client.get(f"/dmesh/dps/{dp_id}")
        
        # THEN
        assert_that(final_get.status_code).is_equal_to(404)

    async def test_data_contract_lifecycle(self, api_client):
        """Verify Data Contract operations via API."""
        # GIVEN: A Data Product to attach the contract to
        dp_resp = await api_client.post("/dmesh/dps", json={"domain": "hr", "name": "staff"})
        dp_id = dp_resp.json()["id"]
        
        # 1. CREATE CONTRACT (WHEN)
        contract_spec = {}
        dc_resp = await api_client.post(f"/dmesh/dps/{dp_id}/dcs", json=contract_spec)
        
        # THEN
        assert_that(dc_resp.status_code).is_equal_to(201)
        dc_data = dc_resp.json()
        dc_id = dc_data["id"]
        assert_that(dc_data["domain"]).is_equal_to("hr")
        assert_that(dc_data["dataProduct"]).is_equal_to("staff")
        
        # 2. GET CONTRACT (WHEN)
        get_dc = await api_client.get(f"/dmesh/dcs/{dc_id}")
        
        # THEN
        assert_that(get_dc.status_code).is_equal_to(200)
        assert_that(get_dc.json()["id"]).is_equal_to(dc_id)
        
        # 3. PATCH CONTRACT (WHEN)
        patch_resp = await api_client.patch(
            f"/dmesh/dcs/{dc_id}", 
            json={"status": "active"}
        )
        
        # THEN
        assert_that(patch_resp.status_code).is_equal_to(200)
        assert_that(patch_resp.json()["status"]).is_equal_to("active")
        
        # 4. DELETE CONTRACT (WHEN)
        del_resp = await api_client.delete(f"/dmesh/dcs/{dc_id}")
        
        # THEN
        assert_that(del_resp.status_code).is_equal_to(200)

    async def test_error_handling(self, api_client):
        """Verify API handles invalid input correctly."""
        # GIVEN: Invalid specification (missing required fields)
        # We need something that definitely fails Bitol validation
        bad_spec = {"apiVersion": "v1.0.0", "kind": "DataProduct", "invalid_field": "error"}
        
        # WHEN
        resp = await api_client.post("/dmesh/dps", json=bad_spec)
        
        # THEN
        assert_that(resp.status_code).is_equal_to(400)
        assert_that(resp.json()["detail"]).contains("Invalid Data Product specification")

    async def test_non_existent_resource(self, api_client):
        """Verify 404 for non-existent resources."""
        # GIVEN: A valid but non-existent UUID
        import uuid
        fake_id = str(uuid.uuid4())
        
        # WHEN
        resp = await api_client.get(f"/dmesh/dps/{fake_id}")
        
        # THEN
        assert_that(resp.status_code).is_equal_to(404)
        assert_that(resp.json()["detail"]).contains("not found")

    async def test_discovery(self, api_client):
        """Verify the /discover endpoint returns a flat list of entities with filtering."""
        # GIVEN: 2 domains, each with 2 data products, each product with a contract
        # Domain: Finance
        f_ledger = await api_client.post("/dmesh/dps", json={"domain": "finance", "name": "ledger"})
        await api_client.post(f"/dmesh/dps/{f_ledger.json()['id']}/dcs", json={"name": "ledger-contract"})
        
        f_tx = await api_client.post("/dmesh/dps", json={"domain": "finance", "name": "transactions"})
        await api_client.post(f"/dmesh/dps/{f_tx.json()['id']}/dcs", json={"name": "tx-contract"})

        # Domain: HR
        h_staff = await api_client.post("/dmesh/dps", json={"domain": "hr", "name": "staff"})
        await api_client.post(f"/dmesh/dps/{h_staff.json()['id']}/dcs", json={"name": "staff-contract"})
        
        h_payroll = await api_client.post("/dmesh/dps", json={"domain": "hr", "name": "payroll"})
        await api_client.post(f"/dmesh/dps/{h_payroll.json()['id']}/dcs", json={"name": "payroll-contract"})

        # --- SCENARIO 1: No filters (Global Discovery) ---
        all_resp = await api_client.get("/dmesh/discover")
        assert_that(all_resp.status_code).is_equal_to(200)
        # 4 DPs + 4 DCs = 8 items
        items = all_resp.json()
        assert_that(items).is_type_of(list)
        assert_that(len(items)).is_equal_to(8)

        # --- SCENARIO 2: Filter by Domain only ---
        fin_resp = await api_client.get("/dmesh/discover?domain=finance")
        assert_that(fin_resp.status_code).is_equal_to(200)
        # 2 DPs + 2 DCs = 4 items
        items = fin_resp.json()
        assert_that(len(items)).is_equal_to(4)
        for item in items:
            assert_that(item["domain"]).is_equal_to("finance")

        # --- SCENARIO 3: Filter by Domain + Name ---
        spec_resp = await api_client.get("/dmesh/discover?domain=finance&name=ledger")
        assert_that(spec_resp.status_code).is_equal_to(200)
        # 1 DP + 1 DC = 2 items
        items = spec_resp.json()
        assert_that(len(items)).is_equal_to(2)
        assert_that([i["name"] for i in items if i["kind"] == "DataProduct"]).contains("ledger")
        assert_that([i["dataProduct"] for i in items if i["kind"] == "DataContract"]).contains("ledger")

        # --- SCENARIO 4: Filter by non-existent domain ---
        none_resp = await api_client.get("/dmesh/discover?domain=marketing")
        assert_that(none_resp.status_code).is_equal_to(200)
        assert_that(none_resp.json()).is_empty()
