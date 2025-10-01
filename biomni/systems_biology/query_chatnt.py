#!/usr/bin/env python3
"""
Wrapper for Biomni query_chatnt tool
"""
import sys


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
    from biomni.tool.systems_biology import query_chatnt
    if len(sys.argv) != 4:
        print("Usage: query_chatnt.py <question> <sequence> <device>")
        sys.exit(1)

    question = sys.argv[1]
    sequence = sys.argv[2]
    device = int(sys.argv[3])

    result = query_chatnt(question, sequence, device)
    print(result)

if __name__ == "__main__":
    main()
