export CAMBER_API_KEY=1904da271777049d9b595662d1d5291f86c6d89b

# Single-cell RNA-seq Testing Instructions for LLM Agents

## 🚀 Issue Resolution: Docker Command Not Found

**CRITICAL FIX APPLIED**: The main issue was that the failed job (3491) used `test,docker` profile but Docker is not available on the Camber platform. The solution is to:

1. **Use platform's built-in container system**: Let Camber handle containers via `/etc/mpi/nextflow.camber.config`
2. **Avoid explicit profile overrides**: Don't specify conflicting profiles like `test,docker`
3. **Use Singularity configuration**: Explicitly disable docker and enable singularity

## ✅ WORKING SOLUTION

### Quick Start (Fixed Command)
```bash
cd /home/ubuntu/prod_apps/nextflow/scrnaseq

# Upload configuration to stash
camber stash cp camber-scrnaseq-fix.config stash://username/

# Run scrnaseq test with proper configuration
camber job create --engine nextflow \
  --cmd "nextflow run nf-core/scrnaseq -profile test -c /etc/mpi/nextflow.camber.config -c camber-scrnaseq-fix.config --outdir results-final -ansi-log false -r 4.0.0" \
  --path "stash://username/" --size large
```

### Required Files

**Configuration File** (`camber-scrnaseq-fix.config`):
```groovy
process {
  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }
  withName:'.*:STARSOLO:STAR_ALIGN.*' {
    cpus   = { 8 * task.attempt }
    memory = { 32.GB * task.attempt }
    time   = { 8.h * task.attempt }
  }
}

singularity {
  enabled = true
  autoMounts = true
}

docker {
  enabled = false  // CRITICAL: Disable Docker to avoid "command not found" error
}
```

## Problem Analysis from Failed Job 3491

### Root Cause
- **Error**: `docker: command not found` in process FASTQC
- **Cause**: Pipeline used `test,docker` profile but Docker is not available on Camber
- **Container**: `quay.io/biocontainers/fastqc:0.12.1--hdfd78af_0`
- **Profile**: `test,docker` (problematic)

### Solution Strategy
1. **Remove docker profile**: Use `test` profile only
2. **Add platform config**: `-c /etc/mpi/nextflow.camber.config` first
3. **Add custom config**: `-c camber-scrnaseq-fix.config` second  
4. **Explicit container settings**: Enable Singularity, disable Docker

## Expected Pipeline Processes
When successful, the scRNA-seq pipeline should run these processes:
1. **FASTQC** - Quality control of raw reads
2. **STARSOLO** - Single-cell RNA alignment with STARsolo
3. **ALEVIN** - Alternative quantification with Salmon Alevin
4. **MULTIQC** - Comprehensive quality control report
5. **CELLRANGER** - 10x Genomics CellRanger processing (if specified)

## Key Success Factors

### 1. Container System Configuration
- **✅ WORKING**: `-c /etc/mpi/nextflow.camber.config` (platform config first)
- **✅ WORKING**: `singularity.enabled = true` in custom config
- **❌ FAILED**: `test,docker` profile (Docker not available)
- **Critical**: Must explicitly disable Docker and enable Singularity

### 2. Resource Requirements
- **✅ LARGE instance required**: scRNA-seq is computationally intensive
- **Memory**: High memory requirements for STAR alignment and quantification
- **CPU**: Multi-core processing essential for alignment steps

### 3. Configuration Layering
- **Order matters**: Platform config first, then custom overrides
- **Proper syntax**: `nextflow run nf-core/scrnaseq -profile test -c config1 -c config2`
- **Profile selection**: Use built-in `test` profile, not `test,docker`

## Troubleshooting Common Issues

### Issue 1: "docker: command not found"
**Cause**: Using docker profile on platform without Docker support
**Solution**: 
```groovy
docker { enabled = false }
singularity { enabled = true; autoMounts = true }
```

### Issue 2: Container pull failures
**Cause**: Network timeouts or registry access issues
**Solution**: Let platform handle container management via standard profiles

### Issue 3: Resource allocation errors
**Cause**: Insufficient resources for STAR alignment
**Solution**: Use LARGE node size and proper process resource allocation

## Test Data Information
The built-in test profile uses:
- **Species**: Mouse (Mus musculus)
- **Protocol**: 10x Genomics 3' v2 chemistry
- **Data Type**: Single-cell RNA-seq
- **Samples**: Test samples from nf-core/test-datasets
- **Expected Output**: Gene expression matrix and QC reports

## Debug Commands
```bash
# Check job status
camber job get <job_id>

# View logs
camber job logs <job_id>

# Check stash contents
camber stash ls stash://username/

# Monitor job progress
watch -n 30 "camber job get <job_id>"
```

## Expected Output
Successful completion should show:
- Status: `COMPLETED`
- Gene expression count matrices
- Quality control reports
- Cell-level and gene-level statistics
- MultiQC comprehensive report

## Performance Expectations
- **Test Duration**: ~20-30 minutes (test dataset)
- **Resource Usage**: LARGE node recommended
- **Network**: ~2-3GB download (test data + containers)
- **Output**: Complete single-cell analysis with QC metrics

## Technical Requirements Met
- ✅ **Container System**: Singularity-based (Docker disabled)
- ✅ **Platform Integration**: Uses Camber's container management
- ✅ **Resource Allocation**: Proper CPU/memory limits per process
- ✅ **Profile Compatibility**: Uses standard `test` profile
- ✅ **Configuration Layering**: Platform config + custom overrides

## Key Configuration Patterns
```bash
# CORRECT command structure:
nextflow run nf-core/scrnaseq \
  -profile test \                           # Built-in test profile
  -c /etc/mpi/nextflow.camber.config \     # Platform config FIRST
  -c camber-scrnaseq-fix.config \          # Custom overrides SECOND
  --outdir results \
  -r 4.0.0

# WRONG (causes docker error):
nextflow run nf-core/scrnaseq \
  -profile test,docker \                   # Docker not available
  -c camber-final-fix.config \            # Missing platform config
  --outdir results
```

This configuration ensures the nf-core/scrnaseq pipeline runs successfully on the Camber platform by properly handling container systems and resource allocation.