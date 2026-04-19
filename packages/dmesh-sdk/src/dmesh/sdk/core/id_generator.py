"""Determininstic ID generation interface and default implementations."""
import os
import uuid
from typing import Any, Protocol, runtime_checkable

# Fixed namespace for all dmesh IDs
_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # NAMESPACE_DNS

DEFAULT_DP_SCHEME = "DataProduct/{domain}/{name}"
DEFAULT_DC_SCHEME = "DataContract/{domain}/{name}/{dc_index}"
DEFAULT_DUA_SCHEME = "DataUsageAgreement/{provider_id}/{consumer_id}/{start_date}"


@runtime_checkable
class IDGenerator(Protocol):
    """Protocol for generating determininstic IDs for Data Mesh entities."""

    def make_dp_id(self, spec: dict[str, Any]) -> uuid.UUID:
        """Generate a deterministic ID for a data product spec."""
        ...

    def make_dc_id(self, spec: dict[str, Any]) -> uuid.UUID:
        """Generate a deterministic ID for a data contract spec."""
        ...

    def make_dua_id(self, spec: dict[str, Any]) -> uuid.UUID:
        """Generate a deterministic ID for a data usage agreement spec."""
        ...


class DefaultIDGenerator:
    """Default implementation using UUID5 and configurable schemes."""

    def _scheme(self, env_var: str, default: str) -> str:
        return os.environ.get(env_var, default)

    def make_dp_id(self, spec: dict[str, Any]) -> uuid.UUID:
        """Generate a deterministic ID for a data product.
        
        Input is a dictionary containing at least 'domain', 'name' and 'version'.
        """
        domain = spec.get("domain", "")
        name = spec.get("name", "")
        version = spec.get("version", "v1.0.0")

        scheme = self._scheme("DP_ID_SCHEME", DEFAULT_DP_SCHEME)
        try:
            key = scheme.format(domain=domain, name=name, version=version)
        except KeyError:
            key = f"DataProduct/{domain}/{name}/{version}"
        return uuid.uuid5(_NAMESPACE, key)

    def make_dc_id(self, spec: dict[str, Any]) -> uuid.UUID:
        """Generate a deterministic ID for a data contract.

        Input is a dictionary containing parent information ('domain', 'dataProduct')
        and an internal '_dc_index' representing the sequence of contracts for the product
        (0-based: first DC gets index 0).
        """
        domain = spec.get("domain", "")
        name = spec.get("dataProduct", "")
        dc_index = spec.get("_dc_index", 0)

        scheme = self._scheme("DC_ID_SCHEME", DEFAULT_DC_SCHEME)
        try:
            key = scheme.format(
                domain=domain,
                name=name,
                dc_index=dc_index,
            )
        except KeyError:
            key = f"DataContract/{domain}/{name}/{dc_index}"
        return uuid.uuid5(_NAMESPACE, key)

    def make_dua_id(self, spec: dict[str, Any]) -> uuid.UUID:
        """Generate a deterministic ID for a data usage agreement.

        Input is a dictionary containing 'provider' and 'consumer' blocks,
        and an 'info' block with a 'startDate'.
        """
        provider_id = spec.get("provider", {}).get("dataProductId", "")
        consumer_id = spec.get("consumer", {}).get("dataProductId", "")
        info = spec.get("info", {})
        start_date = info.get("startDate", "")

        scheme = self._scheme("DUA_ID_SCHEME", DEFAULT_DUA_SCHEME)
        try:
            key = scheme.format(
                provider_id=provider_id,
                consumer_id=consumer_id,
                start_date=start_date,
            )
        except KeyError:
            key = f"DataUsageAgreement/{provider_id}/{consumer_id}/{start_date}"
        return uuid.uuid5(_NAMESPACE, key)


# Global instance for legacy function-based access
_generator: IDGenerator = DefaultIDGenerator()


def set_generator(generator: IDGenerator):
    """Set the global ID generator instance."""
    global _generator
    _generator = generator


def get_generator() -> IDGenerator:
    """Get the current global ID generator instance."""
    return _generator


def make_dp_id(spec: dict[str, Any]) -> uuid.UUID:
    """Generate a deterministic ID for a data product using the configured generator."""
    return _generator.make_dp_id(spec)


def make_dc_id(spec: dict[str, Any]) -> uuid.UUID:
    """Generate a deterministic ID for a data contract using the configured generator."""
    return _generator.make_dc_id(spec)


def make_dua_id(spec: dict[str, Any]) -> uuid.UUID:
    """Generate a deterministic ID for a data usage agreement using the configured generator."""
    return _generator.make_dua_id(spec)
