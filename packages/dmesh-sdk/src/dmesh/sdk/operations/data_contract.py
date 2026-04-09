from typing import Any, List, Optional, Union
from dmesh.sdk.models import DataContract
from dmesh.sdk.ports.repository import DataContractRepository, DataProductRepository
from dmesh.sdk.sdk import AsyncSDK, _RepoWrapper

async def create_dc(
    repo: DataContractRepository, 
    dp_repo: DataProductRepository,
    spec: dict[str, Any], 
    dp_id: str, 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataContract]:
    """Create a data contract for a given data product."""
    return await AsyncSDK(_RepoWrapper(dp_repo=dp_repo, dc_repo=repo)).put_data_contract(
        spec, dp_id=dp_id, include_metadata=include_metadata
    )

async def update_dc(
    repo: DataContractRepository, 
    spec: dict[str, Any], 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataContract]:
    """Update an existing data contract."""
    if not spec.get("id"):
        raise ValueError("Data contract id is required for update")
    return await AsyncSDK(_RepoWrapper(dc_repo=repo)).put_data_contract(
        spec, include_metadata=include_metadata
    )

async def patch_dc(
    repo: DataContractRepository, 
    spec: dict[str, Any], 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataContract]:
    """Patch an existing data contract."""
    dc_id = spec.get("id")
    if not dc_id:
        raise ValueError("Data contract id is required for patch")
    return await AsyncSDK(_RepoWrapper(dc_repo=repo)).patch_data_contract(
        dc_id, spec, include_metadata=include_metadata
    )

async def get_dc(
    repo: DataContractRepository, 
    id: str, 
    include_metadata: Optional[bool] = False
) -> Optional[Union[dict, DataContract]]:
    """Fetch a single data contract by ID."""
    return await AsyncSDK(_RepoWrapper(dc_repo=repo)).get_data_contract(id, include_metadata=include_metadata)

async def list_dcs(
    repo: DataContractRepository, 
    dp_id: Optional[str] = None, 
    include_metadata: Optional[bool] = False
) -> List[Union[dict, DataContract]]:
    """List data contracts, optionally filtering by parent data product."""
    return await AsyncSDK(_RepoWrapper(dc_repo=repo)).list_data_contracts(
        dp_id=dp_id, include_metadata=include_metadata
    )

async def delete_dc(repo: DataContractRepository, id: str) -> bool:
    """Delete a data contract by ID."""
    return await AsyncSDK(_RepoWrapper(dc_repo=repo)).delete_data_contract(id)
