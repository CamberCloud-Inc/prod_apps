#!/bin/bash
#==============================================================================
# MethylC-analyzer Wrapper Script for Camber Platform
#
# This wrapper script accepts parameters from the Camber app and runs the
# main setup and analysis script with custom configuration.
#
# Usage: bash methylc_wrapper.sh <cgmap_file> <gtf_file> <output_dir> <group_a> <group_b>
#==============================================================================

set -e  # Exit on any error

# Parse command line arguments
CGMAP_FILE="$1"
GTF_FILE="$2"
OUTPUT_DIR="$3"
GROUP_A="${4:-met1}"
GROUP_B="${5:-WT}"

# Validate arguments
if [ -z "$CGMAP_FILE" ] || [ -z "$GTF_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 <cgmap_file> <gtf_file> <output_dir> [group_a] [group_b]"
    exit 1
fi

# Setup working directory
WORK_DIR="/home/camber/manu"
mkdir -p "$WORK_DIR"

# Capture the current directory where prod_apps was cloned
PROD_APPS_DIR="$(pwd)/prod_apps"

echo "=============================================="
echo "  MethylC-analyzer Camber Wrapper"
echo "=============================================="
echo ""
echo "Configuration:"
echo "  CGmap File:    $CGMAP_FILE"
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

# Try to find the files in various locations
CGMAP_FOUND=""
GTF_FOUND=""

# Search for files
for search_path in "$CGMAP_FILE" "./$CGMAP_FILE" "/home/camber/$CGMAP_FILE" "$(pwd)/$CGMAP_FILE"; do
    if [ -f "$search_path" ]; then
        CGMAP_FOUND="$search_path"
        echo "[INFO] Found CGmap at: $CGMAP_FOUND"
        break
    fi
done

for search_path in "$GTF_FILE" "./$GTF_FILE" "/home/camber/$GTF_FILE" "$(pwd)/$GTF_FILE"; do
    if [ -f "$search_path" ]; then
        GTF_FOUND="$search_path"
        echo "[INFO] Found GTF at: $GTF_FOUND"
        break
    fi
done

if [ -z "$CGMAP_FOUND" ]; then
    echo "[ERROR] CGmap file not found. Searched: $CGMAP_FILE"
    echo "[DEBUG] Directory listing:"
    find . -name "*.gz" -o -name "*.CGmap*" 2>/dev/null | head -10
    exit 1
fi

if [ -z "$GTF_FOUND" ]; then
    echo "[ERROR] GTF file not found. Searched: $GTF_FILE"
    echo "[DEBUG] Directory listing:"
    find . -name "*gtf*" 2>/dev/null | head -10
    exit 1
fi

# Check file type and convert if needed
echo "[INFO] Checking input file type..."
CGMAP_BASENAME=$(basename "$CGMAP_FOUND")
FINAL_CGMAP="$WORK_DIR/GSM5761347_S52_7B_01.CGmap_hq.CGmap.gz"

# Check if file is a CX report (Bismark format) that needs conversion
if [[ "$CGMAP_BASENAME" =~ \.txt(\.gz)?$ ]] && [[ ! "$CGMAP_BASENAME" =~ \.CGmap\.gz$ ]]; then
    echo "[INFO] Detected Bismark CX report file. Converting to CGmap format..."

    # Copy the CX report file to working directory first
    cp "$CGMAP_FOUND" "$WORK_DIR/$CGMAP_BASENAME"

    # Install pandas if not available (required for conversion script)
    pip3 install --quiet pandas numpy 2>/dev/null || echo "[WARNING] pandas/numpy may already be installed"

    # Run conversion script
    python3 "$PROD_APPS_DIR/bio/methylC/MethylC-analyzer/scripts/methcalls2cgmap.py" \
        -n "$WORK_DIR/$CGMAP_BASENAME" \
        -f bismark

    # The conversion creates a file with .CGmap.gz appended
    CONVERTED_FILE="$WORK_DIR/${CGMAP_BASENAME}.CGmap.gz"

    if [ -f "$CONVERTED_FILE" ]; then
        mv "$CONVERTED_FILE" "$FINAL_CGMAP"
        echo "[INFO] ✓ Conversion successful: $CGMAP_BASENAME → CGmap format"
    else
        echo "[ERROR] Conversion failed. Expected output: $CONVERTED_FILE"
        exit 1
    fi
else
    echo "[INFO] CGmap format detected. No conversion needed."
    cp "$CGMAP_FOUND" "$FINAL_CGMAP"
fi

# Copy GTF file to working directory
echo "[INFO] Copying GTF file to $WORK_DIR..."
cp "$GTF_FOUND" "$WORK_DIR/hg38.ncbiRefSeq.gtf.gz"

cd "$WORK_DIR"

echo "[INFO] Files prepared successfully"
echo ""

# Create the main setup script with parameterized values
cat > "$WORK_DIR/methylc_setup.sh" << 'MAINSCRIPT'
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

WORK_DIR="/home/camber/manu"
SOURCE_CGMAP="$WORK_DIR/GSM5761347_S52_7B_01.CGmap_hq.CGmap.gz"
GTF_FILE_GZ="$WORK_DIR/hg38.ncbiRefSeq.gtf.gz"
GTF_FILE="$WORK_DIR/hg38.ncbiRefSeq.gtf"
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

# Create sample replicates with absolute paths
log "Creating sample replicates..."
cp "$SOURCE_CGMAP" "$WORK_DIR/wt1.CGmap.gz"
cp "$SOURCE_CGMAP" "$WORK_DIR/wt2.CGmap.gz"
cp "$SOURCE_CGMAP" "$WORK_DIR/met1_1.CGmap.gz"
cp "$SOURCE_CGMAP" "$WORK_DIR/met1_2.CGmap.gz"

# Create samples_list.txt with absolute path
cat > "$WORK_DIR/samples_list.txt" << 'EOF'
wt1	wt1.CGmap.gz	WT
wt2	wt2.CGmap.gz	WT
met1_1	met1_1.CGmap.gz	met1
met1_2	met1_2.CGmap.gz	met1
EOF

log "✓ Sample files prepared"
info "samples_list.txt created at: $WORK_DIR/samples_list.txt"
ls -lh "$WORK_DIR"/samples_list.txt "$WORK_DIR"/*.CGmap.gz 2>/dev/null | head -5

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
python3 "$METHYLC_DIR/scripts/MethylC.py" run \
    samples_list.txt \
    hg38.ncbiRefSeq.gtf \
    "$WORK_DIR/" \
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
sed -i "s|__PROD_APPS_DIR__|$PROD_APPS_DIR|g" "$WORK_DIR/methylc_setup.sh"
sed -i "s/__GROUP_A__/$GROUP_A/g" "$WORK_DIR/methylc_setup.sh"
sed -i "s/__GROUP_B__/$GROUP_B/g" "$WORK_DIR/methylc_setup.sh"

# Make script executable
chmod +x "$WORK_DIR/methylc_setup.sh"

# Run the main script
echo "[INFO] Starting MethylC-analyzer pipeline..."
echo ""
bash "$WORK_DIR/methylc_setup.sh"

EXIT_CODE=$?

# Copy results to output directory (stash)
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "[INFO] Preparing results for upload to stash..."

    # Create temporary results directory
    RESULTS_DIR="/tmp/methylc_results"
    mkdir -p "$RESULTS_DIR"

    # Copy all output files to temp directory
    cp "$WORK_DIR"/*.txt "$RESULTS_DIR/" 2>/dev/null || true
    cp "$WORK_DIR"/*.pdf "$RESULTS_DIR/" 2>/dev/null || true
    cp "$WORK_DIR"/*.png "$RESULTS_DIR/" 2>/dev/null || true
    cp "$WORK_DIR"/*.bed "$RESULTS_DIR/" 2>/dev/null || true

    echo "[INFO] Files prepared in $RESULTS_DIR"
    echo ""
    echo "Output files:"
    ls -lh "$RESULTS_DIR" | tail -n +2
    echo ""

    # Copy results to stash using camber CLI
    echo "[INFO] Uploading results to stash: $OUTPUT_DIR"
    if command -v camber >/dev/null 2>&1; then
        camber stash cp -r "$RESULTS_DIR" "$OUTPUT_DIR/" || echo "[WARNING] Failed to upload to stash, results are in $RESULTS_DIR"
    else
        echo "[WARNING] camber CLI not available, results remain in $RESULTS_DIR"
    fi

    echo ""
    echo "=============================================="
    echo "  Analysis Complete!"
    echo "=============================================="
    echo ""
    echo "Results location: $RESULTS_DIR"
    echo "Stash location: $OUTPUT_DIR"
fi

exit $EXIT_CODE
