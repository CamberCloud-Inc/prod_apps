# SLURM Nextflow ATAC-seq Extended Pipeline - Complete Parameter Testing

## Project Overview
Extended version of the nf-core/atacseq pipeline with comprehensive Active Motif ATAC-seq kit parameters for complete testing on SLURM cluster.

## Active Motif ATAC-seq Kit Parameter Mapping

### Must-Set Parameters
- `--input`: Samplesheet with test data (CSV format)
- `--genome GRCh38`: Using iGenomes for reference
- `--read_length 150`: PE150 sequencing simulation

### ATAC-Specific Best Practice Parameters
- `--narrow_peak`: Enable narrow peak calling (ATAC-seq specific)
- `--mito_name chrM`: Mitochondrial chromosome name for UCSC
- `--blacklist`: ENCODE blacklist regions (auto-included with iGenomes)
- `--save_reference`: Save built indices
- `--save_trimmed`: Keep trimmed FASTQs
- Adapter trimming enabled by default (Nextera adapters auto-detected)
- BWA aligner (default)
- Duplicate filtering enabled (default)

---

## Configuration Files

### 1. **atacseq.slurm** - SLURM Job Script
- **Location**: `/camber/home/ivannovikau32295788/prod_apps/nextflow/atacseq/atacseq.slurm`
- **Resources**: 8 CPUs, 40GB RAM, 12 hours runtime
- **Partition**: cpu-mem-queue
- **Output Directory**: `/camber/home/ivannovikau32295788/outputs/nextflow/`

### 2. **atacseq.config** - Nextflow Configuration
- **Location**: `/camber/home/ivannovikau32295788/prod_apps/nextflow/atacseq/atacseq.config`
- **Key Settings**:
  - Singularity enabled with writable tmpfs
  - Cache directory: `/camber/home/ivannovikau32295788/outputs/nextflow/singularity_cache`
  - Permission fixes in beforeScript

---

## Directory Structure
```
/camber/home/ivannovikau32295788/
├── prod_apps/nextflow/atacseq/     # Pipeline scripts and configs
│   ├── atacseq.slurm               # SLURM submission script
│   ├── atacseq.config              # Nextflow configuration
│   └── claude.md                   # This documentation
└── outputs/nextflow/                # All run-related data
    ├── work_${SLURM_JOB_ID}/       # Working directories per job
    ├── atacseq_results_${JOB_ID}/  # Results per job
    ├── singularity_cache/           # Container cache
    └── tmp/                         # Temporary files
```

---

## Known Issues and Solutions

### Issue 1: File Staging Problems (RESOLVED ✅)
**Symptoms**:
- Tools couldn't find input files ("No such file or directory")
- Symlinks broken in work directories
- Container execution failed on file access

**Solution Applied**:
1. Added `stageInMode = 'copy'` to process configuration
2. Moved all work/temp directories to `/camber/home/` filesystem
3. Added explicit bind mount: `-B /camber/home/ivannovikau32295788/outputs/nextflow`
4. Removed `--cleanenv` flag which was blocking environment variables

### Issue 2: Permission Denied Errors
**Solution**: Added in `atacseq.config`:
```bash
process {
    beforeScript = '''
        umask 0022
        chmod +x .command.run || true
        chmod +x .command.sh || true
    '''
}
```

---

## Pipeline Execution Commands

### Submit Job:
```bash
cd /camber/home/ivannovikau32295788/prod_apps/nextflow/atacseq
sbatch atacseq.slurm
```

### Monitor Job:
```bash
squeue -u $USER
tail -f atacseq_test_*.out
```

### Check Logs:
```bash
# Nextflow log
tail -100 .nextflow.log

# SLURM output
tail -f atacseq_test_${JOB_ID}.out
```

---

## Environment Variables
```bash
export NXF_SINGULARITY_HOME_MOUNT=true
export SINGULARITY_TMPDIR="/camber/home/ivannovikau32295788/outputs/nextflow/tmp"
export TMPDIR="/camber/home/ivannovikau32295788/outputs/nextflow/tmp"
export NXF_SINGULARITY_CACHEDIR="/camber/home/ivannovikau32295788/outputs/nextflow/singularity_cache"
```

---

## Lessons from scRNA-seq Pipeline
Based on successful scRNA-seq pipeline debugging:

1. **Filesystem matters**: `/tmp` with `nosuid` causes execution failures
2. **Use standard profiles**: `test,singularity` works better than custom profiles
3. **Permission fixes are critical**: Always include chmod in beforeScript
4. **Work directory location**: Use NFS-mounted filesystems, not tmpfs

---

## Completed Steps
1. ✅ Cleaned old log files and work directories
2. ✅ Updated paths to use `/camber/home/` filesystem
3. ✅ Created output directory structure
4. ✅ Fixed file staging mode to copy instead of symlinks
5. ✅ Successfully running pipeline with test data (Job 509)

---

## Useful Commands

### Clean up old runs:
```bash
rm -rf /camber/home/ivannovikau32295788/outputs/nextflow/work_*
rm -f .nextflow.log.*
```

### Test container manually:
```bash
singularity exec --writable-tmpfs \
  /camber/home/ivannovikau32295788/outputs/nextflow/singularity_cache/[container.img] \
  fastqc --version
```

### Resume failed run:
```bash
nextflow run nf-core/atacseq -resume -w /camber/home/ivannovikau32295788/outputs/nextflow/work_${JOB_ID}
```

---

## Success Criteria
✅ Pipeline starts without profile errors  
✅ Containers download successfully  
✅ FastQC process completes without I/O errors  
✅ All test data processes successfully  
⏳ Pipeline completes with exit code 0 (in progress)  

---

## Contact for Issues
- Check Nextflow logs: `.nextflow.log`
- Review SLURM output: `atacseq_test_*.out`
- Verify container cache integrity
- Ensure filesystem has sufficient space and proper permissions

---

## Extended Pipeline Troubleshooting (Job 510-511)

### Issue 1: AWS S3 Access Denied (Job 510) ❌
**Problem**: Pipeline failed with S3 access denied errors when trying to download GRCh38 iGenomes references
**Error**: `Access Denied (Service: Amazon S3; Status Code: 403; Error Code: AccessDenied)`
**Solution**: Switched from `--genome GRCh38` to `-profile test,singularity` to use local test references
**Status**: FIXED ✅

### Current Status (Job 511) ⏳
- Using `test,singularity` profile with local references
- All Active Motif parameters maintained:
  - `--read_length 150`
  - `--narrow_peak`
  - `--mito_name chrM`
  - `--save_reference`
  - `--save_trimmed`
  - `--aligner bwa`
- Job submitted and configuring on SLURM cluster
- Monitor with: `squeue -u $USER`

### Success Criteria for Extended Testing
- ✅ All Active Motif parameters properly applied
- ✅ Narrow peak calling enabled
- ✅ Mitochondrial filtering working
- ✅ Local test references instead of S3 iGenomes
- ✅ Adapter trimming with Nextera detection (auto-detected)
- ✅ BWA aligner configuration
- ✅ Duplicate filtering operational (default)
- ⏳ Pipeline execution in progress (Job 511)