#!/usr/bin/env python3
"""
Test all deployed Biomni apps one at a time with automatic fix attempts.
Tracks progress in biomni_test_progress.json
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

PROGRESS_FILE = "biomni_test_progress.json"
LOG_FILE = "biomni_test_log.txt"
MAX_RETRIES = 3
JOB_TIMEOUT = 300  # 5 minutes per job

def log(message):
    """Log to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

def load_progress():
    """Load testing progress from file"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {
        "started_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "apps_tested": 0,
        "apps_passed": 0,
        "apps_failed": 0,
        "apps_skipped": 0,
        "results": {}
    }

def save_progress(progress):
    """Save testing progress to file"""
    progress["last_updated"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def get_deployed_apps():
    """Get list of all deployed Biomni apps"""
    log("Fetching list of deployed Biomni apps...")
    result = subprocess.run(
        ["camber", "app", "list"],
        capture_output=True,
        text=True
    )

    apps = []
    for line in result.stdout.split('\n'):
        if 'biomni-' in line:
            # Extract app name
            if 'Name' in line:
                app_name = line.split('Name')[1].strip().strip(':').strip()
                if app_name.startswith('biomni-'):
                    apps.append(app_name)

    log(f"Found {len(apps)} deployed Biomni apps")
    return sorted(set(apps))

def find_app_json(app_name):
    """Find the app JSON file for a given app name"""
    # Convert app name to file path
    # biomni-blast-sequence -> biomni/database/blast_sequence_app.json
    name_parts = app_name.replace('biomni-', '').split('-')

    # Search for the app JSON file
    for json_file in Path('biomni').rglob('*_app.json'):
        json_name = json_file.stem.replace('_app', '')
        if json_name == '_'.join(name_parts):
            return str(json_file)

    return None

def get_test_inputs(app_json_path):
    """Generate test inputs for an app based on its spec"""
    with open(app_json_path, 'r') as f:
        app_data = json.load(f)

    inputs = {}
    spec = app_data.get('spec', [])

    for item in spec:
        param_name = item['name']
        param_type = item['type']
        default_value = item.get('defaultValue', '')

        # Skip outputDir
        if param_name in ['outputDir', 'output']:
            continue

        # Use default values or generate test values
        if default_value:
            inputs[param_name] = default_value
        elif param_type == 'Input':
            inputs[param_name] = 'test_value'
        elif param_type == 'Select':
            options = item.get('options', [])
            if options:
                inputs[param_name] = options[0].get('value', '')
        elif param_type == 'Checkbox':
            inputs[param_name] = 'false'
        elif param_type == 'Stash File':
            inputs[param_name] = '/test/file.txt'

    return inputs

def get_job_logs(job_id):
    """Get logs from a job"""
    result = subprocess.run(
        ["camber", "job", "logs", job_id],
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

def run_app_test(app_name, app_json_path):
    """Run a test job for an app and wait for completion"""
    log(f"Testing app: {app_name}")

    # Get test inputs
    inputs = get_test_inputs(app_json_path)
    log(f"  Test inputs: {json.dumps(inputs, indent=2)}")

    # Create job
    cmd = ["camber", "app", "run", app_name]
    for key, value in inputs.items():
        cmd.extend(["--input", f"{key}={value}"])

    log(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extract job ID from output
    job_id = None
    for line in result.stdout.split('\n'):
        if 'Job ID' in line or 'job' in line.lower():
            parts = line.split()
            for part in parts:
                if part.isdigit():
                    job_id = part
                    break

    if not job_id:
        log(f"  ❌ Failed to create job")
        return {
            "status": "failed",
            "error": "Failed to create job",
            "output": result.stdout + result.stderr
        }

    log(f"  Job ID: {job_id}")

    # Wait for job completion
    start_time = time.time()
    last_status = None

    while time.time() - start_time < JOB_TIMEOUT:
        # Check job status
        status_result = subprocess.run(
            ["camber", "job", "get", job_id],
            capture_output=True,
            text=True
        )

        status_output = status_result.stdout.lower()

        # Log status changes
        if status_output != last_status:
            for line in status_result.stdout.split('\n'):
                if 'status' in line.lower():
                    log(f"  Status: {line.strip()}")
            last_status = status_output

        if 'completed' in status_output or 'succeeded' in status_output:
            log(f"  ✅ Job completed successfully")
            return {"status": "passed", "job_id": job_id}

        if 'failed' in status_output or 'error' in status_output:
            log(f"  ❌ Job failed - fetching logs...")

            # Get job logs for detailed error analysis
            job_logs = get_job_logs(job_id)
            log(f"  Job logs (last 50 lines):")
            log_lines = job_logs.split('\n')
            for line in log_lines[-50:]:
                if line.strip():
                    log(f"    {line}")

            return {
                "status": "failed",
                "job_id": job_id,
                "error": "Job execution failed",
                "output": status_output,
                "logs": job_logs
            }

        # Still running, wait a bit
        time.sleep(10)

    # Timeout
    log(f"  ⏱️  Job timed out after {JOB_TIMEOUT}s")
    job_logs = get_job_logs(job_id)
    return {
        "status": "timeout",
        "job_id": job_id,
        "error": f"Job timed out after {JOB_TIMEOUT}s",
        "logs": job_logs
    }

def analyze_failure(app_name, test_result):
    """Analyze failure and suggest fixes"""
    error = test_result.get('error', '')
    output = test_result.get('output', '')
    logs = test_result.get('logs', '')

    # Combine all error sources
    all_text = f"{error}\n{output}\n{logs}"

    suggestions = []

    # Check for common issues
    if 'ModuleNotFoundError' in all_text or 'No module named' in all_text:
        # Extract missing module
        if "No module named '" in all_text:
            module = all_text.split("No module named '")[1].split("'")[0]
            suggestions.append({
                "type": "missing_dependency",
                "module": module,
                "fix": f"Add '{module}' to install_dependencies()"
            })
        elif "No module named " in all_text:
            # Try alternative format
            parts = all_text.split("No module named ")
            if len(parts) > 1:
                module = parts[1].split()[0].strip("'\"")
                suggestions.append({
                    "type": "missing_dependency",
                    "module": module,
                    "fix": f"Add '{module}' to install_dependencies()"
                })

    if 'ImportError' in all_text:
        # Extract what couldn't be imported
        if 'cannot import name' in all_text:
            suggestions.append({
                "type": "import_error",
                "fix": "Check import compatibility or missing dependencies"
            })

    if 'FileNotFoundError' in all_text:
        suggestions.append({
            "type": "missing_file",
            "fix": "Test inputs may need valid file paths or files may need to be created"
        })

    if 'validation failed' in all_text.lower():
        suggestions.append({
            "type": "validation_error",
            "fix": "Check app spec validation errors"
        })

    if 'required' in all_text.lower() and 'missing' in all_text.lower():
        suggestions.append({
            "type": "missing_required_param",
            "fix": "Add missing required parameters to spec"
        })

    if 'permission denied' in all_text.lower():
        suggestions.append({
            "type": "permission_error",
            "fix": "Check file permissions or executable permissions"
        })

    if 'timeout' in all_text.lower() or 'timed out' in all_text.lower():
        suggestions.append({
            "type": "timeout",
            "fix": "Job may need more time or has an infinite loop"
        })

    return suggestions

def attempt_fix(app_name, app_json_path, suggestions):
    """Attempt to fix issues based on suggestions"""
    if not suggestions:
        return False

    fixed = False

    for suggestion in suggestions:
        if suggestion['type'] == 'missing_dependency':
            module = suggestion['module']
            log(f"  🔧 Attempting fix: Add dependency '{module}'")

            # Find Python file
            py_file = app_json_path.replace('_app.json', '.py')
            if not os.path.exists(py_file):
                continue

            # Add dependency
            with open(py_file, 'r') as f:
                content = f.read()

            # Find deps list
            import re
            pattern = r"(deps = \[)([^\]]+)(\])"
            match = re.search(pattern, content)

            if match:
                deps_str = match.group(2)
                current_deps = [d.strip().strip("'\"") for d in deps_str.split(',') if d.strip()]

                if module not in current_deps:
                    current_deps.append(module)
                    new_deps_str = ', '.join(f"'{d}'" for d in current_deps)
                    new_content = content.replace(
                        match.group(0),
                        f"{match.group(1)}{new_deps_str}{match.group(3)}"
                    )

                    with open(py_file, 'w') as f:
                        f.write(new_content)

                    log(f"  ✅ Added dependency '{module}' to {py_file}")

                    # Redeploy app
                    log(f"  🔄 Redeploying app...")
                    subprocess.run(["camber", "app", "delete", app_name],
                                 capture_output=True)
                    time.sleep(2)
                    result = subprocess.run(
                        ["camber", "app", "create", "--file", app_json_path],
                        capture_output=True,
                        text=True
                    )

                    if 'created successfully' in result.stdout.lower():
                        log(f"  ✅ App redeployed successfully")
                        fixed = True
                    else:
                        log(f"  ❌ Failed to redeploy app")

    return fixed

def test_app_with_retries(app_name, progress):
    """Test an app with up to MAX_RETRIES attempts"""
    app_json_path = find_app_json(app_name)

    if not app_json_path:
        log(f"⚠️  Could not find app JSON for {app_name}")
        return {
            "status": "skipped",
            "reason": "App JSON not found",
            "attempts": 0
        }

    result = {
        "app_name": app_name,
        "app_json_path": app_json_path,
        "attempts": [],
        "final_status": "unknown"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        log(f"\n{'='*80}")
        log(f"Attempt {attempt}/{MAX_RETRIES} for {app_name}")
        log(f"{'='*80}")

        test_result = run_app_test(app_name, app_json_path)
        result["attempts"].append({
            "attempt_number": attempt,
            "result": test_result
        })

        if test_result["status"] == "passed":
            result["final_status"] = "passed"
            log(f"✅ {app_name} PASSED on attempt {attempt}")
            break

        # Analyze failure and attempt fix
        suggestions = analyze_failure(app_name, test_result)

        if suggestions:
            log(f"  📋 Suggestions for fixing:")
            for sug in suggestions:
                log(f"    - {sug['fix']}")

            if attempt < MAX_RETRIES:
                fixed = attempt_fix(app_name, app_json_path, suggestions)
                if not fixed:
                    log(f"  ⚠️  Could not apply automatic fixes")
        else:
            log(f"  ℹ️  No automatic fixes available")

        if attempt == MAX_RETRIES:
            result["final_status"] = "failed"
            log(f"❌ {app_name} FAILED after {MAX_RETRIES} attempts")

    return result

def main():
    """Main testing loop"""
    log("="*80)
    log("Biomni Apps Testing - Starting")
    log("="*80)

    # Load progress
    progress = load_progress()

    # Get deployed apps
    deployed_apps = get_deployed_apps()

    if not deployed_apps:
        log("❌ No deployed apps found")
        return

    log(f"\nTotal apps to test: {len(deployed_apps)}")
    log(f"Progress file: {PROGRESS_FILE}")
    log(f"Log file: {LOG_FILE}")
    log("")

    # Test each app
    for i, app_name in enumerate(deployed_apps, 1):
        log(f"\n{'#'*80}")
        log(f"Testing app {i}/{len(deployed_apps)}: {app_name}")
        log(f"{'#'*80}")

        # Skip if already tested successfully
        if app_name in progress["results"]:
            if progress["results"][app_name].get("final_status") == "passed":
                log(f"⏭️  Already tested successfully, skipping")
                continue

        # Test the app
        result = test_app_with_retries(app_name, progress)

        # Update progress
        progress["results"][app_name] = result
        progress["apps_tested"] += 1

        if result["final_status"] == "passed":
            progress["apps_passed"] += 1
        elif result["final_status"] == "failed":
            progress["apps_failed"] += 1
        else:
            progress["apps_skipped"] += 1

        save_progress(progress)

        # Summary so far
        log(f"\n{'='*80}")
        log(f"Progress: {progress['apps_tested']}/{len(deployed_apps)} tested")
        log(f"  Passed: {progress['apps_passed']}")
        log(f"  Failed: {progress['apps_failed']}")
        log(f"  Skipped: {progress['apps_skipped']}")
        log(f"{'='*80}\n")

    # Final summary
    log("\n" + "="*80)
    log("FINAL SUMMARY")
    log("="*80)
    log(f"Total apps tested: {progress['apps_tested']}")
    log(f"Passed: {progress['apps_passed']} ({progress['apps_passed']/len(deployed_apps)*100:.1f}%)")
    log(f"Failed: {progress['apps_failed']} ({progress['apps_failed']/len(deployed_apps)*100:.1f}%)")
    log(f"Skipped: {progress['apps_skipped']}")
    log("="*80)

    # List failed apps
    if progress['apps_failed'] > 0:
        log("\nFailed apps:")
        for app_name, result in progress["results"].items():
            if result.get("final_status") == "failed":
                log(f"  ❌ {app_name}")

if __name__ == '__main__':
    main()
