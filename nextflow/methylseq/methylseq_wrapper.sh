#!/bin/bash

# Methylseq wrapper script for Camber platform
# Conditionally adds override config based on CPU count

# Parse command line arguments
INPUT=""
OUTDIR=""
GENOME=""
REVISION=""
OVERRIDE_CONFIG=""

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
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# Get CPU count
CPU_COUNT=$(nproc)

# Set Nextflow environment variables
export NXF_CACHE_DIR=/camber_work/temp/.nextflow
export NXF_LOG_FILE=${OUTDIR}/nextflow.log

# Build base command
BASE_CMD="nextflow run nf-core/methylseq --input \"${INPUT}\" --outdir \"${OUTDIR}\" --genome ${GENOME} -r ${REVISION} -c /etc/mpi/nextflow.camber.config"

# Add override config if CPU >= 60 AND override config is provided
if [ ${CPU_COUNT} -ge 60 ] && [ -n "${OVERRIDE_CONFIG}" ]; then
  echo "CPU count: ${CPU_COUNT} (>= 60) - Using override config: ${OVERRIDE_CONFIG}"
  FULL_CMD="${BASE_CMD} -c \"${OVERRIDE_CONFIG}\" -ansi-log false -profile k8s"
else
  echo "CPU count: ${CPU_COUNT} (< 60) - Running without override config"
  FULL_CMD="${BASE_CMD} -ansi-log false -profile k8s"
fi

# Execute the command
echo "Executing: ${FULL_CMD}"
eval ${FULL_CMD}
