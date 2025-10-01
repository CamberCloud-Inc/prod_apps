#!/bin/bash

# Deploy all 205 Biomni apps to Camber platform
# This script creates or updates all apps with the latest documentation

echo "======================================================================"
echo "Deploying All 205 Biomni Apps to Camber"
echo "======================================================================"
echo ""

# Counter
total=0
deployed=0
failed=0

# Find all app JSON files
for json_file in biomni/*/*_app.json; do
    total=$((total + 1))
    app_name=$(basename "$json_file" _app.json)
    category=$(basename $(dirname "$json_file"))

    echo "[$total] Deploying: biomni-$app_name (category: $category)"

    # Deploy the app (creates new or updates existing)
    if camber app create --file "$json_file" 2>&1; then
        echo "    ✅ Success"
        deployed=$((deployed + 1))
    else
        echo "    ❌ Failed"
        failed=$((failed + 1))
    fi

    echo ""

    # Brief pause to avoid rate limiting
    sleep 0.5
done

echo ""
echo "======================================================================"
echo "Deployment Summary"
echo "======================================================================"
echo "Total apps:     $total"
echo "Deployed:       $deployed"
echo "Failed:         $failed"
echo "======================================================================"
