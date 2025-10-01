#!/usr/bin/env python3
"""
Wrapper for Biomni perform_flux_balance_analysis tool
"""
import sys
import json
from biomni.tool.systems_biology import perform_flux_balance_analysis


def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    
    install_dependencies()
    if len(sys.argv) < 2:
        print("Usage: perform_flux_balance_analysis.py <model_file> [constraints_json] [objective_reaction] [output_file]")
        sys.exit(1)

    model_file = sys.argv[1]
    constraints = json.loads(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None
    objective_reaction = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
    output_file = sys.argv[4] if len(sys.argv) > 4 else "fba_results.csv"

    result = perform_flux_balance_analysis(model_file, constraints, objective_reaction, output_file)
    print(result)

if __name__ == "__main__":
    main()
