#!/usr/bin/env python3
"""
Intelligently add dependencies to biomni apps by checking what the biomni modules actually import.
"""

import os
import re
from pathlib import Path
import subprocess
import sys

# Map of import to package
IMPORT_TO_PACKAGE = {
    'Bio': 'biopython',
    'PyPDF2': 'PyPDF2',
    'pypdf': 'pypdf',
    'scipy': 'scipy',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'sklearn': 'scikit-learn',
    'skimage': 'scikit-image',
    'torch': 'torch',
    'tensorflow': 'tensorflow',
    'networkx': 'networkx',
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'lxml': 'lxml',
    'openpyxl': 'openpyxl',
    'xlrd': 'xlrd',
    'yaml': 'pyyaml',
    'nibabel': 'nibabel',
    'SimpleITK': 'SimpleITK',
    'sitk': 'SimpleITK',
    'plotly': 'plotly',
    'h5py': 'h5py',
}

def get_biomni_module_imports(biomni_import_path):
    """
    Figure out what a biomni module imports by checking the actual source.
    E.g., 'biomni.tool.literature' -> check what literature.py imports
    """
    # Try to find the biomni package source
    # First check if it's installed
    try:
        result = subprocess.run(
            [sys.executable, '-c', 'import biomni; print(biomni.__file__)'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            biomni_path = Path(result.stdout.strip()).parent

            # Parse the import path: biomni.tool.literature -> tool/literature.py
            parts = biomni_import_path.split('.')
            if len(parts) > 1:
                # Skip 'biomni' prefix
                rel_path = '/'.join(parts[1:]) + '.py'
                module_file = biomni_path / rel_path

                if module_file.exists():
                    with open(module_file, 'r') as f:
                        content = f.read()

                    imports = set()
                    # Find all import statements
                    for match in re.finditer(r'^(?:from|import)\s+(\w+)', content, re.MULTILINE):
                        imports.add(match.group(1))

                    return imports
    except Exception as e:
        pass

    return set()

def extract_biomni_imports(py_file):
    """Extract biomni module imports from a Python file"""
    with open(py_file, 'r') as f:
        content = f.read()

    biomni_imports = []

    # Match: from biomni.tool.xxx import yyy
    for match in re.finditer(r'from\s+(biomni\.\w+(?:\.\w+)*)\s+import', content):
        biomni_imports.append(match.group(1))

    return biomni_imports

def get_required_packages_for_app(py_file):
    """Determine required packages for an app by checking what biomni modules it uses"""
    required_packages = {'biomni'}  # Always need biomni

    # Get biomni imports
    biomni_imports = extract_biomni_imports(py_file)

    # For each biomni import, check what IT imports
    for biomni_import in biomni_imports:
        module_imports = get_biomni_module_imports(biomni_import)

        # Convert imports to packages
        for imp in module_imports:
            if imp in IMPORT_TO_PACKAGE:
                required_packages.add(IMPORT_TO_PACKAGE[imp])

    return sorted(required_packages)

def update_dependencies(py_file, required_packages):
    """Update the install_dependencies function"""
    with open(py_file, 'r') as f:
        content = f.read()

    # Find deps list
    pattern = r"(deps = \[)([^\]]*)(])"
    match = re.search(pattern, content)

    if not match:
        return False

    # Get current deps
    deps_str = match.group(2)
    current_deps = set()
    if deps_str.strip():
        current_deps = {d.strip().strip("'\"") for d in deps_str.split(',') if d.strip()}

    # Check if we need changes
    new_deps = set(required_packages) - current_deps

    if not new_deps:
        return False

    # Merge and update
    all_deps = sorted(current_deps | set(required_packages))
    new_deps_str = ', '.join(f"'{d}'" for d in all_deps)

    new_content = content.replace(
        match.group(0),
        f"{match.group(1)}{new_deps_str}{match.group(3)}"
    )

    with open(py_file, 'w') as f:
        f.write(new_content)

    return True

def main():
    print("Intelligently analyzing biomni app dependencies...")
    print("="*80)

    # First, check if biomni is installed
    result = subprocess.run(
        [sys.executable, '-c', 'import biomni'],
        capture_output=True
    )

    if result.returncode != 0:
        print("⚠️  biomni package not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'biomni'])

    modified_count = 0
    total_count = 0

    for py_file in sorted(Path('biomni').rglob('*.py')):
        if py_file.name == '__init__.py' or 'test' in str(py_file):
            continue

        # Skip if no install_dependencies function
        with open(py_file, 'r') as f:
            if 'def install_dependencies' not in f.read():
                continue

        total_count += 1
        print(f"\nProcessing: {py_file}")

        # Get required packages
        required_packages = get_required_packages_for_app(py_file)

        print(f"  Required: {', '.join(required_packages)}")

        # Update
        if update_dependencies(py_file, required_packages):
            print(f"  ✅ Updated")
            modified_count += 1
        else:
            print(f"  ⏭️  Already correct")

    print("\n" + "="*80)
    print(f"Processed {total_count} files")
    print(f"Modified {modified_count} files")
    print("="*80)

if __name__ == '__main__':
    main()
