from typing import Any, List, Optional, Union
from uuid import UUID
import jsonschema.exceptions

from dmesh.sdk.models import DataContract, DataContractValidationError
from dmesh.sdk.ports.repository import DataContractRepository, DataProductRepository
from dmesh.sdk.core.enricher import enrich_dc_spec
from dmesh.sdk.core.validator import validate_spec
from dmesh.sdk.core.id_generator import make_dc_id

async def create_dc(
    repo: DataContractRepository, 
    dp_repo: DataProductRepository,
    spec: dict[str, Any], 
    dp_id: str, 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataContract]:
    """Create a data contract for a given data product."""
    try:
        dp = await dp_repo.get(UUID(dp_id))
        if not dp:
            raise ValueError(f"Parent Data Product {dp_id} not found")
        
        existing_dcs = await repo.list(dp_id=dp_id)
        dc_index = len(existing_dcs)
        
        dc_id = make_dc_id(dp.domain, dp.name, dp.version, dc_index)
        enriched_dc = enrich_dc_spec({**spec, "id": dc_id}, dp_spec=dp.specification)
        validate_spec(enriched_dc)
        
        dc = DataContract(id=dc_id, data_product_id=dp_id, specification=enriched_dc)
        await repo.save(dc)
        
        return dc if include_metadata else dc.specification
    except jsonschema.exceptions.ValidationError as e:
        raise DataContractValidationError(f"Invalid Data Contract specification: {e.message}") from e

async def update_dc(
    repo: DataContractRepository, 
    spec: dict[str, Any], 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataContract]:
    """Update an existing data contract."""
    try:
        dc_id = spec.get("id")
        if not dc_id:
            raise ValueError("Data contract id is required for update")
        
        existing = await repo.get(UUID(dc_id))
        if not existing:
            raise ValueError(f"Data contract {dc_id} not found")
        
        enriched_dc = enrich_dc_spec({**spec, "id": dc_id})
        validate_spec(enriched_dc)
        dc = DataContract(id=dc_id, data_product_id=existing.data_product_id, specification=enriched_dc)
        await repo.save(dc)
        
        return dc if include_metadata else dc.specification
    except jsonschema.exceptions.ValidationError as e:
        raise DataContractValidationError(f"Invalid Data Contract specification: {e.message}") from e

async def patch_dc(
    repo: DataContractRepository, 
    spec: dict[str, Any], 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataContract]:
    """Patch an existing data contract."""
    try:
        dc_id = spec.get("id")
        if not dc_id:
            raise ValueError("Data contract id is required for patch")
        
        current_full = await repo.get(UUID(dc_id))
        if not current_full:
            raise ValueError(f"Data contract {dc_id} not found")
        
        current_spec = current_full.specification.copy()

        spec_to_update = current_spec.copy()
        for key, value in spec.items():
            if key == "customProperties" and key in spec_to_update:
                spec_to_update[key] = spec_to_update[key] + value
            else:
                spec_to_update[key] = value
        
        return await update_dc(repo, spec_to_update, include_metadata=include_metadata)
    except jsonschema.exceptions.ValidationError as e:
        raise DataContractValidationError(f"Invalid Data Contract specification: {e.message}") from e

async def get_dc(
    repo: DataContractRepository, 
    id: str, 
    include_metadata: Optional[bool] = False
) -> Optional[Union[dict, DataContract]]:
    """Fetch a single data contract by ID."""
    dc = await repo.get(UUID(id))
    if dc:
        return dc if include_metadata else dc.specification
    return None

async def list_dcs(
    repo: DataContractRepository, 
    dp_id: Optional[str] = None, 
    include_metadata: Optional[bool] = False
) -> List[Union[dict, DataContract]]:
    """List data contracts, optionally filtering by parent data product."""
    results = await repo.list(dp_id=dp_id)
    if include_metadata:
        return results
    return [dc.specification for dc in results]

async def delete_dc(repo: DataContractRepository, id: str) -> bool:
    """Delete a data contract by ID."""
    return await repo.delete(UUID(id))
