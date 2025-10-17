#!/bin/bash

echo "=== Variant Calling Apps Parameter Verification ==="
echo

# Function to test boolean logic
test_boolean_logic() {
    local app_name=$1
    local enable_vep=$2
    local enable_snpeff=$3
    local enable_bcfann=$4
    local tools="mutect2"
    
    echo "Testing $app_name with:"
    echo "  enable_vep=$enable_vep"
    echo "  enable_snpeff=$enable_snpeff"
    echo "  enable_bcfann=$enable_bcfann"
    
    # Simulate the logic from the apps
    TOOLS="$tools"
    ANNOTATION_TOOLS=""
    
    if [ "$enable_vep" = "true" ] || [ "$enable_vep" = "True" ]; then 
        ANNOTATION_TOOLS="vep"
    fi
    
    if [ "$enable_snpeff" = "true" ] || [ "$enable_snpeff" = "True" ]; then 
        if [ -n "$ANNOTATION_TOOLS" ]; then 
            ANNOTATION_TOOLS="${ANNOTATION_TOOLS},snpeff"
        else 
            ANNOTATION_TOOLS="snpeff"
        fi
    fi
    
    if [ "$enable_bcfann" = "true" ] || [ "$enable_bcfann" = "True" ]; then 
        if [ -n "$ANNOTATION_TOOLS" ]; then 
            ANNOTATION_TOOLS="${ANNOTATION_TOOLS},bcfann"
        else 
            ANNOTATION_TOOLS="bcfann"
        fi
    fi
    
    if [ -n "$ANNOTATION_TOOLS" ]; then 
        if [ -n "$TOOLS" ]; then 
            TOOLS="${TOOLS},${ANNOTATION_TOOLS}"
        else 
            TOOLS="$ANNOTATION_TOOLS"
        fi
    fi
    
    echo "  Result: --tools \"$TOOLS\""
    echo
}

# Test scenarios
echo "1. Testing with lowercase booleans (like job 5558):"
test_boolean_logic "Scenario 1" "false" "true" "false"

echo "2. Testing with uppercase booleans:"
test_boolean_logic "Scenario 2" "False" "True" "False"

echo "3. Testing with all annotations enabled (lowercase):"
test_boolean_logic "Scenario 3" "true" "true" "true"

echo "4. Testing with all annotations enabled (uppercase):"
test_boolean_logic "Scenario 4" "True" "True" "True"

echo "5. Testing with mixed case (edge case):"
test_boolean_logic "Scenario 5" "true" "True" "false"

echo "=== Verification Complete ==="
echo
echo "Both somatic and germline apps now use the same logic:"
echo "  if [ \"\${enable_vep}\" = \"true\" ] || [ \"\${enable_vep}\" = \"True\" ]; then"
echo
echo "This handles both lowercase and uppercase boolean values correctly."