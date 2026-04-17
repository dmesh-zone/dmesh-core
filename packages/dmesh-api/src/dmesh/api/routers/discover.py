from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
from dmesh.sdk import discover
from dmesh.api.dependencies import get_dp_repo, get_dc_repo
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

discover_router = APIRouter(tags=["Discovery"])

@discover_router.get("/discover")
async def get_discover(
    domain: str = Query(None),
    name: str = Query(None),
    dp_id: str = Query(None),
    dp_repo: DataProductRepository = Depends(get_dp_repo),
    dc_repo: DataContractRepository = Depends(get_dc_repo)
):
    """
    Discover Data Products and their associated Data Contracts.
    Can filter by domain and name, or by a specific Data Product ID.
    """
    return await discover(
        dp_repo=dp_repo, 
        dc_repo=dc_repo, 
        domain=domain, 
        name=name, 
        dp_id=dp_id
    )
