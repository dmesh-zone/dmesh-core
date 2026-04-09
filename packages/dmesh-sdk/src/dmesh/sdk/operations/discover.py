from typing import Any, List, Optional, Union
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
from dmesh.sdk.sdk import AsyncSDK, _RepoWrapper

async def discover(
    dp_repo: DataProductRepository,
    dc_repo: DataContractRepository,
    dp_id: Optional[str] = None,
    domain: Optional[str] = None,
    name: Optional[str] = None,
    include_metadata: Optional[bool] = False,
    include_metadata_in_response: Optional[bool] = False
) -> List[Union[dict, DataProduct, DataContract]]:
    """Discovery by ID OR by domain and name. Returns a flat list of DataProduct and DataContract objects."""
    # Note: include_metadata_in_response maps to include_metadata in SDK
    incl = include_metadata or include_metadata_in_response
    return await AsyncSDK(_RepoWrapper(dp_repo=dp_repo, dc_repo=dc_repo)).discover(
        dp_id=dp_id, domain=domain, name=name, include_metadata=incl
    )
