from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from dmesh.sdk import create_dp, update_dp, get_dp, list_dps, delete_dp
from dmesh.api.dependencies import get_dp_repo
from dmesh.sdk.ports.repository import DataProductRepository

router = APIRouter(tags=["Data Products"])

@router.post("/dps", status_code=201)
@router.post("/dp", status_code=201, include_in_schema=False)
@router.post("/data-products", status_code=201, include_in_schema=False)
@router.post("/data-product", status_code=201, include_in_schema=False)
async def create_data_product(spec: dict, repo: DataProductRepository = Depends(get_dp_repo)):
    try:
        return await create_dp(repo, spec)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dps")
@router.get("/dp", include_in_schema=False)
@router.get("/data-products", include_in_schema=False)
@router.get("/data-product", include_in_schema=False)
async def list_data_products(
    domain: str = Query(None),
    name: str = Query(None),
    repo: DataProductRepository = Depends(get_dp_repo)
):
    try:
        return await list_dps(repo, domain=domain, name=name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dps/{dp_id}")
@router.get("/dp/{dp_id}", include_in_schema=False)
@router.get("/data-products/{dp_id}", include_in_schema=False)
@router.get("/data-product/{dp_id}", include_in_schema=False)
async def get_data_product(dp_id: str, repo: DataProductRepository = Depends(get_dp_repo)):
    dp = await get_dp(repo, id=dp_id)
    if not dp:
        raise HTTPException(status_code=404, detail=f"Data Product {dp_id} not found")
    return dp

@router.delete("/dps/{dp_id}")
@router.delete("/dp/{dp_id}", include_in_schema=False)
@router.delete("/data-products/{dp_id}", include_in_schema=False)
@router.delete("/data-product/{dp_id}", include_in_schema=False)
async def delete_data_product(dp_id: str, repo: DataProductRepository = Depends(get_dp_repo)):
    success = await delete_dp(repo, id=dp_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Data Product {dp_id} not found")
    return {"status": "deleted"}
