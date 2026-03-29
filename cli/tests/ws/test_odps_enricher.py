"""Unit and property-based tests for odps_enricher.py."""
import uuid
from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.odps_enricher import enrich_spec


BASE_SPEC: dict[str, Any] = {
    "apiVersion": "v3.0.0",
    "domain": "finance",
    "name": "transactions",
    "version": "1.0.0",
}


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_enrich_spec_injects_uuid():
    result = enrich_spec(BASE_SPEC)
    assert "id" in result
    uuid.UUID(result["id"])  # raises if not valid UUID


def test_enrich_spec_sets_status_default():
    result = enrich_spec(BASE_SPEC)
    assert result["status"] == "draft"


def test_enrich_spec_preserves_existing_status():
    spec = {**BASE_SPEC, "status": "published"}
    result = enrich_spec(spec)
    assert result["status"] == "published"


def test_enrich_spec_preserves_other_fields():
    spec = {**BASE_SPEC, "owner": "team-alpha", "tags": ["finance"]}
    result = enrich_spec(spec)
    assert result["owner"] == "team-alpha"
    assert result["tags"] == ["finance"]


def test_enrich_spec_does_not_mutate_input():
    spec = dict(BASE_SPEC)
    original = dict(spec)
    enrich_spec(spec)
    assert spec == original


def test_enrich_spec_overwrites_existing_id():
    # id is always recomputed deterministically from domain/name/version
    existing_id = str(uuid.uuid4())
    spec = {**BASE_SPEC, "id": existing_id}
    result = enrich_spec(spec)
    # The deterministic id replaces whatever was in the spec
    from app.id_generator import make_dp_id
    expected = make_dp_id(BASE_SPEC["domain"], BASE_SPEC["name"], BASE_SPEC["version"])
    assert result["id"] == expected


# ---------------------------------------------------------------------------
# Property-based tests
# Feature: data-mesh-data-product-create
# ---------------------------------------------------------------------------

@given(spec=st.fixed_dictionaries({
    "apiVersion": st.text(min_size=1),
    "domain": st.text(min_size=1),
    "name": st.text(min_size=1),
    "version": st.text(min_size=1),
}))
@settings(max_examples=100)
def test_enrich_spec_always_sets_valid_uuid(spec):
    # Property 8.1: enrich_spec always sets id to a valid UUID5 string
    result = enrich_spec(spec)
    parsed = uuid.UUID(result["id"])
    assert parsed.version == 5  # deterministic UUID5


@given(spec=st.fixed_dictionaries({
    "apiVersion": st.text(min_size=1),
    "domain": st.text(min_size=1),
    "name": st.text(min_size=1),
    "version": st.text(min_size=1),
}))
@settings(max_examples=100)
def test_enrich_spec_sets_status_draft_when_absent(spec):
    # Property 8.2: enrich_spec always sets status="draft" when status absent
    assert "status" not in spec
    result = enrich_spec(spec)
    assert result["status"] == "draft"


@given(spec=st.fixed_dictionaries({
    "apiVersion": st.text(min_size=1),
    "domain": st.text(min_size=1),
    "name": st.text(min_size=1),
    "version": st.text(min_size=1),
}))
@settings(max_examples=100)
def test_enrich_spec_never_mutates_input(spec):
    # Property 8.4: enrich_spec never mutates the input dict
    original = dict(spec)
    enrich_spec(spec)
    assert spec == original
