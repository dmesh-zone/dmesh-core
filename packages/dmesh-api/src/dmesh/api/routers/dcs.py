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

@router.put("/dcs/{dc_id}")
@router.put("/dc/{dc_id}", include_in_schema=False)
@router.put("/data-contracts/{dc_id}", include_in_schema=False)
@router.put("/data-contract/{dc_id}", include_in_schema=False)
async def save_data_contract(dc_id: str, spec: dict, repo: DataContractRepository = Depends(get_dc_repo)):
    try:
        from dmesh.sdk.models import DataContract
        import uuid

        if "specification" in spec:
            dc_spec = spec["specification"]
            dp_id = spec.get("data_product_id")
        else:
            dc_spec = spec
            dp_id = spec.get("dataProductId") or spec.get("data_product_id")
            
        dc = DataContract(
            id=uuid.UUID(dc_id),
            data_product_id=uuid.UUID(dp_id) if dp_id else None,
            specification=dc_spec,
            created_at=spec.get("created_at"),
            updated_at=spec.get("updated_at")
        )
        await repo.save(dc)
        return {
            "status": "saved", 
            "id": dc_id,
            "created_at": dc.created_at.isoformat() if dc.created_at else None, 
            "updated_at": dc.updated_at.isoformat() if dc.updated_at else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/admin/truncate_dcs", include_in_schema=False)
async def truncate_data_contracts(repo: DataContractRepository = Depends(get_dc_repo)):
    try:
        await repo.truncate()
        return {"status": "truncated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dcs/{dc_id}")
@router.get("/dc/{dc_id}", include_in_schema=False)
@router.get("/data-contracts/{dc_id}", include_in_schema=False)
@router.get("/data-contract/{dc_id}", include_in_schema=False)
async def get_data_contract(dc_id: str, include_metadata: bool = False, repo: DataContractRepository = Depends(get_dc_repo)):
    dc = await get_dc(repo, id=dc_id, include_metadata=include_metadata)
    if not dc:
        raise HTTPException(status_code=404, detail=f"Data Contract {dc_id} not found")
    return dc

@router.get("/dcs")
@router.get("/dc", include_in_schema=False)
@router.get("/data-contracts", include_in_schema=False)
@router.get("/data-contract", include_in_schema=False)
async def list_data_contracts(
    dp_id: str = Query(None),
    include_metadata: bool = Query(False),
    repo: DataContractRepository = Depends(get_dc_repo)
):
    try:
        return await list_dcs(repo, dp_id=dp_id, include_metadata=include_metadata)
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
