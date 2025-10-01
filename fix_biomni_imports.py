#!/usr/bin/env python3
"""
Fix all Biomni wrappers to import biomni AFTER installing dependencies.
Currently the biomni imports happen at module level, before install_dependencies() runs.
This causes ModuleNotFoundError in Camber containers.
"""

import os
import re
from pathlib import Path

BIOMNI_DIR = Path("/Users/david/git/prod_apps/biomni")

def fix_wrapper(filepath):
    """Move biomni imports inside main function after install_dependencies() call"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already fixed (no biomni import at top level)
    if 'from biomni.' not in content.split('def install_dependencies')[0]:
        return False

    # Extract the biomni import line(s)
    import_pattern = r'^(from biomni\..*?)$'
    imports = re.findall(import_pattern, content, re.MULTILINE)

    if not imports:
        return False

    # Remove the top-level biomni import
    for imp in imports:
        content = content.replace(imp + '\n', '', 1)

    # Find where to insert the import (after install_dependencies() call in main)
    # Pattern: def main(...): \n    install_dependencies() \n
    main_pattern = r'(def main\([^)]*\):[^\n]*\n\s+install_dependencies\(\)[^\n]*\n)'

    def add_import_after_install(match):
        imports_str = '\n    # Import after dependencies are installed\n    ' + '\n    '.join(imports) + '\n'
        return match.group(1) + imports_str

    new_content = re.sub(main_pattern, add_import_after_install, content, count=1)

    # Only write if something changed
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True

    return False

def main():
    """Fix all Biomni wrapper scripts"""
    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for category_dir in sorted(BIOMNI_DIR.iterdir()):
        if not category_dir.is_dir():
            continue

        print(f"\nProcessing {category_dir.name}/")

        for py_file in sorted(category_dir.glob("*.py")):
            try:
                if fix_wrapper(py_file):
                    print(f"  ✅ Fixed: {py_file.name}")
                    fixed_count += 1
                else:
                    print(f"  ⏭️  Skipped: {py_file.name} (already correct)")
                    skipped_count += 1
            except Exception as e:
                print(f"  ❌ Error: {py_file.name}: {e}")
                error_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Fixed: {fixed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {fixed_count + skipped_count + error_count}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
