import pytest
import jsonschema
from dmesh.sdk.lean_validator.validator import load_data, Validator
import glob

def get_valid_example_files():
    files = glob.glob("examples/lean-validator/dp-specs/valid/*.yaml") + glob.glob("examples/lean-validator/dp-specs/valid/*.yml") + glob.glob("examples/lean-validator/dp-specs/valid/*.json")
    return sorted(files)

def get_invalid_example_files():
    files = glob.glob("examples/lean-validator/dp-specs/invalid/*.yaml") + glob.glob("examples/lean-validator/dp-specs/invalid/*.yml") + glob.glob("examples/lean-validator/dp-specs/invalid/*.json")
    return sorted(files)

@pytest.fixture(scope="module")
def validator():
    return Validator()

@pytest.mark.parametrize("example_file", get_valid_example_files())
def test_valid_example_validation(validator, example_file):
    data = load_data(example_file)
    try:
        validator.validate_data(data)
    except jsonschema.exceptions.ValidationError as e:
        pytest.fail(f"Validation failed for valid example {example_file}: {e.message}")

@pytest.mark.parametrize("example_file", get_invalid_example_files())
def test_invalid_example_validation(validator, example_file):
    data = load_data(example_file)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate_data(data)
