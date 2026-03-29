"""Enriches an ODPS spec dict before persistence."""
from typing import Any

from open_data_mesh_sdk.core.id_generator import make_dp_id


def enrich_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Return a new dict with deterministic id injected and defaults applied.

    The id is derived from domain + name + version (deterministic).
    Does not mutate the input dict.
    """
    enriched = dict(spec)
    
    # Apply defaults if missing
    enriched.setdefault("apiVersion", "v1.0.0")
    enriched.setdefault("kind", "DataProduct")
    enriched.setdefault("version", "v1.0.0")
    enriched.setdefault("status", "draft")
    
    enriched["id"] = make_dp_id(
        enriched.get("domain", ""),
        enriched.get("name", ""),
        enriched.get("version"),
    )
    return enriched
