#!/usr/bin/env python3
"""
Fix all _app.json files to use proper REPO_DIR with random hash
"""
import json
import glob
import re

# Find all app.json files
app_files = glob.glob('python/*_app.json')

print(f"Found {len(app_files)} app files to fix")

for app_file in app_files:
    with open(app_file, 'r') as f:
        data = json.load(f)

    # Check if command field exists and contains git clone
    if 'command' in data and 'git clone' in data['command']:
        old_command = data['command']

        # Pattern 1: Simple rm -rf prod_apps && git clone ...
        pattern1 = r'rm -rf prod_apps && git clone --depth 1 https://github\.com/CamberCloud-Inc/prod_apps\.git'
        replacement1 = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'

        # Pattern 2: rm -rf prod_apps (without &&)
        pattern2 = r'rm -rf prod_apps\s+git clone'
        replacement2 = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone'

        new_command = old_command

        # Try pattern 1 first
        if re.search(pattern1, old_command):
            new_command = re.sub(pattern1, replacement1, old_command)
            print(f"Updating {app_file} with pattern 1")
        # Try pattern 2
        elif re.search(pattern2, old_command):
            new_command = re.sub(pattern2, replacement2, old_command)
            print(f"Updating {app_file} with pattern 2")

        # Now fix all $REPO_DIR/ references to use the variable properly
        # Replace python $REPO_DIR/python with python "$REPO_DIR/python"
        new_command = re.sub(r'\bpython \$REPO_DIR/', 'python "$REPO_DIR/', new_command)

        # If command changed, update it
        if new_command != old_command:
            data['command'] = new_command

            # Write back
            with open(app_file, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"  ✓ Updated: {app_file}")
        else:
            print(f"  - Skipped (no changes): {app_file}")

print("\nAll app files have been processed!")