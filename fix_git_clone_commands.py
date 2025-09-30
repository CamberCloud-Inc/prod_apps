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

        # Multiple patterns to match different git clone command variations
        new_command = old_command
        updated = False

        # Pattern 1: rm -rf prod_apps && git clone (with or without --depth 1)
        pattern1 = r'rm -rf prod_apps && git clone(?:\s+--depth\s+1)?\s+https://github\.com/CamberCloud-Inc/prod_apps\.git'
        if re.search(pattern1, old_command):
            if '--depth 1' in old_command:
                replacement = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
            else:
                replacement = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
            new_command = re.sub(pattern1, replacement, old_command)
            print(f"Updating {app_file} with pattern 1")
            updated = True

        # Pattern 2: rm -rf prod_apps 2>/dev/null || true && git clone
        pattern2 = r'rm -rf prod_apps 2>/dev/null \|\| true && git clone(?:\s+--depth\s+1)?\s+https://github\.com/CamberCloud-Inc/prod_apps\.git'
        if not updated and re.search(pattern2, old_command):
            if '--depth 1' in old_command:
                replacement = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
            else:
                replacement = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
            new_command = re.sub(pattern2, replacement, old_command)
            print(f"Updating {app_file} with pattern 2")
            updated = True

        # Pattern 3: rm -rf prod_apps 2>/dev/null || true; [ ! -d prod_apps ] && git clone
        pattern3 = r'rm -rf prod_apps 2>/dev/null \|\| true; \[ ! -d prod_apps \] && git clone(?:\s+--depth\s+1)?\s+https://github\.com/CamberCloud-Inc/prod_apps\.git'
        if not updated and re.search(pattern3, old_command):
            if '--depth 1' in old_command:
                replacement = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone --depth 1 https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
            else:
                replacement = 'REPO_DIR="prod_apps_${RANDOM}_${RANDOM}"; rm -rf "$REPO_DIR" 2>/dev/null || true; git clone https://github.com/CamberCloud-Inc/prod_apps.git "$REPO_DIR"'
            new_command = re.sub(pattern3, replacement, old_command)
            print(f"Updating {app_file} with pattern 3")
            updated = True

        # Now fix all references to use the variable properly
        # Replace python prod_apps/python with python "$REPO_DIR/python"
        new_command = re.sub(r'\bpython prod_apps/', 'python "$REPO_DIR/', new_command)
        # Replace python $REPO_DIR/python (without quotes) with python "$REPO_DIR/python"
        new_command = re.sub(r'\bpython \$REPO_DIR/', 'python "$REPO_DIR/', new_command)
        # Ensure closing quote is added if not already present
        if '"$REPO_DIR/' in new_command and not re.search(r'"\$REPO_DIR/[^"]*"', new_command):
            # Find python "$REPO_DIR/... and add closing quote before next space or &&
            new_command = re.sub(r'python "\$REPO_DIR/([^\s"]+)', r'python "$REPO_DIR/\1"', new_command)

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