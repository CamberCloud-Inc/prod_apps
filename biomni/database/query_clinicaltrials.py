"""
Camber wrapper for biomni.tool.database.query_clinicaltrials
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

def main(prompt=None, endpoint=None, term=None, status=None, condition=None, intervention=None, location=None, phase=None, page_size=10, max_pages=1, page_token=None, verbose=True):
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.database import query_clinicaltrials
    """
    Wrapper for query_clinicaltrials from biomni.tool.database
    
    Query ClinicalTrials.gov API for clinical studies.

    Modes:
    - Direct URL: set `endpoint` to a full URL or a path (e.g., "/studies?query.term=breast%20cancer").
    - Structured params: provide `term`, `status`, `condition`, etc.
    - Natural language: provide `prompt` and the function will infer structured params.

    Returns a dict with aggregated results across pages (up to `max_pages`).
    """
    result = query_clinicaltrials(prompt=prompt, endpoint=endpoint, term=term, status=status, condition=condition, intervention=intervention, location=location, phase=phase, page_size=page_size, max_pages=max_pages, page_token=page_token, verbose=verbose)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='query_clinicaltrials')
    parser.add_argument('--prompt', type=str, default=None, help='prompt')
    parser.add_argument('--endpoint', type=str, default=None, help='endpoint')
    parser.add_argument('--term', type=str, default=None, help='term')
    parser.add_argument('--status', type=str, default=None, help='status')
    parser.add_argument('--condition', type=str, default=None, help='condition')
    parser.add_argument('--intervention', type=str, default=None, help='intervention')
    parser.add_argument('--location', type=str, default=None, help='location')
    parser.add_argument('--phase', type=str, default=None, help='phase')
    parser.add_argument('--page_size', type=int, default=10, help='page_size')
    parser.add_argument('--max_pages', type=int, default=1, help='max_pages')
    parser.add_argument('--page_token', type=str, default=None, help='page_token')
    parser.add_argument('--verbose', type=bool, default=True, help='verbose')
    
    args = parser.parse_args()
    main(**vars(args))
