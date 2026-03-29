from typing import List, Any
from fastapi import APIRouter, Request, HTTPException, Query
from open_data_mesh_sdk.core.service import DataMeshService

router = APIRouter()

@router.post("/data-products", status_code=201)
@router.post("/dps", status_code=201, include_in_schema=False)
def create_dp(request: Request, spec: dict):
    service: DataMeshService = request.app.state.service
    try:
        dp = service.create_data_product(spec)
        return dp.specification
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/data-products")
@router.get("/dps", include_in_schema=False)
def list_dps(
    request: Request,
    domain: str = Query(None),
    name: str = Query(None),
    version: str = Query(None)
):
    service: DataMeshService = request.app.state.service
    dps = service.list_data_products(domain, name, version)
    return [dp.specification for dp in dps]

@router.get("/data-products/{dp_id}")
@router.get("/dps/{dp_id}", include_in_schema=False)
def get_dp(request: Request, dp_id: str):
    service: DataMeshService = request.app.state.service
    dp = service.get_data_product(dp_id)
    if not dp:
        raise HTTPException(status_code=404, detail=f"Data Product {dp_id} not found")
    return dp.specification
