#!/usr/bin/env python3
"""
Scan all biomni Python scripts and add required dependencies based on imports.
"""

import os
import re
from pathlib import Path

# Mapping of import statements to pip packages
IMPORT_TO_PACKAGE = {
    'Bio': 'biopython',
    'PyPDF2': 'PyPDF2',
    'scipy': 'scipy',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'sklearn': 'scikit-learn',
    'torch': 'torch',
    'tensorflow': 'tensorflow',
    'keras': 'keras',
    'networkx': 'networkx',
    'requests': 'requests',
    'beautifulsoup4': 'beautifulsoup4',
    'lxml': 'lxml',
    'openpyxl': 'openpyxl',
    'xlrd': 'xlrd',
    'yaml': 'pyyaml',
    'toml': 'toml',
    'h5py': 'h5py',
    'nibabel': 'nibabel',
    'SimpleITK': 'SimpleITK',
    'skimage': 'scikit-image',
    'plotly': 'plotly',
    'streamlit': 'streamlit',
}

def extract_imports(py_file):
    """Extract all import statements from a Python file"""
    with open(py_file, 'r') as f:
        content = f.read()

    imports = set()

    # Match: import xxx
    for match in re.finditer(r'^import\s+(\w+)', content, re.MULTILINE):
        imports.add(match.group(1))

    # Match: from xxx import yyy
    for match in re.finditer(r'^from\s+(\w+)', content, re.MULTILINE):
        imports.add(match.group(1))

    return imports

def get_required_packages(imports):
    """Convert imports to required pip packages"""
    packages = set(['biomni'])  # Always include biomni

    for imp in imports:
        if imp in IMPORT_TO_PACKAGE:
            packages.add(IMPORT_TO_PACKAGE[imp])

    return sorted(packages)

def update_dependencies(py_file, required_packages):
    """Update the install_dependencies function with required packages"""
    with open(py_file, 'r') as f:
        content = f.read()

    # Find the deps list
    pattern = r"(deps = \[)([^\]]*)(\])"
    match = re.search(pattern, content)

    if not match:
        print(f"  ⚠️  No deps list found in {py_file}")
        return False

    # Get current deps
    deps_str = match.group(2)
    current_deps = set()
    if deps_str.strip():
        current_deps = {d.strip().strip("'\"") for d in deps_str.split(',') if d.strip()}

    # Check if we need to add anything
    new_deps = set(required_packages) - current_deps

    if not new_deps:
        return False  # No changes needed

    # Merge and sort
    all_deps = sorted(current_deps | set(required_packages))
    new_deps_str = ', '.join(f"'{d}'" for d in all_deps)

    # Replace
    new_content = content.replace(
        match.group(0),
        f"{match.group(1)}{new_deps_str}{match.group(3)}"
    )

    with open(py_file, 'w') as f:
        f.write(new_content)

    return True

def process_python_file(py_file):
    """Process a single Python file"""
    # Extract imports
    imports = extract_imports(py_file)

    # Skip if it's importing from biomni (means it's not a wrapper script)
    if 'biomni' not in imports and 'subprocess' not in imports:
        return None

    # Get required packages
    required_packages = get_required_packages(imports)

    # Update dependencies
    if update_dependencies(py_file, required_packages):
        return required_packages

    return None

def main():
    print("Scanning all biomni Python scripts for dependencies...")
    print("="*80)

    modified_count = 0
    total_count = 0

    for py_file in sorted(Path('biomni').rglob('*.py')):
        # Skip __init__.py and test files
        if py_file.name in ['__init__.py'] or 'test' in str(py_file):
            continue

        total_count += 1
        print(f"\nProcessing: {py_file}")

        result = process_python_file(py_file)

        if result:
            print(f"  ✅ Updated dependencies: {', '.join(result)}")
            modified_count += 1
        else:
            print(f"  ⏭️  No changes needed")

    print("\n" + "="*80)
    print(f"Processed {total_count} Python files")
    print(f"Modified {modified_count} files")
    print("="*80)

if __name__ == '__main__':
    main()
