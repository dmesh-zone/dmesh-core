"""Enriches an ODPS spec dict before persistence."""
from typing import Any

from dmesh.sdk.core.id_generator import make_dp_id


def enrich_dp_spec(spec: dict[str, Any]) -> dict[str, Any]:
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
    # Default outputPorts version to "v1" if missing
    if "outputPorts" in enriched and isinstance(enriched["outputPorts"], list):
        new_ports = []
        for port in enriched["outputPorts"]:
            if isinstance(port, dict):
                p = dict(port)
                p.setdefault("version", "v1")
                new_ports.append(p)
            else:
                new_ports.append(port)
        enriched["outputPorts"] = new_ports
    
    enriched["id"] = make_dp_id(
        enriched.get("domain", ""),
        enriched.get("name", ""),
        enriched.get("version"),
    )
    return enriched


def enrich_dc_spec(spec: dict[str, Any], dp_spec: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a new DataContract spec with defaults applied.

    If a parent Data Product spec is provided, inherit common contextual values.
    Does not mutate the input dict.
    """
    enriched = dict(spec)
    enriched.setdefault("apiVersion", "v3.1.0")
    enriched.setdefault("kind", "DataContract")
    enriched.setdefault("version", "v1.0.0")
    enriched.setdefault("status", "draft")

    if dp_spec is not None:
        if "dataProduct" not in enriched and dp_spec.get("name"):
            enriched["dataProduct"] = dp_spec["name"]
        if "domain" not in enriched and dp_spec.get("domain"):
            enriched["domain"] = dp_spec["domain"]

    return enriched
