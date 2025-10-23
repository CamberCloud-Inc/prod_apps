#!/bin/bash

# Methylseq wrapper script for Camber platform
# Conditionally adds override config based on CPU count

# Parse command line arguments
INPUT=""
OUTDIR=""
GENOME=""
REVISION=""
OVERRIDE_CONFIG=""
EXTRA_PARAMS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --input)
      INPUT="$2"
      shift 2
      ;;
    --outdir)
      OUTDIR="$2"
      shift 2
      ;;
    --genome)
      GENOME="$2"
      shift 2
      ;;
    -r)
      REVISION="$2"
      shift 2
      ;;
    --override-config)
      OVERRIDE_CONFIG="$2"
      shift 2
      ;;
    -c|-ansi-log|-profile|--profile)
      # Collect these parameters to pass through to nextflow
      EXTRA_PARAMS+=("$1")
      if [[ $1 != "-ansi-log" ]]; then
        EXTRA_PARAMS+=("$2")
        shift 2
      else
        shift 2  # -ansi-log takes a parameter
      fi
      ;;
    *)
      # Collect any other unknown parameters
      EXTRA_PARAMS+=("$1")
      shift
      ;;
  esac
done

# Get CPU count
CPU_COUNT=$(nproc)

# Set Nextflow environment variables (only if not already set)
export NXF_CACHE_DIR=${NXF_CACHE_DIR:-/camber_work/temp/.nextflow}
export NXF_LOG_FILE=${NXF_LOG_FILE:-${OUTDIR}/nextflow.log}

# Build base command
BASE_CMD="nextflow run nf-core/methylseq --input \"${INPUT}\" --outdir \"${OUTDIR}\" --genome ${GENOME} -r ${REVISION}"

# Add override config if CPU >= 60 AND override config is provided and not empty
if [ ${CPU_COUNT} -ge 60 ] && [ -n "${OVERRIDE_CONFIG}" ] && [ "${OVERRIDE_CONFIG}" != '""' ]; then
  echo "CPU count: ${CPU_COUNT} (>= 60) - Using override config: ${OVERRIDE_CONFIG}"
  BASE_CMD="${BASE_CMD} -c \"${OVERRIDE_CONFIG}\""
else
  echo "CPU count: ${CPU_COUNT} (< 60 or no override config) - Running without override config"
fi

# Add any extra parameters passed by the platform
if [ ${#EXTRA_PARAMS[@]} -gt 0 ]; then
  echo "Adding platform parameters: ${EXTRA_PARAMS[@]}"
  BASE_CMD="${BASE_CMD} ${EXTRA_PARAMS[@]}"
fi

# Execute the command
echo "Executing: ${BASE_CMD}"
eval ${BASE_CMD}
