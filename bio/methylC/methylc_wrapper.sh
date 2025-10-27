#!/bin/bash
#==============================================================================
# MethylC-analyzer Wrapper Script for Camber Platform
#
# This wrapper script accepts parameters from the Camber app and runs the
# main setup and analysis script with custom configuration.
#
# Usage: bash methylc_wrapper.sh <input_path> <gtf_file> <output_dir> <group_a> <group_b>
#        input_path can be:
#          - Single CGmap.gz file
#          - Single CpG_report.txt.gz file (will be converted)
#          - Directory containing multiple CpG_report.txt.gz files (auto-discover)
#==============================================================================

set -e  # Exit on any error

# Parse command line arguments
INPUT_PATH="$1"
GTF_FILE="$2"
OUTPUT_DIR="$3"
GROUP_A="${4:-met1}"
GROUP_B="${5:-WT}"

# Validate arguments
if [ -z "$INPUT_PATH" ] || [ -z "$GTF_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 <input_path> <gtf_file> <output_dir> [group_a] [group_b]"
    exit 1
fi

# Setup working directory - use OUTPUT_DIR
WORK_DIR="$OUTPUT_DIR"
mkdir -p "$WORK_DIR"

# Capture the current directory where prod_apps was cloned
PROD_APPS_DIR="$(pwd)/prod_apps"

# Capture the stash mount point (current working directory) before changing dirs
STASH_MOUNT_DIR="$(pwd)"

# Extract GTF basename for use throughout the script
GTF_BASENAME=$(basename "$GTF_FILE")

echo "=============================================="
echo "  MethylC-analyzer Camber Wrapper"
echo "=============================================="
echo ""
echo "Configuration:"
echo "  Input Path:    $INPUT_PATH"
echo "  GTF File:      $GTF_FILE"
echo "  Output Dir:    $OUTPUT_DIR"
echo "  Group A:       $GROUP_A"
echo "  Group B:       $GROUP_B"
echo "=============================================="
echo ""

# Check current directory and find files
echo "[INFO] Current directory: $(pwd)"
echo "[INFO] Looking for input files..."
ls -lah . 2>/dev/null | head -20

# Find input path (file or directory)
INPUT_FOUND=""
IS_DIRECTORY=false

for search_path in "$INPUT_PATH" "./$INPUT_PATH" "/home/camber/$INPUT_PATH" "$(pwd)/$INPUT_PATH"; do
    if [ -d "$search_path" ]; then
        INPUT_FOUND="$search_path"
        IS_DIRECTORY=true
        echo "[INFO] Found input directory at: $INPUT_FOUND"
        break
    elif [ -f "$search_path" ]; then
        INPUT_FOUND="$search_path"
        IS_DIRECTORY=false
        echo "[INFO] Found input file at: $INPUT_FOUND"
        break
    fi
done

if [ -z "$INPUT_FOUND" ]; then
    echo "[ERROR] Input path not found. Searched: $INPUT_PATH"
    echo "[DEBUG] Directory listing:"
    find . -maxdepth 2 -type f -name "*.gz" -o -name "*.CGmap*" -o -type d 2>/dev/null | head -10
    exit 1
fi

# Find GTF file
GTF_FOUND=""
for search_path in "$GTF_FILE" "./$GTF_FILE" "/home/camber/$GTF_FILE" "$(pwd)/$GTF_FILE"; do
    if [ -f "$search_path" ]; then
        GTF_FOUND="$search_path"
        echo "[INFO] Found GTF at: $GTF_FOUND"
        break
    fi
done

if [ -z "$GTF_FOUND" ]; then
    echo "[ERROR] GTF file not found. Searched: $GTF_FILE"
    echo "[DEBUG] Directory listing:"
    find . -name "*gtf*" 2>/dev/null | head -10
    exit 1
fi

# Use GTF file path as-is without copying
echo "[INFO] Using GTF file at: $GTF_FOUND"

# Install pandas if not available (required for conversion script)
echo "[INFO] Installing Python dependencies..."
pip3 install --quiet pandas numpy 2>/dev/null || echo "[WARNING] pandas/numpy may already be installed"

# Process input based on type
if [ "$IS_DIRECTORY" = true ]; then
    echo ""
    echo "=============================================="
    echo "  DIRECTORY MODE: Auto-discovering Bismark reports"
    echo "=============================================="
    echo ""

    # Find all CpG_report files in the directory
    echo "[INFO] Searching for CpG_report.txt.gz files in: $INPUT_FOUND"

    # Search for bismark report files (recursively, up to 3 levels deep)
    REPORT_FILES=$(find "$INPUT_FOUND" -maxdepth 3 -type f \( -name "*CpG_report.txt.gz" -o -name "*report.txt.gz" \) 2>/dev/null | sort)

    if [ -z "$REPORT_FILES" ]; then
        echo "[ERROR] No CpG_report.txt.gz files found in directory: $INPUT_FOUND"
        echo "[DEBUG] Directory contents:"
        find "$INPUT_FOUND" -maxdepth 2 -type f 2>/dev/null | head -20
        exit 1
    fi

    echo "[INFO] Found $(echo "$REPORT_FILES" | wc -l) report file(s):"
    echo "$REPORT_FILES"
    echo ""

    # Convert each report file to CGmap format
    SAMPLE_INDEX=0
    > "$WORK_DIR/samples_list.txt"  # Clear samples list

    for REPORT_FILE in $REPORT_FILES; do
        SAMPLE_INDEX=$((SAMPLE_INDEX + 1))
        REPORT_BASENAME=$(basename "$REPORT_FILE")
        SAMPLE_NAME=$(echo "$REPORT_BASENAME" | sed 's/\.CpG_report\.txt\.gz$//' | sed 's/\.txt\.gz$//')

        echo "[INFO] Processing sample $SAMPLE_INDEX: $SAMPLE_NAME"
        echo "       Source: $REPORT_FILE"

        # Copy report to working directory
        cp "$REPORT_FILE" "$WORK_DIR/$REPORT_BASENAME"

        # Convert to CGmap format
        echo "       Converting to CGmap format..."
        python3 "$PROD_APPS_DIR/bio/methylC/MethylC-analyzer/scripts/methcalls2cgmap.py" \
            -n "$WORK_DIR/$REPORT_BASENAME" \
            -f bismark

        # The conversion creates a file with .CGmap.gz appended
        CONVERTED_FILE="$WORK_DIR/${REPORT_BASENAME}.CGmap.gz"
        FINAL_CGMAP="$WORK_DIR/${SAMPLE_NAME}.CGmap.gz"

        if [ -f "$CONVERTED_FILE" ]; then
            mv "$CONVERTED_FILE" "$FINAL_CGMAP"
            echo "       ✓ Converted: $FINAL_CGMAP"
        else
            echo "[ERROR] Conversion failed for $REPORT_BASENAME"
            exit 1
        fi

        # Assign to groups: first half to GROUP_B (control), second half to GROUP_A (treatment)
        TOTAL_SAMPLES=$(echo "$REPORT_FILES" | wc -l)
        HALF_SAMPLES=$(( (TOTAL_SAMPLES + 1) / 2 ))

        if [ $SAMPLE_INDEX -le $HALF_SAMPLES ]; then
            GROUP="$GROUP_B"
        else
            GROUP="$GROUP_A"
        fi

        # Add to samples list (tab-delimited)
        echo -e "${SAMPLE_NAME}\t${SAMPLE_NAME}.CGmap.gz\t${GROUP}" >> "$WORK_DIR/samples_list.txt"
        echo "       Assigned to group: $GROUP"
        echo ""
    done

    echo "[INFO] ✓ Processed $SAMPLE_INDEX samples successfully"
    echo "[INFO] Samples list:"
    cat "$WORK_DIR/samples_list.txt"
    echo ""

else
    echo ""
    echo "=============================================="
    echo "  SINGLE FILE MODE"
    echo "=============================================="
    echo ""

    # Single file processing
    INPUT_BASENAME=$(basename "$INPUT_FOUND")
    FINAL_CGMAP="$WORK_DIR/sample.CGmap.gz"

    # Check if file is a CX report (Bismark format) that needs conversion
    if [[ "$INPUT_BASENAME" =~ \.txt(\.gz)?$ ]] && [[ ! "$INPUT_BASENAME" =~ \.CGmap\.gz$ ]]; then
        echo "[INFO] Detected Bismark CX report file. Converting to CGmap format..."

        # Copy the CX report file to working directory first
        cp "$INPUT_FOUND" "$WORK_DIR/$INPUT_BASENAME"

        # Run conversion script
        python3 "$PROD_APPS_DIR/bio/methylC/MethylC-analyzer/scripts/methcalls2cgmap.py" \
            -n "$WORK_DIR/$INPUT_BASENAME" \
            -f bismark

        # The conversion creates a file with .CGmap.gz appended
        CONVERTED_FILE="$WORK_DIR/${INPUT_BASENAME}.CGmap.gz"

        if [ -f "$CONVERTED_FILE" ]; then
            mv "$CONVERTED_FILE" "$FINAL_CGMAP"
            echo "[INFO] ✓ Conversion successful: $INPUT_BASENAME → CGmap format"
        else
            echo "[ERROR] Conversion failed. Expected output: $CONVERTED_FILE"
            exit 1
        fi
    else
        echo "[INFO] CGmap format detected. No conversion needed."
        cp "$INPUT_FOUND" "$FINAL_CGMAP"
    fi

    # Create sample replicates for testing (duplicate same file 4 times)
    echo "[INFO] Creating test replicates (duplicating input file)..."
    cp "$FINAL_CGMAP" "$WORK_DIR/wt1.CGmap.gz"
    cp "$FINAL_CGMAP" "$WORK_DIR/wt2.CGmap.gz"
    cp "$FINAL_CGMAP" "$WORK_DIR/met1_1.CGmap.gz"
    cp "$FINAL_CGMAP" "$WORK_DIR/met1_2.CGmap.gz"

    # Create samples_list.txt with replicate structure
    cat > "$WORK_DIR/samples_list.txt" << EOF
wt1	wt1.CGmap.gz	$GROUP_B
wt2	wt2.CGmap.gz	$GROUP_B
met1_1	met1_1.CGmap.gz	$GROUP_A
met1_2	met1_2.CGmap.gz	$GROUP_A
EOF

    echo "[INFO] ✓ Sample files prepared (4 replicates for testing)"
fi

cd "$WORK_DIR"

echo "[INFO] Files prepared successfully"
echo ""

# Create the main setup script with parameterized values
cat > "methylc_setup.sh" << 'MAINSCRIPT'
#!/bin/bash
set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
info() { echo -e "${BLUE}[INFO]${NC} $1"; }

WORK_DIR="__WORK_DIR__"
GTF_FILE_PATH="__GTF_FILE_PATH__"
GTF_FILE_GZ="$GTF_FILE_PATH"
GTF_FILE="${GTF_FILE_GZ%.gz}"
# MethylC-analyzer path will be substituted from outer wrapper
METHYLC_DIR="__PROD_APPS_DIR__/bio/methylC/MethylC-analyzer"
GROUP_A="__GROUP_A__"
GROUP_B="__GROUP_B__"

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Install dependencies using micromamba (faster than conda, no root required)
log "Installing dependencies via micromamba (no root required)..."

# Install micromamba (much faster than miniconda/conda)
if ! command -v micromamba &> /dev/null; then
    info "Installing micromamba..."
    cd /tmp
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
    mkdir -p $HOME/.local/bin
    mv bin/micromamba $HOME/.local/bin/
    export PATH="$HOME/.local/bin:$PATH"
    export MAMBA_ROOT_PREFIX="$HOME/micromamba"
    eval "$(micromamba shell hook --shell bash)"
    micromamba shell init --shell bash --root-prefix=$HOME/micromamba > /dev/null 2>&1 || true
    log "✓ Micromamba installed"
else
    info "Micromamba already available"
    export PATH="$HOME/.local/bin:$PATH"
    export MAMBA_ROOT_PREFIX="$HOME/micromamba"
    eval "$(micromamba shell hook --shell bash)"
fi

# Install R and bedtools via micromamba (much faster)
info "Installing R and bedtools via micromamba (this takes ~5 min)..."
micromamba create -n methylc -c conda-forge -c bioconda -y \
    r-base=4.3 \
    r-gplots \
    r-ggplot2 \
    r-viridis \
    bioconductor-complexheatmap \
    bedtools \
    2>&1 | grep -E "(Downloading|Extracting|Installing|Transaction)" || true

micromamba activate methylc
log "✓ Dependencies installed via micromamba"

# MethylC-analyzer code is already available from prod_apps repo
log "Using MethylC-analyzer from prod_apps repository..."
if [ -d "$METHYLC_DIR" ]; then
    log "✓ MethylC-analyzer found at $METHYLC_DIR"
else
    error "MethylC-analyzer not found at $METHYLC_DIR"
    exit 1
fi

# Install Python dependencies
log "Installing Python packages..."
pip3 install --quiet pandas deeptools scipy matplotlib numpy seaborn pyBigWig PyQt5 argparse
log "✓ Python packages installed"

# R packages already installed via conda above
info "R packages (gplots, ggplot2, viridis, ComplexHeatmap) already installed via conda"

# Create python symlink (if needed)
if [ ! -L "/usr/local/bin/python" ] && [ ! -f "/usr/local/bin/python" ]; then
    ln -s "$(command -v python3)" /usr/local/bin/python 2>/dev/null || true
    info "Python symlink created"
fi

# Extract GTF if needed
info "Checking for GTF files in $WORK_DIR..."
ls -lh "$WORK_DIR"/*.gtf* 2>/dev/null | head -5 || echo "No GTF files found"

if [ ! -f "$GTF_FILE" ]; then
    if [ -f "$GTF_FILE_GZ" ]; then
        info "Extracting GTF from $GTF_FILE_GZ..."
        gunzip -c "$GTF_FILE_GZ" > "$GTF_FILE"
        log "✓ GTF extracted ($(wc -l < $GTF_FILE) lines)"
    else
        error "GTF file not found: $GTF_FILE_GZ"
        exit 1
    fi
else
    info "GTF already extracted: $(wc -l < $GTF_FILE) lines"
fi

# Verify samples_list.txt exists and has content
log "Verifying sample files..."
if [ ! -f "$WORK_DIR/samples_list.txt" ]; then
    error "samples_list.txt not found in $WORK_DIR"
    exit 1
fi

info "samples_list.txt content:"
cat "$WORK_DIR/samples_list.txt"
echo ""

# Verify all CGmap files exist
while IFS=$'\t' read -r sample_name cgmap_file group; do
    if [ ! -f "$WORK_DIR/$cgmap_file" ]; then
        error "CGmap file not found: $WORK_DIR/$cgmap_file"
        exit 1
    fi
    info "✓ Found: $cgmap_file ($(du -h $WORK_DIR/$cgmap_file | cut -f1))"
done < "$WORK_DIR/samples_list.txt"

log "✓ All sample files verified"

# Run analysis (ensure micromamba environment is active)
log "Running MethylC-analyzer..."
echo ""

# Activate micromamba environment
export PATH="$HOME/.local/bin:$PATH"
export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$(micromamba shell hook --shell bash)"
micromamba activate methylc

# Change to work directory and run analysis
cd "$WORK_DIR"
python3 "$METHYLC_DIR/scripts/MethylC.py" \
    samples_list.txt \
    "$(basename "$GTF_FILE")" \
    -a "$GROUP_A" \
    -b "$GROUP_B"

EXIT_CODE=$?
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    log "✓ Analysis completed successfully!"
else
    error "Analysis failed with exit code: $EXIT_CODE"
fi

# List output files
log "Generated output files:"
ls -lh *.txt *.pdf *.png 2>/dev/null | awk '{printf "  %-50s %8s\n", $9, $5}' || true

exit $EXIT_CODE
MAINSCRIPT

# Replace placeholders with actual values
sed -i "s|__WORK_DIR__|$WORK_DIR|g" "methylc_setup.sh"
sed -i "s|__GTF_FILE_PATH__|$GTF_FOUND|g" "methylc_setup.sh"
sed -i "s|__PROD_APPS_DIR__|$PROD_APPS_DIR|g" "methylc_setup.sh"
sed -i "s/__GROUP_A__/$GROUP_A/g" "methylc_setup.sh"
sed -i "s/__GROUP_B__/$GROUP_B/g" "methylc_setup.sh"

# Make script executable
chmod +x "methylc_setup.sh"

# Run the main script
echo "[INFO] Starting MethylC-analyzer pipeline..."
echo ""
bash "methylc_setup.sh"

EXIT_CODE=$?

# Copy results to output directory (which is automatically synced to stash)
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "[INFO] Preparing results for stash upload..."

    # Ensure output is in the working directory where stash is mounted
    # The stash is mounted at /home/camber/workdir (saved in $STASH_MOUNT_DIR)
    # Remove any ./ prefix
    CLEAN_OUTPUT_DIR=$(echo "$OUTPUT_DIR" | sed 's|^\./||')

    # Always place output in stash mount directory (captured at script start)
    if [[ "$CLEAN_OUTPUT_DIR" = /* ]]; then
        # Absolute path - use as is
        STASH_OUTPUT_DIR="$CLEAN_OUTPUT_DIR"
    else
        # Relative path - place in stash mount directory
        STASH_OUTPUT_DIR="$STASH_MOUNT_DIR/$CLEAN_OUTPUT_DIR"
    fi

    echo "[INFO] Output directory: $STASH_OUTPUT_DIR"
    echo "[INFO] Stash mount directory: $STASH_MOUNT_DIR"

    # Ensure directory exists
    mkdir -p "$STASH_OUTPUT_DIR"

    # Copy all output files to output directory
    echo "[INFO] Copying results..."
    cp "$WORK_DIR"/*.txt "$STASH_OUTPUT_DIR/" 2>/dev/null || true
    cp "$WORK_DIR"/*.pdf "$STASH_OUTPUT_DIR/" 2>/dev/null || true
    cp "$WORK_DIR"/*.png "$STASH_OUTPUT_DIR/" 2>/dev/null || true
    cp "$WORK_DIR"/*.bed "$STASH_OUTPUT_DIR/" 2>/dev/null || true

    echo ""
    echo "Output files in $STASH_OUTPUT_DIR:"
    ls -lh "$STASH_OUTPUT_DIR" 2>/dev/null | tail -n +2 || echo "  Directory empty or inaccessible"
    echo ""

    echo "=============================================="
    echo "  Analysis Complete!"
    echo "=============================================="
    echo ""
    echo "Results location: $STASH_OUTPUT_DIR"
fi

exit $EXIT_CODE
