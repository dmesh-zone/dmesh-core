from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
from dmesh.sdk import discover
from dmesh.api.dependencies import get_dp_repo, get_dc_repo
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
import httpx
import asyncio
from dmesh.sdk.config import get_settings
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

@discover_router.get("/discover-multi-environment")
async def get_discover_multi_environment(
    domain: str = Query(None),
    name: str = Query(None),
    dp_id: str = Query(None)
):
    """
    Discover Data Products and their associated Data Contracts across multiple environments.
    """
    settings = get_settings()
    environments = settings.api.environments
    
    if not environments:
        return []
        
    async def fetch_env(env_name: str, url: str) -> dict:
        params = {}
        if domain: params["domain"] = domain
        if name: params["name"] = name
        if dp_id: params["dp_id"] = dp_id
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    return {"env": env_name, "data": response.json()}
                else:
                    return {"env": env_name, "data": [], "errorMessage": f"HTTP code {response.status_code}"}
        except Exception as e:
            return {"env": env_name, "data": [], "errorMessage": str(e)}

    tasks = [fetch_env(env, url) for env, url in environments.items()]
    results = await asyncio.gather(*tasks)
    
    return results
