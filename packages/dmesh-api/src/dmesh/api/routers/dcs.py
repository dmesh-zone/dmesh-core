from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from dmesh.sdk import create_dc, update_dc, patch_dc, get_dc, list_dcs, delete_dc
from dmesh.api.dependencies import get_dc_repo, get_dp_repo
from dmesh.sdk.ports.repository import DataContractRepository, DataProductRepository

router = APIRouter(tags=["Data Contracts"])

@router.post("/dps/{dp_id}/dcs", status_code=201)
@router.post("/dp/{dp_id}/dc", status_code=201, include_in_schema=False)
@router.post("/data-products/{dp_id}/data-contracts", status_code=201, include_in_schema=False)
@router.post("/data-product/{dp_id}/data-contract", status_code=201, include_in_schema=False)
async def create_data_contract(
    dp_id: str, 
    spec: dict, 
    repo: DataContractRepository = Depends(get_dc_repo),
    dp_repo: DataProductRepository = Depends(get_dp_repo)
):
    try:
        return await create_dc(repo, dp_repo, spec, dp_id=dp_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dcs/{dc_id}")
@router.get("/dc/{dc_id}", include_in_schema=False)
@router.get("/data-contracts/{dc_id}", include_in_schema=False)
@router.get("/data-contract/{dc_id}", include_in_schema=False)
async def get_data_contract(dc_id: str, repo: DataContractRepository = Depends(get_dc_repo)):
    dc = await get_dc(repo, id=dc_id)
    if not dc:
        raise HTTPException(status_code=404, detail=f"Data Contract {dc_id} not found")
    return dc

@router.get("/dcs")
@router.get("/dc", include_in_schema=False)
@router.get("/data-contracts", include_in_schema=False)
@router.get("/data-contract", include_in_schema=False)
async def list_data_contracts(dp_id: str = Query(None), repo: DataContractRepository = Depends(get_dc_repo)):
    try:
        return await list_dcs(repo, dp_id=dp_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/dcs/{dc_id}")
@router.patch("/dc/{dc_id}", include_in_schema=False)
@router.patch("/data-contracts/{dc_id}", include_in_schema=False)
@router.patch("/data-contract/{dc_id}", include_in_schema=False)
async def patch_data_contract(dc_id: str, spec: dict, repo: DataContractRepository = Depends(get_dc_repo)):
    try:
        # Note: the sdk patch_dc expects 'id' in spec; for REST we typically take from URL
        spec_with_id = {**spec, "id": dc_id}
        return await patch_dc(repo, spec_with_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/dcs/{dc_id}")
@router.delete("/dc/{dc_id}", include_in_schema=False)
@router.delete("/data-contracts/{dc_id}", include_in_schema=False)
@router.delete("/data-contract/{dc_id}", include_in_schema=False)
async def delete_data_contract(dc_id: str, repo: DataContractRepository = Depends(get_dc_repo)):
    success = await delete_dc(repo, id=dc_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Data Contract {dc_id} not found")
    return {"status": "deleted"}
