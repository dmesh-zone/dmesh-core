import importlib.resources
import json
import re
import copy
from pathlib import Path
from typing import Any
from uuid import UUID
from datetime import datetime
import functools

import jsonschema
from jsonschema.validators import validator_for
import requests

SCHEMA_URLS = {
    "DataProduct": "https://raw.githubusercontent.com/bitol-io/open-data-product-standard/refs/heads/main/schema/odps-json-schema-{api_version}.json",
    "DataContract": "https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/refs/heads/main/schema/odcs-json-schema-{api_version}.json",
}

SCHEMA_MAP = {
    "DataProduct": "odps-{api_version}.json",
    "DataContract": "odcs-{api_version}.json",
}


class SchemaFetchError(Exception):
    """Raised when the Bitol JSON Schema cannot be fetched."""


def _stringify_spec(spec: Any) -> Any:
    """Recursively convert UUID and datetime objects to strings."""
    if isinstance(spec, dict):
        return {k: _stringify_spec(v) for k, v in spec.items()}
    elif isinstance(spec, list):
        return [_stringify_spec(v) for v in spec]
    elif isinstance(spec, (UUID, datetime)):
        return str(spec)
    return spec


@functools.lru_cache(maxsize=32)
def _get_validator(kind: str, api_version: str) -> Any:
    # Normalize version: strip 'v' prefix for local file lookup
    clean_version = api_version[1:] if api_version.startswith("v") else api_version

    # 1. Try local lookup
    local_name_template = SCHEMA_MAP.get(kind, "odps-{api_version}.json")
    local_filename = local_name_template.format(api_version=clean_version)
    
    try:
        pkg_path = importlib.resources.files("dmesh.sdk.schemas")
        schema_file = pkg_path / local_filename
        
        if schema_file.is_file():
            with schema_file.open("r", encoding="utf-8") as f:
                schema = json.load(f)
                ValidatorClass = validator_for(schema)
                ValidatorClass.check_schema(schema)
                return ValidatorClass(schema)
    except Exception:
        # Only fallback if the file itself was missing or malformed
        pass

    # 2. Try remote lookup (fallback)
    template = SCHEMA_URLS.get(kind, SCHEMA_URLS["DataProduct"])
    versions_to_try = [api_version, clean_version]
    if not api_version.startswith("v"):
        versions_to_try.append(f"v{api_version}")

    last_error = None
    for v in versions_to_try:
        url = template.format(api_version=v)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                schema = response.json()
                ValidatorClass = validator_for(schema)
                ValidatorClass.check_schema(schema)
                return ValidatorClass(schema)
            last_error = f"HTTP {response.status_code} at {url}"
        except requests.RequestException as e:
            last_error = str(e)

    raise SchemaFetchError(
        f"Schema not found for {kind} apiVersion={api_version} ({last_error})"
    )


def validate_spec(spec: dict[str, Any]) -> None:
    """Validate spec against the versioned Bitol JSON Schema.

    Prioritizes local schemas in the package over external GitHub URLs.

    Raises:
        ValueError: if apiVersion or kind is missing from spec.
        SchemaFetchError: if the schema cannot be fetched locally or remotely.
        jsonschema.ValidationError: if the spec is invalid.
    """
    api_version = spec.get("apiVersion")
    kind = spec.get("kind")
    if not api_version:
        raise ValueError("apiVersion is required for schema validation")
    if not re.match(r"^v\d+\.\d+\.\d+$", api_version):
        raise ValueError(f"invalid apiVersion input \"{api_version}\" expected format: vX.Y.Z")

    if not kind:
        # Heuristic to detect kind if not specified
        if "domain" in spec or "payload" in spec:
            kind = "DataProduct"
        elif "specification" in spec or "info" in spec:
            kind = "DataContract"
        else:
            # Default to DataProduct if ambiguous
            kind = "DataProduct"

    # Convert UUIDs and datetimes to strings for JSON schema validation
    serializable_spec = _stringify_spec(spec)

    validator = _get_validator(kind, api_version)
    validator.validate(serializable_spec)
