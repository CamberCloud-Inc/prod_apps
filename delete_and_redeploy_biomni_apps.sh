#!/bin/bash

# Delete and redeploy all 205 Biomni apps with new individual parameter interface

echo "========================================================================"
echo "Delete and Redeploy All 205 Biomni Apps"
echo "========================================================================"
echo ""

total=0
deleted=0
deployed=0
failed=0

# Get list of all biomni apps currently deployed
echo "Fetching list of existing Biomni apps..."
existing_apps=$(camber app list 2>&1 | grep -A1 "^Name" | grep "biomni-" | sed 's/Name[[:space:]]*: //' || echo "")

# Delete all existing biomni apps
if [ -n "$existing_apps" ]; then
    echo "Deleting existing Biomni apps..."
    for app_name in $existing_apps; do
        echo "  Deleting: $app_name"
        if camber app delete "$app_name" 2>&1 | grep -q "deleted successfully"; then
            deleted=$((deleted + 1))
            echo "    ✅ Deleted"
        else
            echo "    ⚠️  Delete failed (may not exist)"
        fi
        sleep 0.3
    done
    echo ""
    echo "Deleted $deleted apps"
    echo ""
fi

# Deploy all apps with new interface
echo "Deploying all 205 Biomni apps with new individual parameter interface..."
echo ""

for json_file in biomni/*/*_app.json; do
    total=$((total + 1))
    app_name=$(basename "$json_file" _app.json)
    category=$(basename $(dirname "$json_file"))

    echo "[$total] Deploying: biomni-$app_name (category: $category)"

    if camber app create --file "$json_file" 2>&1 | grep -q "App created successfully"; then
        echo "    ✅ Success"
        deployed=$((deployed + 1))
    else
        echo "    ❌ Failed"
        failed=$((failed + 1))
    fi

    echo ""
    sleep 0.5
done

echo ""
echo "========================================================================"
echo "Deployment Summary"
echo "========================================================================"
echo "Total apps:     $total"
echo "Deleted:        $deleted"
echo "Deployed:       $deployed"
echo "Failed:         $failed"
echo "========================================================================"
