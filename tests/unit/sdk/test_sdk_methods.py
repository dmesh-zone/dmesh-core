import pytest
from dmesh.sdk import AsyncSDK
from unittest.mock import MagicMock

def test_get_custom_property_value():
    custom_props = [
        {"property": "p1", "value": "v1"},
        {"property": "dataProductId", "value": "uuid-123"},
        {"property": "tier", "value": "sourceAligned"}
    ]
    
    # Test existing property (positional)
    assert AsyncSDK.get_custom_property_value(custom_props, "p1") == "v1"
    assert AsyncSDK.get_custom_property_value(custom_props, "dataProductId") == "uuid-123"
    assert AsyncSDK.get_custom_property_value(custom_props, "tier") == "sourceAligned"
    
    # Test with spec
    spec = {
        "domain": "finance",
        "customProperties": custom_props
    }
    assert AsyncSDK.get_custom_property_value(spec, "dataProductId") == "uuid-123"
    
    # Test non-existing property
    assert AsyncSDK.get_custom_property_value(custom_props, "nonexistent") is None
    
    # Test empty list
    assert AsyncSDK.get_custom_property_value([], "any") is None
    
    # Test malformed property (missing 'property' or 'value' key)
    malformed_props = [{"not_property": "p1", "value": "v1"}]
    assert AsyncSDK.get_custom_property_value(malformed_props, "p1") is None

def test_set_custom_property_value():
    custom_props = [
        {"property": "p1", "value": "v1"}
    ]
    
    # Test update existing (list)
    AsyncSDK.set_custom_property_value(custom_props, "p1", "v2")
    assert custom_props[0]["value"] == "v2"
    
    # Test add new (list)
    AsyncSDK.set_custom_property_value(custom_props, "p2", "v3")
    assert len(custom_props) == 2
    assert custom_props[1]["property"] == "p2"
    assert custom_props[1]["value"] == "v3"
    
    # Test update existing (spec)
    spec = {"domain": "f", "customProperties": [{"property": "p1", "value": "v1"}]}
    AsyncSDK.set_custom_property_value(spec, "p1", "new_val")
    assert spec["customProperties"][0]["value"] == "new_val"
    
    # Test add new (spec)
    AsyncSDK.set_custom_property_value(spec, "p2", "val2")
    assert any(p["property"] == "p2" and p["value"] == "val2" for p in spec["customProperties"])
    
    # Test create customProperties if missing (spec)
    empty_spec = {"domain": "f"}
    AsyncSDK.set_custom_property_value(empty_spec, "p1", "v1")
    assert "customProperties" in empty_spec
    assert empty_spec["customProperties"][0]["property"] == "p1"
