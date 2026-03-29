from typing import List, Any
from fastapi import APIRouter, Request, HTTPException, Query
from open_data_mesh_sdk.core.service import DataMeshService

router = APIRouter()

@router.post("/dps/{dp_id}/dcs", status_code=201)
def create_dc(request: Request, dp_id: str, spec: dict):
    service: DataMeshService = request.app.state.service
    try:
        dc = service.create_data_contract(dp_id, spec)
        return dc.specification
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dcs/{dc_id}")
def get_dc(request: Request, dc_id: str):
    service: DataMeshService = request.app.state.service
    dc = service.get_data_contract(dc_id)
    if not dc:
        raise HTTPException(status_code=404, detail=f"Data Contract {dc_id} not found")
    return dc.specification

@router.get("/dcs")
def list_dcs(request: Request, dp_id: str = Query(None)):
    service: DataMeshService = request.app.state.service
    dcs = service.list_data_contracts(dp_id=dp_id)
    return [dc.specification for dc in dcs]
