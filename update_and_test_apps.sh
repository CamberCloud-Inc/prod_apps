#!/bin/bash
# Update and test all camber apps

set -e

echo "==================================================================="
echo "UPDATING ALL CAMBER APPS"
echo "==================================================================="

# Sample apps to test (a manageable subset)
TEST_APPS=(
    "base64-encoder"
    "csv-to-json"
    "json-formatter"
    "word-counter"
    "line-sorter"
)

# Update apps by deleting and recreating them
echo ""
echo "Step 1: Updating app definitions..."
echo ""

for app in python/*_app.json; do
    app_name=$(basename "$app" _app.json | tr '_' '-')
    echo "Updating: $app_name"

    # Try to delete (ignore if doesn't exist)
    camber app delete "$app_name" 2>/dev/null || true

    # Create with new definition
    camber app create --file "$app" || echo "  Warning: Failed to create $app_name"

    sleep 1
done

echo ""
echo "Step 2: Testing sample apps..."
echo ""

# Test a few apps to verify they work
for app in "${TEST_APPS[@]}"; do
    echo "-------------------------------------------------------------------"
    echo "Testing: $app"
    echo "-------------------------------------------------------------------"

    case "$app" in
        "base64-encoder")
            camber app run "$app" --input inputFile=sample.txt --input outputDir=./
            ;;
        "csv-to-json")
            camber app run "$app" --input inputFile=sample.csv --input outputDir=./
            ;;
        "json-formatter")
            camber app run "$app" --input inputFile=test.json --input outputDir=./
            ;;
        "word-counter")
            camber app run "$app" --input inputFile=sample_text.txt --input outputDir=./
            ;;
        "line-sorter")
            camber app run "$app" --input inputFile=sample_text.txt --input outputDir=./
            ;;
    esac

    sleep 2
done

echo ""
echo "==================================================================="
echo "UPDATE COMPLETE"
echo "==================================================================="
echo ""
echo "Check job status with: camber job get <JOB_ID>"
echo "Check logs with: camber job logs <JOB_ID>"