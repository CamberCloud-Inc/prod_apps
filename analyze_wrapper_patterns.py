#!/usr/bin/env python3
"""
Analyze all Biomni wrappers to determine which ones need I/O pattern fixes.
Check for:
1. Uses argparse (good)
2. Reads from file vs stdin (file is good)
3. Writes to file vs stdout (file is good)
"""

import os
import re
from pathlib import Path

BIOMNI_DIR = Path("/Users/david/git/prod_apps/biomni")

def analyze_wrapper(filepath):
    """Analyze a wrapper's I/O pattern"""
    with open(filepath, 'r') as f:
        content = f.read()

    issues = []

    # Check for argparse
    has_argparse = 'import argparse' in content
    if not has_argparse:
        issues.append("missing_argparse")

    # Check for stdin reading
    uses_stdin = 'sys.stdin' in content or 'json.load(sys.stdin)' in content
    if uses_stdin:
        issues.append("uses_stdin")

    # Check for stdout-only output (no file writing)
    writes_file = 'open(' in content and "'w'" in content
    if not writes_file and not uses_stdin:  # If not using stdin, should write to file
        issues.append("no_file_output")

    # Check if it reads from a file argument
    reads_file_arg = 'args.' in content and 'open(' in content and "'r'" in content

    return {
        'has_argparse': has_argparse,
        'uses_stdin': uses_stdin,
        'writes_file': writes_file,
        'reads_file_arg': reads_file_arg,
        'issues': issues,
        'needs_fix': bool(issues)
    }

def main():
    """Analyze all Biomni wrapper scripts"""
    results = {
        'good': [],
        'needs_fix': [],
        'by_issue': {
            'missing_argparse': [],
            'uses_stdin': [],
            'no_file_output': []
        }
    }

    for category_dir in sorted(BIOMNI_DIR.iterdir()):
        if not category_dir.is_dir():
            continue

        for py_file in sorted(category_dir.glob("*.py")):
            analysis = analyze_wrapper(py_file)
            rel_path = str(py_file.relative_to(BIOMNI_DIR))

            if analysis['needs_fix']:
                results['needs_fix'].append(rel_path)
                for issue in analysis['issues']:
                    results['by_issue'][issue].append(rel_path)
            else:
                results['good'].append(rel_path)

    # Print report
    print(f"\n{'='*70}")
    print("BIOMNI WRAPPER I/O PATTERN ANALYSIS")
    print(f"{'='*70}\n")

    print(f"✅ Good wrappers (correct pattern): {len(results['good'])}")
    print(f"❌ Need fixing: {len(results['needs_fix'])}\n")

    print("Issues breakdown:")
    for issue, files in results['by_issue'].items():
        print(f"  - {issue}: {len(files)}")

    print(f"\n{'='*70}")
    print("WRAPPERS NEEDING FIXES:")
    print(f"{'='*70}\n")

    for filepath in results['needs_fix'][:20]:  # Show first 20
        print(f"  {filepath}")

    if len(results['needs_fix']) > 20:
        print(f"  ... and {len(results['needs_fix']) - 20} more")

    print(f"\n{'='*70}")
    print(f"Total: {len(results['good']) + len(results['needs_fix'])} wrappers analyzed")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
