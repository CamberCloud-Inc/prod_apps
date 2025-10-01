#!/usr/bin/env python3
"""
Fix missing dependencies found during testing based on which biomni.tool modules are imported.
"""
import os
import re
from pathlib import Path

# Map of biomni.tool modules to their required dependencies
TOOL_MODULE_DEPS = {
    'biomni.tool.molecular_biology': ['biopython', 'beautifulsoup4'],
    'biomni.tool.genetics': ['biopython', 'torch'],
    'biomni.tool.biophysics': ['opencv-python', 'scipy'],
    'biomni.tool.physiology': ['opencv-python', 'scipy', 'scikit-image'],
    'biomni.tool.cancer_biology': ['gseapy', 'FlowCytometryTools'],
    'biomni.tool.literature': ['PyPDF2'],
    'biomni.tool.database': ['biopython'],
    'biomni.tool.microbiology': ['biopython'],
}

def get_biomni_imports(py_file):
    """Extract biomni.tool imports from a Python file"""
    with open(py_file, 'r') as f:
        content = f.read()

    imports = set()
    # Match: from biomni.tool.xxx import yyy
    for match in re.finditer(r'from\s+(biomni\.tool\.\w+)\s+import', content):
        imports.add(match.group(1))

    return imports

def get_required_deps(py_file):
    """Get required dependencies based on biomni.tool imports"""
    imports = get_biomni_imports(py_file)
    deps = {'biomni'}  # Always need biomni

    for imp in imports:
        if imp in TOOL_MODULE_DEPS:
            deps.update(TOOL_MODULE_DEPS[imp])

    return sorted(deps)

def update_dependencies(py_file, required_deps):
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

    # Merge
    all_deps = sorted(current_deps | set(required_deps))
    new_deps_str = ', '.join(f"'{d}'" for d in all_deps)

    new_content = content.replace(
        match.group(0),
        f"{match.group(1)}{new_deps_str}{match.group(3)}"
    )

    if new_content != content:
        with open(py_file, 'w') as f:
            f.write(new_content)
        return True

    return False

def main():
    print("Fixing missing dependencies based on biomni.tool imports...")
    print("="*80)

    modified = []

    for py_file in sorted(Path('biomni').rglob('*.py')):
        if py_file.name == '__init__.py':
            continue

        # Skip if no install_dependencies function
        with open(py_file, 'r') as f:
            if 'def install_dependencies' not in f.read():
                continue

        required_deps = get_required_deps(py_file)

        if len(required_deps) > 1:  # More than just 'biomni'
            if update_dependencies(py_file, required_deps):
                print(f"✅ {py_file}: {', '.join(required_deps)}")
                modified.append(str(py_file))

    print("\n" + "="*80)
    print(f"Modified {len(modified)} files")
    print("="*80)

    if modified:
        print("\nFiles modified:")
        for f in modified:
            print(f"  - {f}")

if __name__ == '__main__':
    main()
