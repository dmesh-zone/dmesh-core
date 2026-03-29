"""Deterministic UUID5 generation for data products and data contracts."""
import os
import uuid

# Fixed namespace for all open-data-mesh IDs
_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # NAMESPACE_DNS

DEFAULT_DP_SCHEME = "DataProduct/{domain}/{name}/{version}"
DEFAULT_DC_SCHEME = "DataContract/{domain}/{name}/{version}/{dc_index}"


def _scheme(env_var: str, default: str) -> str:
    return os.environ.get(env_var, default)


def make_dp_id(domain: str, name: str, version: str) -> str:
    """Generate a deterministic UUID5 for a data product."""
    scheme = _scheme("DP_ID_SCHEME", DEFAULT_DP_SCHEME)
    try:
        key = scheme.format(domain=domain, name=name, version=version)
    except KeyError as e:
        # Fallback if scheme is malformed
        key = f"DataProduct/{domain}/{name}/{version}"
    return str(uuid.uuid5(_NAMESPACE, key))


def make_dc_id(dp_domain: str, dp_name: str, dp_version: str, dc_index: int) -> str:
    """Generate a deterministic UUID5 for a data contract.

    dc_index is the count of existing data contracts for the parent DP
    at creation time (0-based: first DC gets index 0).
    """
    scheme = _scheme("DC_ID_SCHEME", DEFAULT_DC_SCHEME)
    try:
        key = scheme.format(
            domain=dp_domain,
            name=dp_name,
            version=dp_version,
            dc_index=dc_index,
        )
    except KeyError as e:
        # Fallback if scheme is malformed
        key = f"DataContract/{dp_domain}/{dp_name}/{dp_version}/{dc_index}"
    return str(uuid.uuid5(_NAMESPACE, key))
