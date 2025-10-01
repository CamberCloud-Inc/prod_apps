#!/usr/bin/env python3
"""
Convert all Biomni app JSONs to proper Camber format.
Uses the utility apps as a template.
"""

import os
import json
from pathlib import Path

BIOMNI_DIR = Path("/Users/david/git/prod_apps/biomni")

# Template for Camber app JSON
def create_camber_app_json(category, tool_name, description):
    """Create a proper Camber app JSON"""

    # Convert tool_name to app name format
    app_name = f"biomni-{tool_name.replace('_', '-')}"
    title = f"Biomni: {tool_name.replace('_', ' ').title()}"

    return {
        "name": app_name,
        "title": title,
        "description": description or f"Biomni tool: {tool_name}",
        "content": f"<h3>Overview</h3><p>{description or f'Biomedical research tool from Biomni: {tool_name}'}</p><h3>Category</h3><p>{category}</p>",
        "command": f"rm -rf prod_apps 2>/dev/null || true && git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git prod_apps && python3 prod_apps/biomni/{category}/{tool_name}.py \"${{inputFile}}\" -o \"${{outputDir}}\"",
        "engineType": "MPI",
        "jobConfig": [
            {
                "type": "Select",
                "label": "System Size",
                "name": "system_size",
                "hidden": True,
                "description": "Select the configuration for the job",
                "options": [
                    {
                        "label": "Extra Extra Small CPU",
                        "value": "xxsmall_cpu",
                        "mapValue": {
                            "nodeSize": "XXSMALL",
                            "numNodes": 1,
                            "withGpu": False
                        }
                    }
                ],
                "defaultValue": "xxsmall_cpu"
            }
        ],
        "spec": [
            {
                "type": "Stash File",
                "name": "inputFile",
                "label": "Input File",
                "description": "Input file from stash (JSON format)",
                "defaultValue": ""
            },
            {
                "type": "Stash File",
                "name": "outputDir",
                "label": "Output Directory",
                "description": "Output directory in stash",
                "defaultValue": "./"
            }
        ]
    }

def fix_app_json(json_path):
    """Fix a single app JSON file"""
    try:
        # Extract info from path
        category = json_path.parent.name
        tool_name = json_path.stem.replace('_app', '')

        # Try to read existing JSON for description
        try:
            with open(json_path, 'r') as f:
                old_json = json.load(f)
                description = old_json.get('description', '')
        except:
            description = ''

        # Create new Camber-format JSON
        new_json = create_camber_app_json(category, tool_name, description)

        # Write back
        with open(json_path, 'w') as f:
            json.dump(new_json, f, indent=2)

        return True
    except Exception as e:
        print(f"  ❌ Error fixing {json_path}: {e}")
        return False

def main():
    """Fix all Biomni app JSON files"""
    fixed_count = 0
    error_count = 0

    for category_dir in sorted(BIOMNI_DIR.iterdir()):
        if not category_dir.is_dir():
            continue

        print(f"\nProcessing {category_dir.name}/")

        for json_file in sorted(category_dir.glob("*_app.json")):
            if fix_app_json(json_file):
                print(f"  ✅ Fixed: {json_file.name}")
                fixed_count += 1
            else:
                error_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Fixed: {fixed_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
