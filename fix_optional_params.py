#!/usr/bin/env python3
"""
Fix optional parameters in all Biomni app specs.
Read the documentation to identify which parameters are marked as "optional",
then remove the "required" field from those parameters in the spec.
"""

import json
import re
from pathlib import Path

def extract_optional_params_from_docs(content):
    """Extract parameter names that are marked as optional in the documentation"""
    optional_params = set()
    required_params = set()

    # Look for patterns like:
    # <li><strong>param_name</strong> (type, optional): description</li>
    # <li><strong>param_name</strong> (type, required): description</li>
    # <li><strong>param_name</strong> (comma-separated numbers, optional): description</li>

    # Match all parameter entries: <li><strong>NAME</strong> (... optional/required ...): ...
    # This pattern captures the parameter name and everything in the first set of parentheses
    param_pattern = r'<li><strong>([^<]+)</strong>\s*\(([^)]+)\):'
    matches = re.findall(param_pattern, content, re.IGNORECASE)

    for param_name, param_info in matches:
        param_name = param_name.strip()
        param_info_lower = param_info.lower()

        # Convert underscores and hyphens for matching
        # e.g., "temperature_data" should match "temperature_data" or "temperature-data"

        if 'optional' in param_info_lower:
            optional_params.add(param_name)
        elif 'required' in param_info_lower:
            required_params.add(param_name)

    return optional_params, required_params

def fix_app_spec(app_data):
    """Fix the spec array to remove 'required' field from optional parameters"""
    if 'content' not in app_data or 'spec' not in app_data:
        return False

    optional_params, required_params = extract_optional_params_from_docs(app_data['content'])

    if not optional_params and not required_params:
        return False

    modified = False
    for spec_item in app_data['spec']:
        param_name = spec_item.get('name')

        # Skip outputDir - always required
        if param_name in ['outputDir', 'output']:
            continue

        # If this parameter is marked as optional in docs
        if param_name in optional_params:
            # Ensure 'required' field is explicitly set to false
            if 'required' not in spec_item or spec_item['required'] != False:
                spec_item['required'] = False
                modified = True

        # If parameter is marked as required in docs, ensure it's marked in spec
        elif param_name in required_params:
            if 'required' not in spec_item or spec_item['required'] != True:
                spec_item['required'] = True
                modified = True

    return modified

def process_app_file(json_path):
    """Process a single app JSON file"""
    with open(json_path, 'r') as f:
        app_data = json.load(f)

    modified = fix_app_spec(app_data)

    if modified:
        with open(json_path, 'w') as f:
            json.dump(app_data, f, indent=2)
        return True

    return False

def main():
    """Process all Biomni app JSON files"""
    print("Fixing optional parameters in all Biomni apps...")
    print("="*80)

    modified_count = 0
    total_count = 0

    # Process all app JSON files
    for json_file in sorted(Path('biomni').rglob('*_app.json')):
        total_count += 1
        print(f"\nProcessing: {json_file}")

        try:
            if process_app_file(json_file):
                modified_count += 1
                print(f"  ✅ Fixed optional parameters")
            else:
                print(f"  ⏭️  No changes needed")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    print("\n" + "="*80)
    print(f"Processed {total_count} apps")
    print(f"Modified {modified_count} apps")
    print("="*80)

if __name__ == '__main__':
    main()
