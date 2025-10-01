#!/usr/bin/env python3
"""
Biomni Tool: Query Clinicaltrials
Wraps: biomni.tool.database.query_clinicaltrials
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Query Clinicaltrials'
    )
    parser.add_argument('--prompt', help='Query prompt/description')
    parser.add_argument('--endpoint', help='API endpoint path')
    parser.add_argument('--term', help='Search term')
    parser.add_argument('--status', help='Trial status filter')
    parser.add_argument('--condition', help='Condition/disease filter')
    parser.add_argument('--intervention', help='Intervention filter')
    parser.add_argument('--location', help='Location filter')
    parser.add_argument('--phase', help='Trial phase filter')
    parser.add_argument('--page_size', default='10', help='Results per page (default: 10)')
    parser.add_argument('--max_pages', default='1', help='Maximum pages to retrieve (default: 1)')
    parser.add_argument('--page_token', help='Page token for pagination')
    parser.add_argument('--verbose', default='true', help='Enable verbose output (true/false, default: true)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import query_clinicaltrials

    result = query_clinicaltrials(
        prompt=args.prompt,
        endpoint=args.endpoint,
        term=args.term,
        status=args.status,
        condition=args.condition,
        intervention=args.intervention,
        location=args.location,
        phase=args.phase,
        page_size=int(args.page_size) if args.page_size else None,
        max_pages=int(args.max_pages) if args.max_pages else None,
        page_token=args.page_token,
        verbose=args.verbose.lower() == 'true' if args.verbose else None
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'clinicaltrials_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
