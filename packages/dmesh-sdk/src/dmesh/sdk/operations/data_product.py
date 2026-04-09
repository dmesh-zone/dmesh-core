from typing import Any, List, Optional, Union
from dmesh.sdk.models import DataProduct
from dmesh.sdk.ports.repository import DataProductRepository
from dmesh.sdk.sdk import AsyncSDK, _RepoWrapper

async def create_dp(
    repo: DataProductRepository, 
    spec: dict[str, Any], 
    domain: Optional[str] = None, 
    name: Optional[str] = None, 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataProduct]:
    """Create a new data product."""
    return await AsyncSDK(_RepoWrapper(dp_repo=repo)).put_data_product(
        spec, domain=domain, name=name, include_metadata=include_metadata
    )

async def update_dp(
    repo: DataProductRepository, 
    spec: dict[str, Any], 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataProduct]:
    """Update an existing data product."""
    if not spec.get("id"):
        raise ValueError("Data product id is required for update")
    return await AsyncSDK(_RepoWrapper(dp_repo=repo)).put_data_product(
        spec, include_metadata=include_metadata
    )

async def get_dp(
    repo: DataProductRepository, 
    id: Optional[str] = None, 
    include_metadata: bool = False
) -> Optional[Union[dict, DataProduct]]:
    """Fetch a single data product by ID."""
    if not id:
        return None
    return await AsyncSDK(_RepoWrapper(dp_repo=repo)).get_data_product(id, include_metadata=include_metadata)

async def list_dps(
    repo: DataProductRepository, 
    domain: Optional[str] = None, 
    name: Optional[str] = None, 
    include_metadata: Optional[bool] = False
) -> List[Union[dict, DataProduct]]:
    """List data products with optional filtering."""
    return await AsyncSDK(_RepoWrapper(dp_repo=repo)).list_data_products(
        domain=domain, name=name, include_metadata=include_metadata
    )

async def delete_dp(repo: DataProductRepository, id: str) -> bool:
    """Delete a data product by ID."""
    return await AsyncSDK(_RepoWrapper(dp_repo=repo)).delete_data_product(id)
