# MethylC-analyzer Camber App

## App Information

- **App Name:** methylc-analyzer
- **App ID:** 112b3601-e93f-4ec3-b5ba-2c2202c24c5e
- **Engine:** MPI
- **Status:** Deployed to Camber Platform ✓

## Files Created

1. **app.json** - App configuration with MPI engine
2. **methylc_wrapper.sh** - Parameterized wrapper script for analysis  
3. **README.md** - This documentation

## Test Data Uploaded to Stash

Location: `stash://ivannovikau32295788/methylc-test/`

- `methylc_wrapper.sh` (7.9KB)
- `GSM5761347_S52_7B_01.CGmap_hq.CGmap.gz` (1.5MB)
- `hg38.ncbiRefSeq.gtf.gz` (39.9MB)

## App Features

### Inputs
- Wrapper script (methylc_wrapper.sh)
- CGmap file (compressed bisulfite sequencing data)
- GTF annotation file (gene annotations)
- Output directory (for results)

### Analysis Pipeline
1. Installs all dependencies (bedtools, R, Python packages)
2. Performs differential methylation analysis (met1 vs WT groups)
3. Generates methylation profiles across genomic features
4. Creates publication-quality visualizations

### System Size Options
- Small (16 CPUs, 90GB RAM) - Test datasets
- Medium (32 CPUs, 180GB RAM) - Recommended
- Large (64 CPUs, 360GB RAM) - Large genomes

## Current Limitation

**Container Compatibility Issue:**
The MethylC-analyzer requires R and bedtools to be installed via apt-get, which needs root access. The current Camber MPI container (`mpi5.0-cpu-v2025.6.19`) runs as a non-root user and does not have sudo available.

**Available in Container:**
- ✓ Python 3.11.7
- ✓ pandas, numpy, scipy
- ✓ git, wget, curl
- ✗ R (required for statistical analysis and plots)
- ✗ bedtools (required for genomic region processing)

## Solutions

### Option 1: Use Custom Container (Recommended)
Create a custom container image based on the MPI image with R and bedtools pre-installed:

```dockerfile
FROM 392513736110.dkr.ecr.us-east-2.amazonaws.com/hpc-base:mpi5.0-cpu-v2025.6.19
USER root
RUN apt-get update && apt-get install -y bedtools r-base
USER camber
```

### Option 2: Run via Camber Jobs CLI
Run the original script directly on a container with root access:

```bash
camber job create --engine mpi --size medium --cmd "bash methylc_complete_setup_and_run.sh" --path "stash://path/"
```

### Option 3: Modify for Available Tools
Rewrite the analysis to use only Python-based tools (BioPython, PyRanges, etc.) instead of R and bedtools.

## Usage

Once container dependencies are resolved, run the app via:

```bash
# Via Camber CLI
camber app run methylc-analyzer \
  --input wrapper_script=stash://path/methylc_wrapper.sh \
  --input cgmap_file=stash://path/data.CGmap.gz \
  --input gtf_file=stash://path/annotation.gtf.gz \
  --input outputDir=stash://path/output

# Via Camber Web UI
# Navigate to Apps → methylc-analyzer → Run
```

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| App creation | ✓ Pass | Successfully created in Camber |
| App deployment | ✓ Pass | Deployed with ID 112b3601-e93f-4ec3-b5ba-2c2202c24c5e |
| Test data upload | ✓ Pass | 3 files uploaded to stash |
| File path resolution | ✓ Pass | Wrapper successfully finds input files |
| Dependency installation | ✗ Fail | Requires root access (R, bedtools) |
| Full analysis | ⏸ Blocked | Waiting for container with dependencies |

## Next Steps

1. Create custom MPI container with R and bedtools pre-installed
2. Update app.json to use custom container image
3. Re-test full analysis pipeline
4. Verify output files in stash

## Technical Details

**App Configuration:**
- Engine Type: MPI
- Default Node Size: MEDIUM (32 CPUs, 180GB RAM)
- Group Comparison: met1 (test) vs WT (control)
- Tags: epigenetics, genomics, analysis, biology

**Expected Outputs:**
- CommonRegion_CG.txt, CommonRegion_CHG.txt, CommonRegion_CHH.txt
- Unionsite.txt
- Average_methylation_levels.pdf
- BED files for genomic features
- PNG heatmaps and profiles

**Expected Runtime:** 10-30 minutes (depends on genome size and coverage)
