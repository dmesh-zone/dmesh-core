"""Unit tests for odps_validator.py."""
from unittest.mock import MagicMock, patch

import jsonschema
import pytest

from app.odps_validator import SchemaFetchError, validate_spec

MINIMAL_SPEC = {
    "apiVersion": "v3.0.0",
    "domain": "finance",
    "name": "transactions",
    "version": "1.0.0",
}

MINIMAL_SCHEMA = {"type": "object"}


def test_validate_spec_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MINIMAL_SCHEMA
    with patch("app.odps_validator.requests.get", return_value=mock_response):
        validate_spec(MINIMAL_SPEC)  # should not raise


def test_validate_spec_fetch_error_on_network_failure():
    import requests as req
    with patch("app.odps_validator.requests.get", side_effect=req.RequestException("timeout")):
        with pytest.raises(SchemaFetchError, match="Network error"):
            validate_spec(MINIMAL_SPEC)


def test_validate_spec_fetch_error_on_non_200():
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch("app.odps_validator.requests.get", return_value=mock_response):
        with pytest.raises(SchemaFetchError, match="HTTP 404"):
            validate_spec(MINIMAL_SPEC)


def test_validate_spec_raises_validation_error_on_invalid_spec():
    strict_schema = {
        "type": "object",
        "required": ["mustHaveThis"],
        "properties": {"mustHaveThis": {"type": "string"}},
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = strict_schema
    with patch("app.odps_validator.requests.get", return_value=mock_response):
        with pytest.raises(jsonschema.ValidationError):
            validate_spec(MINIMAL_SPEC)


def test_validate_spec_raises_value_error_on_missing_api_version():
    spec = {"domain": "finance", "name": "transactions", "version": "1.0.0"}
    with pytest.raises(ValueError, match="apiVersion"):
        validate_spec(spec)
