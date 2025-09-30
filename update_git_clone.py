#!/usr/bin/env python3
"""
Update all _app.json files to use a random hash suffix when cloning prod_apps
"""
import json
import glob
import re

# Find all app.json files
app_files = glob.glob('python/*_app.json')

print(f"Found {len(app_files)} app files to update")

for app_file in app_files:
    with open(app_file, 'r') as f:
        data = json.load(f)

    # Check if command field exists and contains git clone
    if 'command' in data and 'git clone' in data['command']:
        old_command = data['command']

        # Replace the pattern to add random hash
        # Old: rm -rf prod_apps 2>/dev/null || true; [ ! -d prod_apps ] && git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git
        # New: REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; [ ! -d "$REPO_DIR" ] && git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"

        # Update the command to use random hash
        new_command = old_command.replace(
            'rm -rf prod_apps 2>/dev/null || true; [ ! -d prod_apps ] && git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git',
            'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; [ ! -d "$REPO_DIR" ] && git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
        )

        # Now replace all references to prod_apps/ with $REPO_DIR/
        # Match patterns like: prod_apps/python/script.py
        new_command = re.sub(r'\bprod_apps/', '$REPO_DIR/', new_command)

        data['command'] = new_command

        # Write back
        with open(app_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Updated: {app_file}")

print("\nAll app files have been updated!")