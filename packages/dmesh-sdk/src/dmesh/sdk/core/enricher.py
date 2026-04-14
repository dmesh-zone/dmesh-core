"""Enriches an ODPS spec dict before persistence."""
from typing import Any

from dmesh.sdk.core.id_generator import make_dp_id, IDGenerator


def enrich_dp_spec(
    spec: dict[str, Any], 
    id_generator: IDGenerator | None = None,
    status_default: str = "draft"
) -> dict[str, Any]:
    """Return a new dict with deterministic id injected and defaults applied.

    The id is derived from domain + name + version (deterministic).
    Does not mutate the input dict.
    """
    enriched = dict(spec)
    
    # Apply defaults if missing
    enriched.setdefault("apiVersion", "v1.0.0")
    enriched.setdefault("kind", "DataProduct")
    enriched.setdefault("version", "v1.0.0")
    enriched.setdefault("status", status_default)
    # Basic enrichment moved to SDK enrichment methods if needed
    
    if id_generator:
        enriched["id"] = id_generator.make_dp_id(enriched)
    else:
        enriched["id"] = make_dp_id(enriched)
        
    return enriched


def enrich_dc_spec(
    spec: dict[str, Any], 
    dp_spec: dict[str, Any] | None = None,
    status_default: str = "draft"
) -> dict[str, Any]:
    """Return a new DataContract spec with defaults applied.

    If a parent Data Product spec is provided, inherit common contextual values.
    Does not mutate the input dict.
    """
    enriched = dict(spec)
    enriched.setdefault("apiVersion", "v3.1.0")
    enriched.setdefault("kind", "DataContract")
    enriched.setdefault("version", "v1.0.0")
    enriched.setdefault("status", status_default)

    if dp_spec is not None:
        if "dataProduct" not in enriched and dp_spec.get("name"):
            enriched["dataProduct"] = dp_spec["name"]
        if "domain" not in enriched and dp_spec.get("domain"):
            enriched["domain"] = dp_spec["domain"]

    return enriched
