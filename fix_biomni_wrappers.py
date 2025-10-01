#!/usr/bin/env python3
"""
Fix all Biomni wrapper scripts to include inline dependency installation.
This ensures all dependencies are installed at runtime, following the utility apps pattern.
"""

import os
import re
from pathlib import Path

BIOMNI_DIR = Path("/Users/david/git/prod_apps/biomni")

# Template for the install_dependencies function
INSTALL_DEPS_TEMPLATE = '''
def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
'''

def fix_wrapper(filepath):
    """Add install_dependencies to a wrapper script"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already has install_dependencies
    if 'def install_dependencies' in content:
        return False

    # Find the import section
    lines = content.split('\n')

    # Find where to insert (after imports, before first function)
    insert_pos = 0
    in_docstring = False
    docstring_char = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track docstrings
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if not in_docstring:
                in_docstring = True
                docstring_char = stripped[:3]
            elif stripped.endswith(docstring_char):
                in_docstring = False
            continue

        if in_docstring:
            continue

        # Found a function definition
        if stripped.startswith('def ') and 'main' in stripped:
            insert_pos = i
            break

        # Track imports
        if stripped.startswith(('import ', 'from ')):
            insert_pos = i + 1

    # Insert install_dependencies function and call it in main
    new_lines = lines[:insert_pos] + [''] + INSTALL_DEPS_TEMPLATE.strip().split('\n') + [''] + lines[insert_pos:]

    # Now add install_dependencies() call at the start of main()
    new_content = '\n'.join(new_lines)

    # Find main function and add install call
    main_pattern = r'(def main\([^)]*\):.*?(?:""".*?"""|\'\'\'.*?\'\'\')?\s*)'

    def add_install_call(match):
        return match.group(1) + '\n    install_dependencies()\n    '

    new_content = re.sub(main_pattern, add_install_call, new_content, flags=re.DOTALL, count=1)

    # Write back
    with open(filepath, 'w') as f:
        f.write(new_content)

    return True

def main():
    """Fix all Biomni wrapper scripts"""
    fixed_count = 0
    skipped_count = 0

    for category_dir in BIOMNI_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        print(f"\nProcessing {category_dir.name}/")

        for py_file in category_dir.glob("*.py"):
            try:
                if fix_wrapper(py_file):
                    print(f"  ✅ Fixed: {py_file.name}")
                    fixed_count += 1
                else:
                    print(f"  ⏭️  Skipped: {py_file.name} (already has install_dependencies)")
                    skipped_count += 1
            except Exception as e:
                print(f"  ❌ Error: {py_file.name}: {e}")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Fixed: {fixed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {fixed_count + skipped_count}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
