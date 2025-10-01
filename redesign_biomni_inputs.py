#!/usr/bin/env python3
"""
Redesign Biomni apps to use individual input parameters instead of JSON files.
This makes them more user-friendly by exposing each parameter as a separate input.
"""

import json
import os
import re
from pathlib import Path

def extract_parameters_from_content(content):
    """Extract parameter information from HTML content"""
    params = []

    # Find the Input Parameters section
    if '<h3>Input Parameters</h3>' not in content:
        return params

    params_section = content.split('<h3>Input Parameters</h3>')[1].split('<h3>')[0]

    # Parse each parameter from <li> tags
    param_items = re.findall(r'<li><strong>(\w+)</strong>[^<]*\(([^)]+)\)[^:]*:([^<]+)', params_section)

    for param_name, param_type, param_desc in param_items:
        # Parse type information
        type_info = param_type.lower()
        is_required = 'required' in type_info
        is_optional = 'optional' in type_info

        # Determine Camber input type
        camber_type = "Input"  # default
        if 'array' in type_info or 'list' in type_info:
            camber_type = "TextArea"  # Use textarea for arrays (comma-separated)
        elif 'integer' in type_info or 'int' in type_info:
            camber_type = "Number"
        elif 'float' in type_info or 'number' in type_info:
            camber_type = "Number"
        elif 'boolean' in type_info or 'bool' in type_info:
            camber_type = "Checkbox"
        elif 'file' in param_name.lower() or 'path' in param_name.lower():
            camber_type = "Stash File"

        params.append({
            'name': param_name,
            'type': camber_type,
            'description': param_desc.strip(),
            'required': is_required,
            'optional': is_optional
        })

    return params

def should_use_individual_params(params):
    """Decide if app should use individual parameters or keep JSON input"""
    # Use individual params if:
    # - Less than 10 parameters
    # - No complex nested objects
    # - Mostly simple types (string, number, boolean)

    if len(params) == 0 or len(params) > 10:
        return False

    # Check for complex types
    for param in params:
        if param['type'] == 'TextArea' and 'array' not in param['description'].lower():
            # Complex object, keep JSON
            return False

    return True

def generate_spec_from_params(params):
    """Generate Camber spec array from parameters"""
    spec = []

    for param in params:
        spec_item = {
            "type": param['type'],
            "name": param['name'],
            "label": param['name'].replace('_', ' ').title(),
            "description": param['description']
        }

        # Add default values based on type
        if param['type'] == "Checkbox":
            spec_item["defaultValue"] = False
        elif param['type'] == "Number":
            spec_item["defaultValue"] = 0
        else:
            spec_item["defaultValue"] = ""

        spec.append(spec_item)

    # Always add output directory
    spec.append({
        "type": "Stash File",
        "name": "outputDir",
        "label": "Output Directory",
        "description": "Output directory in stash",
        "defaultValue": "./"
    })

    return spec

def generate_command_from_params(params, category, script_name):
    """Generate command string with individual parameters"""
    param_refs = []

    for param in params:
        if param['type'] == "Checkbox":
            # For boolean, add flag if true
            param_refs.append(f"${{[[ \"${{{param['name']}}}\" == \"true\" ]] && echo \"--{param['name']}\" || echo \"\"}}")
        else:
            param_refs.append(f"--{param['name']} \"${{{param['name']}}}\"")

    param_string = " ".join(param_refs)

    command = f"rm -rf prod_apps 2>/dev/null || true && git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git prod_apps && python3 prod_apps/biomni/{category}/{script_name}.py {param_string} -o \"${{outputDir}}\""

    return command

def analyze_all_apps():
    """Analyze all Biomni apps"""
    print("Analyzing all Biomni apps...")
    print("="*80)

    categories = [d for d in os.listdir('biomni') if os.path.isdir(f'biomni/{d}') and not d.startswith('.')]

    stats = {
        'total': 0,
        'can_use_individual_params': 0,
        'keep_json': 0,
        'by_category': {}
    }

    for category in sorted(categories):
        apps = [f.replace('_app.json', '') for f in os.listdir(f'biomni/{category}') if f.endswith('_app.json')]
        stats['by_category'][category] = {'total': len(apps), 'individual': 0, 'json': 0}

        for app_name in apps:
            stats['total'] += 1
            json_path = f'biomni/{category}/{app_name}_app.json'

            with open(json_path) as f:
                data = json.load(f)

            params = extract_parameters_from_content(data.get('content', ''))
            use_individual = should_use_individual_params(params)

            if use_individual:
                stats['can_use_individual_params'] += 1
                stats['by_category'][category]['individual'] += 1
            else:
                stats['keep_json'] += 1
                stats['by_category'][category]['json'] += 1

    print(f"\nTotal apps: {stats['total']}")
    print(f"Can use individual params: {stats['can_use_individual_params']}")
    print(f"Keep JSON input: {stats['keep_json']}")
    print(f"\nBy category:")
    for cat, data in sorted(stats['by_category'].items()):
        print(f"  {cat}: {data['individual']} individual, {data['json']} JSON")

    return stats

if __name__ == '__main__':
    stats = analyze_all_apps()

    print(f"\n{'='*80}")
    print("Analysis complete!")
    print(f"{'='*80}")
