from typing import Any, List, Optional, Union
from uuid import UUID
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

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
    results = []
    dps = []
    
    if dp_id:
        dp = await dp_repo.get(UUID(dp_id))
        if dp is not None:
            if not include_metadata_in_response:
                dps.append(dp.specification)
            else:
                dps.append(dp)
    elif domain and name:
        dps_found = await dp_repo.list(domain=domain, name=name)
        if not include_metadata_in_response:
            dps = [dp.specification for dp in dps_found]
        else:
            dps = dps_found
    
    for dp_item in dps:
        results.append(dp_item)
        # Identify DP ID for contract lookup
        current_dp_id = dp_item["id"] if isinstance(dp_item, dict) else dp_item.id
        
        # Look up contracts for this DP
        dcs = await dc_repo.list(dp_id=current_dp_id)
        if not include_metadata_in_response:
            results.extend([dc.specification for dc in dcs])
        else:
            results.extend(dcs)
            
    return results
