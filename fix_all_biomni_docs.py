#!/usr/bin/env python3
"""
Fix all Biomni app documentation and spec fields:
1. Remove JSON input format documentation (no longer relevant)
2. Make optional parameters truly optional (remove required field or set to false)
3. Update descriptions to reflect individual parameter inputs
"""

import json
import os
import re
from pathlib import Path

def clean_documentation(content):
    """Remove JSON input format sections from documentation"""
    # Remove "Input Format" section with JSON examples
    content = re.sub(
        r'<h3>Input Format</h3>.*?(?=<h3>|$)',
        '',
        content,
        flags=re.DOTALL
    )

    # Update any remaining references to JSON files
    content = content.replace('JSON file', 'parameter')
    content = content.replace('JSON input', 'input parameters')
    content = content.replace('input file', 'parameters')

    return content

def fix_spec_optional_params(spec, python_file):
    """Make optional parameters truly optional by analyzing Python argparse"""
    if not os.path.exists(python_file):
        return spec

    # Read Python file to find which args are required
    with open(python_file, 'r') as f:
        py_content = f.read()

    # Find all argparse add_argument calls
    required_params = set()
    optional_params = set()

    # Match patterns like: parser.add_argument('--param', required=True...)
    for match in re.finditer(r"add_argument\(['\"]--(\w+)['\"].*?(?:required=(\w+)|default=)", py_content, re.DOTALL):
        param_name = match.group(1)
        is_required = match.group(2) == 'True' if match.group(2) else False

        if is_required:
            required_params.add(param_name)
        else:
            optional_params.add(param_name)

    # Also check for positional arguments (these are required)
    for match in re.finditer(r"add_argument\(['\"](\w+)['\"](?!,\s*help)", py_content):
        param_name = match.group(1)
        if not param_name.startswith('-'):
            required_params.add(param_name)

    # Update spec based on analysis
    for item in spec:
        if item['name'] == 'outputDir':
            continue  # Always required

        param_name = item['name']

        # Check if this parameter is optional in Python
        if param_name in optional_params or (param_name not in required_params and 'default' in item):
            # Make it optional in spec
            if 'required' in item:
                item['required'] = False

    return spec

def process_app(json_path):
    """Process a single app JSON file"""
    with open(json_path, 'r') as f:
        app_data = json.load(f)

    modified = False

    # Clean documentation
    if 'content' in app_data:
        new_content = clean_documentation(app_data['content'])
        if new_content != app_data['content']:
            app_data['content'] = new_content
            modified = True

    # Fix spec optional parameters
    if 'spec' in app_data:
        # Get corresponding Python file
        app_name = os.path.basename(json_path).replace('_app.json', '.py')
        category = os.path.basename(os.path.dirname(json_path))
        python_file = os.path.join('biomni', category, app_name)

        new_spec = fix_spec_optional_params(app_data['spec'], python_file)
        if new_spec != app_data['spec']:
            app_data['spec'] = new_spec
            modified = True

    # Write back if modified
    if modified:
        with open(json_path, 'w') as f:
            json.dump(app_data, f, indent=2)
        return True
    return False

def main():
    """Process all Biomni apps"""
    print("Fixing all Biomni app documentation and specs...")
    print("="*80)

    modified_count = 0
    total_count = 0

    # Process all app JSON files
    for json_file in Path('biomni').rglob('*_app.json'):
        total_count += 1
        if process_app(json_file):
            modified_count += 1
            print(f"✅ Fixed: {json_file}")
        else:
            print(f"⏭️  No changes: {json_file}")

    print("\n" + "="*80)
    print(f"Processed {total_count} apps")
    print(f"Modified {modified_count} apps")
    print("="*80)

if __name__ == '__main__':
    main()
