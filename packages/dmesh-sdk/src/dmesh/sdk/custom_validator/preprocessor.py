import os
import json

def get_custom_properties(data, results=None):
    if results is None:
        results = []
    
    if isinstance(data, dict):
        for k, v in data.items():
            if k == "customProperties" and isinstance(v, list):
                results.append(v)
            else:
                get_custom_properties(v, results)
    elif isinstance(data, list):
        for item in data:
            get_custom_properties(item, results)
            
    return results

def preprocess(data, schema_dir="examples/custom-validation/schemas/custom-properties"):
    """
    Traverses the data dictionary to find `customProperties` arrays.
    It builds a lookup of all 'Inserts' properties (e.g. `publishToS3Inserts`),
    and then replaces `_insertFrom` references in base properties 
    (e.g. `publishToS3`) with the values from the corresponding Inserts object.
    It also dynamically injects default values from the JSON schemas into
    objects that omit those fields.
    """
    if not isinstance(data, (dict, list)):
        return data

    all_custom_props = get_custom_properties(data)
    
    # 1. Build a lookup of insertId -> values from properties ending with '_inserts'
    inserts_lookup = {}
    for custom_props in all_custom_props:
        for prop in custom_props:
            if isinstance(prop, dict):
                prop_name = prop.get("property", "")
                if prop_name.endswith("_inserts"):
                    # The value should be a list of insert objects
                    inserts = prop.get("value", [])
                    if isinstance(inserts, list):
                        for insert_obj in inserts:
                            if "_insertId" in insert_obj:
                                # the template name we will reference
                                insert_id = insert_obj["_insertId"]
                                
                                # we associate the base property name (e.g. publishToS3)
                                # with this insert object
                                base_prop = prop_name[:-len("_inserts")]
                                
                                if base_prop not in inserts_lookup:
                                    inserts_lookup[base_prop] = {}
                                inserts_lookup[base_prop][insert_id] = insert_obj

    # 2. Process '_insertFrom' properties and expand them
    for custom_props in all_custom_props:
        for prop in custom_props:
            if isinstance(prop, dict):
                prop_name = prop.get("property")
                value = prop.get("value")
                
                # Check if it has an _insertFrom reference
                if prop_name and isinstance(value, dict) and "_insertFrom" in value:
                    insert_id = value["_insertFrom"]
                    if prop_name in inserts_lookup and insert_id in inserts_lookup[prop_name]:
                        template = inserts_lookup[prop_name][insert_id]
                        # Remove _insertFrom
                        del value["_insertFrom"]
                        
                        # Copy all fields from template except _insertId
                        for k, v in template.items():
                            if k != "_insertId" and k not in value:
                                value[k] = v
                    else:
                        raise ValueError(f"Could not find template for property '{prop_name}' with _insertId '{insert_id}'")

    # 3. Dynamic Schema Default Injection
    if os.path.exists(schema_dir):
        for custom_props in all_custom_props:
            for prop in custom_props:
                if not isinstance(prop, dict):
                    continue
                prop_name = prop.get("property")
                value = prop.get("value")
                
                if prop_name:
                    schema_path = os.path.join(schema_dir, f"{prop_name}.json")
                    if os.path.exists(schema_path):
                        try:
                            with open(schema_path, "r") as f:
                                schema = json.load(f)
                                
                            # Root-level default for the value itself (e.g. enterpriseDataProduct)
                            if "default" in schema and "value" not in prop:
                                prop["value"] = schema["default"]
                                
                            # Object-level defaults (for fields within a dict value, e.g. publishToS3)
                            value = prop.get("value")
                            if isinstance(value, dict):
                                properties = schema.get("properties", {})
                                for field, subschema in properties.items():
                                    if "default" in subschema and field not in value:
                                        value[field] = subschema["default"]
                        except Exception:
                            pass

    return data
