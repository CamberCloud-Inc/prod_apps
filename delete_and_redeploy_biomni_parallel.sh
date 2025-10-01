#!/bin/bash

# Delete and redeploy all 205 Biomni apps with PARALLEL operations

echo "========================================================================"
echo "Delete and Redeploy All 205 Biomni Apps (PARALLEL)"
echo "========================================================================"
echo ""

# Get list of all biomni apps currently deployed
echo "Fetching list of existing Biomni apps..."
existing_apps=$(camber app list 2>&1 | grep -A1 "^Name" | grep "biomni-" | sed 's/Name[[:space:]]*: //' || echo "")

# Count apps
total_to_delete=$(echo "$existing_apps" | wc -w | tr -d ' ')
echo "Found $total_to_delete Biomni apps to delete"
echo ""

# Delete all existing biomni apps IN PARALLEL
if [ -n "$existing_apps" ]; then
    echo "Deleting existing Biomni apps in parallel..."
    for app_name in $existing_apps; do
        (
            if camber app delete "$app_name" 2>&1 | grep -q "deleted successfully"; then
                echo "✅ Deleted: $app_name"
            else
                echo "⚠️  Failed: $app_name"
            fi
        ) &
    done

    # Wait for all deletions to complete
    wait
    echo ""
    echo "All deletions complete!"
    echo ""
fi

# Brief pause before redeployment
sleep 2

# Deploy all apps with new interface IN PARALLEL (batches of 20 to avoid overwhelming the API)
echo "Deploying all 205 Biomni apps with new interface..."
echo ""

total=0
deployed=0
failed=0

# Process in batches of 20
batch_size=20
batch_count=0

for json_file in biomni/*/*_app.json; do
    total=$((total + 1))
    app_name=$(basename "$json_file" _app.json)
    category=$(basename $(dirname "$json_file"))

    (
        if camber app create --file "$json_file" 2>&1 | grep -q "App created successfully"; then
            echo "✅ [$total] Deployed: biomni-$app_name ($category)"
        else
            echo "❌ [$total] Failed: biomni-$app_name ($category)"
        fi
    ) &

    batch_count=$((batch_count + 1))

    # Wait after each batch to avoid rate limiting
    if [ $((batch_count % batch_size)) -eq 0 ]; then
        wait
        sleep 1
    fi
done

# Wait for final batch
wait

echo ""
echo "========================================================================"
echo "Deployment Complete"
echo "========================================================================"
echo "Total apps processed: $total"
echo "Check logs above for success/failure status"
echo "========================================================================"
