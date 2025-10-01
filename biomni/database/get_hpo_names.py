"""
Camber wrapper for biomni.tool.database.get_hpo_names
"""

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

def main(hpo_terms, data_lake_path):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import get_hpo_names
    """
    Wrapper for get_hpo_names from biomni.tool.database
    
    Helper function to query LLMs for generating API calls based on natural language prompts.

    Supports multiple model providers including Claude, Gemini, GPT, and others via the unified get_llm interface.

    Parameters
    ----------
    prompt (str): Natural language query to process
    schema (dict): API schema to include in the system prompt
    system_template (str): Template string for the system prompt (should have {schema} placeholder)

    Returns
    -------
    dict: Dictionary wit
    """
    result = get_hpo_names(hpo_terms=hpo_terms, data_lake_path=data_lake_path)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='get_hpo_names')
    parser.add_argument('--hpo_terms', type=str, required=True, help='hpo_terms')
    parser.add_argument('--data_lake_path', type=str, required=True, help='data_lake_path')
    
    args = parser.parse_args()
    main(**vars(args))
