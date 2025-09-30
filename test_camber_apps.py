#!/usr/bin/env python3
"""
Test all utility apps using camber app run
"""
import subprocess
import json
import time
import sys

# Apps to test with appropriate inputs
TEST_APPS = [
    {
        "name": "base64-encoder",
        "inputs": {
            "inputFile": "stash://test_data/sample.txt",
            "outputDir": "./"
        },
        "description": "Encode text file to Base64"
    },
    {
        "name": "csv-to-json",
        "inputs": {
            "inputFile": "stash://test_data/sample.csv",
            "outputDir": "./"
        },
        "description": "Convert CSV to JSON"
    },
    {
        "name": "json-formatter",
        "inputs": {
            "inputFile": "stash://test_data/test.json",
            "outputDir": "./"
        },
        "description": "Format JSON file"
    },
    {
        "name": "word-counter",
        "inputs": {
            "inputFile": "stash://test_data/sample.txt",
            "outputDir": "./"
        },
        "description": "Count words in text file"
    },
    {
        "name": "line-sorter",
        "inputs": {
            "inputFile": "stash://test_data/sample.txt",
            "outputDir": "./"
        },
        "description": "Sort lines in text file"
    },
]

def run_camber_app(app_name, inputs):
    """Run a camber app with given inputs"""
    print(f"\n{'='*80}")
    print(f"Testing: {app_name}")
    print(f"{'='*80}")

    # Build command
    cmd = ["camber", "app", "run", app_name]
    for key, value in inputs.items():
        cmd.extend(["--input", f"{key}={value}"])

    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180  # 3 minute timeout
        )

        if result.returncode == 0:
            print(f"✓ SUCCESS")
            print(f"Output: {result.stdout[:500]}")
            return {"status": "PASSED", "output": result.stdout}
        else:
            print(f"✗ FAILED")
            print(f"Error: {result.stderr[:500]}")
            return {"status": "FAILED", "error": result.stderr}

    except subprocess.TimeoutExpired:
        print(f"⏱ TIMEOUT")
        return {"status": "TIMEOUT", "error": "Command timed out after 3 minutes"}
    except Exception as e:
        print(f"⚠ ERROR: {e}")
        return {"status": "ERROR", "error": str(e)}

def main():
    print("="*80)
    print("CAMBER APP TESTING")
    print("="*80)
    print(f"\nTesting {len(TEST_APPS)} apps via camber app run...")

    results = []
    passed = 0
    failed = 0

    for app_config in TEST_APPS:
        result = run_camber_app(app_config["name"], app_config["inputs"])
        result["app"] = app_config["name"]
        result["description"] = app_config["description"]
        results.append(result)

        if result["status"] == "PASSED":
            passed += 1
        else:
            failed += 1

        # Small delay between tests
        time.sleep(2)

    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total: {len(TEST_APPS)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    # Save results
    with open("python/test_outputs/camber_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "total": len(TEST_APPS),
                "passed": passed,
                "failed": failed
            },
            "results": results
        }, f, indent=2)

    print(f"\nResults saved to: python/test_outputs/camber_test_results.json")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())