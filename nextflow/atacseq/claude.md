# SLURM Nextflow ATAC-seq Pipeline - Debugging and Setup Documentation

## Project Overview
This document tracks the setup and debugging of the nf-core/atacseq pipeline on the SLURM cluster.

## Current Status: ✅ PIPELINE RUNNING SUCCESSFULLY!

### Latest Status (Job 509)
- **Status**: RUNNING 
- **Processes Executing**: FastQC, TrimGalore, BWA alignment, Samtools stats
- **Containers**: Successfully downloading and executing
- **No Errors**: All processes submitting and running correctly

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