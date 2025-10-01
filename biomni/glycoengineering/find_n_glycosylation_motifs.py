#!/usr/bin/env python3
"""
Camber wrapper for find_n_glycosylation_motifs from biomni.tool.glycoengineering
Scan a protein sequence for N-linked glycosylation sequons (N-X-[S/T]).
"""

import sys
import json


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

    # Import after dependencies are installed
    from biomni.tool.glycoengineering import find_n_glycosylation_motifs

    # Read input from stdin
    input_data = json.load(sys.stdin)

    sequence = input_data.get("sequence")
    allow_overlap = input_data.get("allow_overlap", False)

    # Validate required parameters
    if not sequence:
        print(json.dumps({
            "error": "Missing required parameter: sequence"
        }))
        sys.exit(1)

    try:
        # Call the tool function
        result = find_n_glycosylation_motifs(
            sequence=sequence,
            allow_overlap=allow_overlap
        )

        # Output result as JSON
        output = {
            "result": result
        }
        print(json.dumps(output, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
