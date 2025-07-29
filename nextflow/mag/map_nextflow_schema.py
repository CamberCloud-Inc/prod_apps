import json
import sys

# Helper function to flatten all property dicts from nested definitions
def collect_properties(schema, visited_defs=None):
    if visited_defs is None:
        visited_defs = set()
    properties = {}
    # collect direct properties
    if "properties" in schema:
        properties.update(schema["properties"])
    # recursively collect from allOf
    if "allOf" in schema:
        for item in schema["allOf"]:
            if "$ref" in item:
                ref = item["$ref"]
                # only internal refs supported here
                if ref.startswith("#/$defs/"):
                    defname = ref.split("/")[-1]
                    if defname in visited_defs:
                        continue
                    visited_defs.add(defname)
                    if defname in schema.get("$defs", {}):
                        properties.update(collect_properties(schema["$defs"][defname], visited_defs))
            else:
                properties.update(collect_properties(item, visited_defs))
    return properties

def map_field(name, prop):
    typ = prop.get("type", "string")
    format_ = prop.get("format", "")
    enum = prop.get("enum", None)

    # Decide field type
    if typ == "boolean":
        field_type = "Checkbox"
    elif typ in ("integer", "number"):
        field_type = "Input"
    elif typ == "string" and enum:
        field_type = "Radio" if 2 <= len(enum) <= 3 else "Select"
    elif typ == "string" and format_ in ("file-path", "directory-path"):
        field_type = "Multi Stash File"
    else:
        field_type = "Input"

    # Set defaultValue with correct type
    if field_type == "Multi Stash File":
        default_value = prop.get("default", prop.get("defaultValue", []))
        if not isinstance(default_value, list):
            default_value = []
    elif field_type == "Checkbox":
        default_value = prop.get("default", prop.get("defaultValue", False))
        if not isinstance(default_value, bool):
            default_value = False
    elif field_type == "Input":
        default_value = prop.get("default", prop.get("defaultValue", ""))
        if not isinstance(default_value, str):
            default_value = str(default_value)
    else:
        default_value = prop.get("default", prop.get("defaultValue", ""))

    field = {
        "label": prop.get("title", name),
        "name": name,
        "description": prop.get("description", ""),
        "defaultValue": default_value,
        "hidden": prop.get("hidden", False),
        "required": name in prop.get("required", []) or prop.get("required", False),
        "disabled": False,
        "type": field_type
    }

    if field_type in ("Radio", "Select"):
        field["options"] = [{"label": str(v), "value": v} for v in enum]

    # For pattern (e.g. email), add description
    if "pattern" in prop:
        field["description"] += f" (pattern: {prop['pattern']})"
    return field

def nextflow_schema_to_spec(nextflow_schema_path):
    with open(nextflow_schema_path) as f:
        schema = json.load(f)
    properties = collect_properties(schema)
    spec = []
    for name, prop in properties.items():
        # skip hidden or internal fields
        if prop.get("hidden", False):
            continue
        spec.append(map_field(name, prop))
    return spec

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} nextflow_schema.json", file=sys.stderr)
        sys.exit(1)
    spec = nextflow_schema_to_spec(sys.argv[1])
    print(json.dumps(spec, indent=2))
