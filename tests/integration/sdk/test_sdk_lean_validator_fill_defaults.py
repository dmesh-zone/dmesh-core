from dmesh.sdk.lean_validator.preprocessor import preprocess
from dmesh.sdk.lean_validator.validator import load_data

def find_property_value(data, prop_name):
    from dmesh.sdk.lean_validator.preprocessor import get_custom_properties
    for custom_props in get_custom_properties(data):
        for prop in custom_props:
            if isinstance(prop, dict) and prop.get("property") == prop_name:
                return prop.get("value")
                
    # Fallback to schema default if completely omitted
    import os, json
    schema_path = os.path.join("examples/lean-validator/schemas/custom-properties", f"{prop_name}.json")
    if os.path.exists(schema_path):
        try:
            with open(schema_path) as f:
                schema = json.load(f)
            return schema.get("default")
        except Exception:
            pass
    return None

def test_fill_defaults_from_schema():
    # Load the YAML which now explicitly omits the 'format' field
    data = load_data("examples/lean-validator/dp-specs/valid/custom-odps-datamart-sample-spec.yaml")
    
    # Process the data (expands _inserts and applies schema defaults)
    processed_data = preprocess(data)
    
    compounds_port = processed_data["inputPorts"][0]
    publish_to_s3_prop = compounds_port["customProperties"][0]
    
    assert publish_to_s3_prop["property"] == "publishToS3"
    
    value = publish_to_s3_prop["value"]
    
    # Assert that the default 'format' from the JSON schema was dynamically injected
    assert "format" in value, "The 'format' property was not injected!"
    assert value["format"] == "deltaLake", f"Expected format 'deltaLake', got {value['format']}"

def test_enterprise_data_product_datamart():
    data = load_data("examples/lean-validator/dp-specs/valid/custom-odps-datamart-sample-spec.yaml")
    processed = preprocess(data)
    val = find_property_value(processed, "enterpriseDataProduct")
    assert val is False, f"Expected False, got {val}"

def test_enterprise_data_product_dataproduct():
    data = load_data("examples/lean-validator/dp-specs/valid/custom-odps-dataproduct-sample-spec.yaml")
    processed = preprocess(data)
    val = find_property_value(processed, "enterpriseDataProduct")
    assert val is True, f"Expected True, got {val}"
