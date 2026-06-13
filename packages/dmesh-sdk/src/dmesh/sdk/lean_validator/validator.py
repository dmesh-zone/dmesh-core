import argparse
import json
import yaml
import jsonschema
from jsonschema import validate, ValidationError
import sys
import pathlib
import urllib.request
import referencing
import referencing.exceptions

def load_data(file_path):
    with open(file_path, 'r') as f:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(f)
        elif file_path.endswith('.json'):
            return json.load(f)
        else:
            raise ValueError("Unsupported file format. Please use .json, .yaml, or .yml")

def load_schema(schema_path):
    with open(schema_path, 'r') as f:
        return json.load(f)

def retrieve_from_filesystem(uri: str):
    if uri.startswith("file://"):
        req = urllib.request.Request(uri)
        with urllib.request.urlopen(req) as response:
            return referencing.Resource.from_contents(json.loads(response.read().decode("utf-8")))
    raise referencing.exceptions.NoSuchResource(ref=uri)  # type: ignore

class Validator:
    def __init__(self, schema_path="examples/lean-validator/schemas/custom-odps-json-schema-v1.0.0.json", custom_properties_dir="examples/lean-validator/schemas/custom-properties"):
        self.schema_path = schema_path
        self.custom_properties_dir = custom_properties_dir
        self.schema = load_schema(schema_path)
        self.schema["$id"] = pathlib.Path(self.schema_path).absolute().as_uri()
        self.registry = referencing.Registry(retrieve=retrieve_from_filesystem)  # type: ignore
        
    def validate_data(self, data):
        """
        Validates a python dictionary against the schema.
        Raises jsonschema.exceptions.ValidationError if invalid.
        Returns the preprocessed data.
        """
        from dmesh.sdk.lean_validator.preprocessor import preprocess
        processed_data = preprocess(data, schema_dir=self.custom_properties_dir)
        validate(instance=processed_data, schema=self.schema, registry=self.registry)
        return processed_data

def main():
    parser = argparse.ArgumentParser(description="Validate JSON/YAML data against a JSON Schema.")
    parser.add_argument("data_file", help="Path to the JSON or YAML data file to validate.")
    parser.add_argument("--schema", default="examples/lean-validator/schemas/custom-odps-json-schema-v1.0.0.json", help="Path to the JSON schema file (default: examples/lean-validator/schemas/custom-odps-json-schema-v1.0.0.json).")
    parser.add_argument("--custom-properties-dir", default="examples/lean-validator/schemas/custom-properties", help="Path to the directory containing custom properties schemas.")

    args = parser.parse_args()

    try:
        data = load_data(args.data_file)
        validator = Validator(schema_path=args.schema, custom_properties_dir=args.custom_properties_dir)
    except Exception as e:
        print(f"Error loading files: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        processed_data = validator.validate_data(data)
        print(f"✅ Validation successful! '{args.data_file}' is valid against '{args.schema}'.")
    except ValidationError as e:
        path_list = list(e.absolute_path)
        is_custom_property = False
        
        if "customProperties" in path_list:
            idx = path_list.index("customProperties")
            if len(path_list) > idx + 1 and isinstance(path_list[idx + 1], int):
                curr = data
                try:
                    for p in path_list[:idx + 2]:
                        curr = curr[p]
                    property_name = curr.get("property", "unknown")
                    
                    # Replace the numeric index with the property name for better readability
                    path_list[idx + 1] = property_name
                    json_path = " -> ".join(str(p) for p in path_list)
                    
                    if e.validator == "enum":
                        field_name = path_list[-1]
                        invalid_val = e.instance
                        if isinstance(e.validator_value, (list, tuple)):
                            supported_vals = ", ".join(str(v) for v in e.validator_value)
                        else:
                            supported_vals = str(e.validator_value)
                        msg = f"ERROR: Specification {args.data_file} customProperty {property_name} {field_name} has an invalid value ({invalid_val}) supported values are ({supported_vals}). Please correct: {json_path}"
                        print(msg, file=sys.stderr)
                        is_custom_property = True
                    else:
                        msg = f"ERROR: Specification {args.data_file} customProperty {property_name} error: {e.message}. Please correct: {json_path}"
                        print(msg, file=sys.stderr)
                        is_custom_property = True
                except Exception:
                    pass
                    
        if not is_custom_property:
            print(f"❌ Validation failed!", file=sys.stderr)
            print(f"Message: {e.message}", file=sys.stderr)
            print(f"Path: {' -> '.join(str(p) for p in e.absolute_path)}", file=sys.stderr)
            
        sys.exit(1)
    except jsonschema.exceptions.SchemaError as e:
        print(f"❌ Schema error! The provided schema is invalid.", file=sys.stderr)
        print(f"Message: {e.message}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
