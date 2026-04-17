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
