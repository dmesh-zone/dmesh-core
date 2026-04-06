from typing import Any, List, Optional, Union
from uuid import UUID
import jsonschema.exceptions

from dmesh.sdk.models import DataProduct, DataProductValidationError
from dmesh.sdk.ports.repository import DataProductRepository
from dmesh.sdk.core.enricher import enrich_dp_spec
from dmesh.sdk.core.validator import validate_spec

async def create_dp(
    repo: DataProductRepository, 
    spec: dict[str, Any], 
    domain: Optional[str] = None, 
    name: Optional[str] = None, 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataProduct]:
    """Create a new data product."""
    try:
        merged_spec = {**spec}
        if domain: merged_spec["domain"] = domain
        if name: merged_spec["name"] = name
        
        enriched = enrich_dp_spec(merged_spec)
        validate_spec(enriched)
        
        dp = DataProduct(id=enriched["id"], specification=enriched)
        await repo.save(dp)
        
        return dp if include_metadata else dp.specification
    except jsonschema.exceptions.ValidationError as e:
        raise DataProductValidationError(f"Invalid Data Product specification: {e.message}") from e

async def update_dp(
    repo: DataProductRepository, 
    spec: dict[str, Any], 
    include_metadata: Optional[bool] = False
) -> Union[dict, DataProduct]:
    """Update an existing data product."""
    try:
        dp_id = spec.get("id")
        if not dp_id:
            raise ValueError("Data product id is required for update")
        
        enriched = enrich_dp_spec(spec)
        validate_spec(enriched)
        
        dp = DataProduct(id=dp_id, specification=enriched)
        await repo.save(dp)
        
        return dp if include_metadata else dp.specification
    except jsonschema.exceptions.ValidationError as e:
        raise DataProductValidationError(f"Invalid Data Product specification: {e.message}") from e

async def get_dp(
    repo: DataProductRepository, 
    id: Optional[str] = None, 
    include_metadata: bool = False
) -> Optional[Union[dict, DataProduct]]:
    """Fetch a single data product by ID."""
    if id:
        dp = await repo.get(UUID(id))
        if dp:
            return dp if include_metadata else dp.specification
    return None

async def list_dps(
    repo: DataProductRepository, 
    domain: Optional[str] = None, 
    name: Optional[str] = None, 
    include_metadata: Optional[bool] = False
) -> List[Union[dict, DataProduct]]:
    """List data products with optional filtering."""
    results = await repo.list(domain=domain, name=name)
    if include_metadata:
        return results
    return [dp.specification for dp in results]

async def delete_dp(repo: DataProductRepository, id: str) -> bool:
    """Delete a data product by ID."""
    return await repo.delete(UUID(id))
