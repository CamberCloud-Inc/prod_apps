#!/usr/bin/env python3
"""
Inline all biomni functions into wrapper scripts.
For each biomni wrapper:
1. Extract the function code from biomni source
2. Analyze dependencies needed by that specific function
3. Embed function code directly in wrapper
4. Update install_dependencies to install only what's needed
5. Remove biomni package dependency
"""

import os
import re
import ast
from pathlib import Path

# Map of wrapper files to their biomni function imports
BIOMNI_SOURCE = "/tmp/biomni_source/biomni/tool"

def extract_function_from_source(category, function_name):
    """Extract a specific function from biomni source code"""
    source_file = os.path.join(BIOMNI_SOURCE, f"{category}.py")

    if not os.path.exists(source_file):
        print(f"  ⚠️  Source file not found: {source_file}")
        return None, set()

    with open(source_file, 'r') as f:
        content = f.read()

    # Parse the AST to find the function
    try:
        tree = ast.parse(content)
    except:
        print(f"  ⚠️  Failed to parse {source_file}")
        return None, set()

    # Find the function definition
    function_code = None
    imports_needed = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Get the source code for this function
            function_start = node.lineno - 1
            function_end = node.end_lineno
            lines = content.split('\n')
            function_code = '\n'.join(lines[function_start:function_end])
            break

    if not function_code:
        print(f"  ⚠️  Function {function_name} not found in {source_file}")
        return None, set()

    # Extract imports from the source file that this function uses
    # Parse all imports at top of file
    all_imports = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                all_imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names = ', '.join([alias.name for alias in node.names])
                all_imports.append(f"from {node.module} import {names}")

    # Analyze function to see which imports it uses
    function_tree = ast.parse(function_code)
    names_used = set()
    for node in ast.walk(function_tree):
        if isinstance(node, ast.Name):
            names_used.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                names_used.add(node.value.id)

    # Filter imports to only those used
    for imp in all_imports:
        imp_names = re.findall(r'import\s+([\w.]+)', imp)
        imp_names += re.findall(r'from\s+[\w.]+\s+import\s+([\w,\s]+)', imp)
        for name_group in imp_names:
            for name in name_group.replace(',', ' ').split():
                name = name.strip()
                if name in names_used:
                    imports_needed.add(imp)
                    break

    return function_code, imports_needed

def analyze_dependencies(function_code, imports):
    """Determine which pip packages are needed"""
    deps = set()

    # Common package mappings
    pkg_mapping = {
        'Bio': 'biopython',
        'scipy': 'scipy',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'sklearn': 'scikit-learn',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'requests': 'requests',
        'lxml': 'lxml',
        'Pillow': 'Pillow',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'torch': 'torch',
        'tensorflow': 'tensorflow',
        'transformers': 'transformers',
        'rdkit': 'rdkit-pypi',
        'networkx': 'networkx',
        'statsmodels': 'statsmodels',
        'xmltodict': 'xmltodict',
        'beautifulsoup4': 'beautifulsoup4',
        'bs4': 'beautifulsoup4',
    }

    for imp in imports:
        for lib_name, pkg_name in pkg_mapping.items():
            if lib_name in imp:
                deps.add(pkg_name)

    return list(deps)

def process_wrapper(wrapper_path):
    """Process a single wrapper file"""
    print(f"\nProcessing: {wrapper_path}")

    with open(wrapper_path, 'r') as f:
        content = f.read()

    # Extract the import statement to find category and function
    import_match = re.search(r'from biomni\.tool\.(\w+) import (\w+)', content)
    if not import_match:
        print(f"  ⏭️  No biomni import found")
        return False

    category = import_match.group(1)
    function_name = import_match.group(2)

    print(f"  Category: {category}, Function: {function_name}")

    # Extract function code from biomni source
    function_code, imports_needed = extract_function_from_source(category, function_name)

    if not function_code:
        return False

    # Analyze dependencies
    deps = analyze_dependencies(function_code, imports_needed)
    print(f"  Dependencies: {deps if deps else 'None'}")

    # Build new wrapper content
    new_content = '#!/usr/bin/env python3\n'
    new_content += f'"""{os.path.basename(wrapper_path)} - Inlined biomni function"""\n\n'

    # Add standard imports
    new_content += 'import sys\n'
    new_content += 'import os\n'
    new_content += 'import argparse\n'
    if 'json' in content.lower():
        new_content += 'import json\n'
    new_content += '\n'

    # Add dependency installation function
    if deps:
        new_content += '# Install dependencies\n'
        new_content += 'def install_dependencies():\n'
        new_content += '    """Install required dependencies"""\n'
        new_content += '    import subprocess\n'
        new_content += f'    deps = {deps}\n'
        new_content += '    print("Installing dependencies...")\n'
        new_content += '    for dep in deps:\n'
        new_content += '        subprocess.check_call([sys.executable, \'-m\', \'pip\', \'install\', \'-q\', dep],\n'
        new_content += '                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n\n'

    # Add the inlined function with its imports
    new_content += '# Inlined biomni function\n'
    for imp in sorted(imports_needed):
        new_content += imp + '\n'
    new_content += '\n'
    new_content += function_code + '\n\n'

    # Add main function - extract from original
    main_match = re.search(r'def main\(\):.*?(?=\nif __name__|$)', content, re.DOTALL)
    if main_match:
        main_code = main_match.group(0)
        # Remove install_dependencies call and biomni import
        main_code = re.sub(r'\s*install_dependencies\(\)\s*', '', main_code)
        main_code = re.sub(r'\s*from biomni\.tool\.\w+ import \w+\s*', '', main_code)

        # Add install_dependencies at start of main if we have deps
        if deps:
            main_code = main_code.replace('def main():', 'def main():\n    install_dependencies()')

        new_content += main_code

    # Add __main__ section
    new_content += '\n\nif __name__ == "__main__":\n'
    new_content += '    main()\n'

    # Write new content
    with open(wrapper_path, 'w') as f:
        f.write(new_content)

    print(f"  ✅ Inlined successfully")
    return True

def main():
    """Process all biomni wrappers"""
    print("Inlining biomni functions into all wrappers...")
    print("="*80)

    if not os.path.exists(BIOMNI_SOURCE):
        print(f"ERROR: Biomni source not found at {BIOMNI_SOURCE}")
        print("Please run: git clone https://github.com/snap-stanford/Biomni.git /tmp/biomni_source")
        return

    modified_count = 0
    total_count = 0

    # Process all Python wrapper files
    for py_file in sorted(Path('biomni').rglob('*.py')):
        if py_file.name.endswith('_app.py') or py_file.name == '__init__.py':
            continue

        total_count += 1
        if process_wrapper(py_file):
            modified_count += 1

    print("\n" + "="*80)
    print(f"Processed {total_count} wrappers")
    print(f"Modified {modified_count} wrappers")
    print("="*80)

if __name__ == '__main__':
    main()
