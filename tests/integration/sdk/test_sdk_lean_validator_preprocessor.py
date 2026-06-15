import pytest
from dmesh.sdk.lean_validator.validator import load_data
from dmesh.sdk.lean_validator.preprocessor import preprocess
import json

def test_preprocessor_publish_to_s3_spec():
    # Load the example file
    data = load_data("examples/lean-validator/dp-specs/valid/custom-odps-dataproduct-publish-to-s3-spec.yaml")
    
    # Run the preprocessor
    processed_data = preprocess(data)
    
    # Assertions
    # Check that inputPorts -> compounds -> publishToS3 has the injected values
    compounds_port = processed_data["inputPorts"][0]
    assert compounds_port["name"] == "compounds"
    
    publish_to_s3_prop = compounds_port["customProperties"][0]
    assert publish_to_s3_prop["property"] == "publishToS3"
    
    value = publish_to_s3_prop["value"]
    
    # Ensure _insertFrom is removed
    assert "_insertFrom" not in value
    
    # Ensure properties from publishToS3_inserts are injected
    assert value["sourceCatalog"] == "<my-source-catalog>"
    assert value["sourceSchema"] == "<my-source-schema>"
    assert value["s3Uri"] == "s3://<bucket>/<path>"
    assert value["s3Region"] == "<s3-region>"
    assert value["trigger"] == "schedule"
    assert value["schedule"] == "0 0 * * * *"
    
    # Original properties should still exist
    assert value["sourceTable"] == "<my-source-table>"
    assert value["targetTable"] == "<my-target-table>"
    
def test_preprocessor_missing_insert_id():
    data = {
        "customProperties": [
            {
                "property": "publishToS3",
                "value": {
                    "_insertFrom": "nonExistent"
                }
            }
        ]
    }
    
    with pytest.raises(ValueError, match="Could not find template for property 'publishToS3' with _insertId 'nonExistent'"):
        preprocess(data)
