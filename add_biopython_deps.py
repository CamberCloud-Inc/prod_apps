#!/usr/bin/env python3
"""Add biopython to apps that need it"""
import os
import re

# Apps that use biomni.tool.database need biopython
database_apps = [
    'biomni/database/blast_sequence.py',
]

# Other apps that might need specific dependencies
additional_deps = {
    # Add scipy for apps that need it
    'scipy': [
        'biomni/biochemistry/analyze_circular_dichroism_spectra.py',
        'biomni/biochemistry/analyze_enzyme_kinetics_assay.py',
        'biomni/biochemistry/analyze_itc_binding_thermodynamics.py',
        'biomni/physiology/analyze_hemodynamic_data.py',
    ],
    # Add networkx for network analysis
    'networkx': [
        'biomni/cancer_biology/analyze_ddr_network_in_cancer.py',
        'biomni/systems_biology/model_protein_dimerization_network.py',
    ],
}

def add_dependency_to_file(filepath, new_dep):
    """Add a dependency to the install_dependencies function"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the deps list in install_dependencies
    pattern = r"(deps = \[)([^\]]+)(\])"
    match = re.search(pattern, content)
    
    if not match:
        print(f"  ⚠️  Could not find deps list in {filepath}")
        return False
    
    deps_str = match.group(2)
    current_deps = [d.strip().strip("'\"") for d in deps_str.split(',') if d.strip()]
    
    if new_dep in current_deps:
        return False  # Already has it
    
    # Add the new dependency
    current_deps.append(new_dep)
    new_deps_str = ', '.join(f"'{d}'" for d in current_deps)
    
    new_content = content.replace(
        match.group(0),
        f"{match.group(1)}{new_deps_str}{match.group(3)}"
    )
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    print("Adding biopython dependency to database apps...")
    print("="*80)
    
    modified_count = 0
    
    # Add biopython to database apps
    for py_file in database_apps:
        if os.path.exists(py_file):
            print(f"\nProcessing: {py_file}")
            if add_dependency_to_file(py_file, 'biopython'):
                print(f"  ✅ Added biopython")
                modified_count += 1
            else:
                print(f"  ⏭️  Already has biopython")
    
    # Add other specific dependencies
    for dep, files in additional_deps.items():
        for py_file in files:
            if os.path.exists(py_file):
                print(f"\nProcessing: {py_file}")
                if add_dependency_to_file(py_file, dep):
                    print(f"  ✅ Added {dep}")
                    modified_count += 1
                else:
                    print(f"  ⏭️  Already has {dep}")
    
    print("\n" + "="*80)
    print(f"Modified {modified_count} files")
    print("="*80)

if __name__ == '__main__':
    main()
