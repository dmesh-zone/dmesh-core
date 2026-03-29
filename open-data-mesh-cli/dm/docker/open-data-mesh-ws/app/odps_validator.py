"""Validates an ODPS spec dict against the versioned ODPS JSON Schema from GitHub."""
from typing import Any

import jsonschema
import requests

SCHEMA_URL_TEMPLATE = (
    "https://raw.githubusercontent.com/bitol-io/open-data-product-standard"
    "/refs/heads/main/schema/odps-json-schema-{api_version}.json"
)


class SchemaFetchError(Exception):
    """Raised when the ODPS JSON Schema cannot be fetched from GitHub."""


def validate_spec(spec: dict[str, Any]) -> None:
    """Validate spec against the versioned ODPS JSON Schema.

    Raises:
        ValueError: if apiVersion is missing from spec.
        SchemaFetchError: if the schema cannot be fetched.
        jsonschema.ValidationError: if the spec is invalid.
    """
    api_version = spec.get("apiVersion")
    if not api_version:
        raise ValueError("apiVersion is required for schema validation")

    url = SCHEMA_URL_TEMPLATE.format(api_version=api_version)
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        raise SchemaFetchError(f"Network error fetching schema: {e}") from e

    if response.status_code != 200:
        raise SchemaFetchError(
            f"Schema not found for odps apiVersion={api_version} (HTTP {response.status_code}) URL={url}"
        )

    schema = response.json()
    jsonschema.validate(spec, schema)
