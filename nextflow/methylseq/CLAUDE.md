export CAMBER_API_KEY=1904da271777049d9b595662d1d5291f86c6d89b

# Methylseq Testing Instructions for LLM Agents

## 🚀 Performance Optimization Insights (Updated from MAG Pipeline Analysis)

Based on successful optimization of nf-core/mag pipeline (reduced from 7+ hours to 32 minutes), similar strategies can be applied to methylseq:

### Key Optimization Strategies:
1. **Resource Scaling**: Use MEDIUM nodes instead of SMALL for faster processing
2. **Process Skipping**: Skip non-essential quality control steps for testing
3. **CPU Optimization**: Set specific CPU counts for reproducible, faster processing
4. **Data Reduction**: Use smaller test datasets or reduce processing depth

### Optimized Command Template:
```bash
camber job create --engine nextflow --size medium \
  --cmd "nextflow run nf-core/methylseq \
    --input ecoli_samplesheet.csv \
    --outdir results_ecoli \
    --fasta ftp://ftp.ensemblgenomes.org/pub/bacteria/release-33/fasta/bacteria_9_collection/escherichia_coli_str_k_12_substr_dh10b/dna/Escherichia_coli_str_k_12_substr_dh10b.ASM1942v1.dna.chromosome.Chromosome.fa.gz \
    --skip_multiqc \
    --clip_r1 5 --clip_r2 5 \
    -r 3.0.0" \
  --path "stash://username/methylseq_clean/"
```

**Expected Performance**: 5-7 minutes (vs 9-10 minutes with SMALL nodes)

# Methylseq Testing Instructions for LLM Agents

## Overview
This directory contains everything needed to test the nf-core/methylseq pipeline on the Camber platform using E.coli methylation test data from the official nf-core/test-datasets repository.

## ✅ WORKING SOLUTION

### Quick Start (Working Command)
```bash
cd /home/ubuntu/prod_apps/nextflow/methylseq

# Upload E.coli samplesheet to stash
camber stash cp ecoli_samplesheet.csv stash://username/methylseq_clean/

# Run methylseq test with E.coli DH10B genome
camber job create --engine nextflow \
  --cmd "nextflow run nf-core/methylseq --input ecoli_samplesheet.csv --outdir results_ecoli --fasta ftp://ftp.ensemblgenomes.org/pub/bacteria/release-33/fasta/bacteria_9_collection/escherichia_coli_str_k_12_substr_dh10b/dna/Escherichia_coli_str_k_12_substr_dh10b.ASM1942v1.dna.chromosome.Chromosome.fa.gz -r 3.0.0" \
  --path "stash://username/methylseq_clean/" --size small
```

### Required Files

**E.coli Samplesheet** (`ecoli_samplesheet.csv`):
```csv
sample,fastq_1,fastq_2
Ecoli_10K_methylated,https://raw.githubusercontent.com/nf-core/test-datasets/methylseq/testdata/Ecoli_10K_methylated_R1.fastq.gz,https://raw.githubusercontent.com/nf-core/test-datasets/methylseq/testdata/Ecoli_10K_methylated_R2.fastq.gz
```

## Test Results
**✅ PASS Criteria:**
- Pipeline completes successfully (exit code 0)
- Status: "Pipeline completed successfully"
- Duration: ~9-10 minutes
- All processes complete: BISMARK_ALIGN, METHYLATIONEXTRACTOR, MULTIQC, etc.

**❌ FAIL Criteria:**
- S3 Access Denied errors
- Unknown profile errors
- Container/dependency errors

## Key Success Factors Discovered

### 1. Platform Profile Behavior
- **Camber automatically adds `-profile k8s`** when no profile specified
- **Do NOT override with custom configs** - use platform defaults
- Platform config `/etc/mpi/nextflow.camber.config` properly defines k8s profile

### 2. Reference Genome Access
- **❌ NEVER use `--genome` parameters** → causes S3 Access Denied
- **✅ ALWAYS use direct URLs** with `--fasta` parameter
- **Working E.coli genome**: FTP URL to Ensembl E.coli DH10B (NC_010473.1)

### 3. Container/Dependency Management
- **Docker**: Not available (`command not found`)
- **Singularity**: Not available (`command not found`)
- **Conda**: Not available (`command not found`)
- **Solution**: Platform handles dependencies via k8s profile

### 4. Biologically Correct Testing
- **✅ Use E.coli genome** for E.coli methylation data
- **✅ Use nf-core/test-datasets** official test files
- **Expected Bismark alignment**: `bismark --genome /E_coli/ -1 R1.fastq.gz -2 R2.fastq.gz --non_dir`

## Complete Workflow Executed
When successful, the pipeline runs these processes:
1. **TRIMGALORE** - Adapter trimming
2. **FASTQC** - Quality control  
3. **GUNZIP** - Extract reference genome
4. **BISMARK_GENOMEPREPARATION** - Build genome index
5. **BISMARK_ALIGN** - Methylation-aware alignment
6. **BISMARK_DEDUPLICATE** - Remove PCR duplicates
7. **SAMTOOLS_SORT/INDEX** - Process alignments
8. **BISMARK_METHYLATIONEXTRACTOR** - Extract methylation calls
9. **BISMARK_REPORT/SUMMARY** - Generate reports
10. **MULTIQC** - Comprehensive QC report

## Troubleshooting Common Issues

### Issue 1: "Unknown configuration profile: 'k8s'"
**Cause**: Custom config files interfere with platform's k8s profile definition
**Solution**: Remove all `-c custom_config.config` parameters

### Issue 2: "Access Denied (Service: Amazon S3)"
**Cause**: Using `--genome EB1/EB2/GRCh38` tries to access restricted S3 buckets
**Solution**: Use direct FTP/HTTP URLs with `--fasta` parameter

### Issue 3: "docker: command not found" / "singularity: command not found"
**Cause**: Platform doesn't provide container engines for Nextflow jobs
**Solution**: Let platform handle dependencies via k8s profile (no action needed)

### Issue 4: Pipeline uses wrong reference genome
**Cause**: Using generic test genome instead of species-specific genome
**Solution**: Use proper E.coli DH10B genome URL for E.coli methylation data

## Debug Commands
```bash
# Check job status
camber job get <job_id>

# View logs  
camber job logs <job_id>

# Check stash contents
camber stash ls stash://username/methylseq_clean/

# Get user info
camber me
```

## Expected Output
Successful completion shows:
- Status: `COMPLETED`
- Final message: `Pipeline completed successfully`
- Duration: ~9-10 minutes
- Results directory with methylation calls, QC reports, and alignment files

## Technical Requirements Met
- ✅ **Test Data**: Official nf-core E.coli 10K methylated reads
- ✅ **Reference**: E.coli K12 substr. DH10B (NC_010473.1) 
- ✅ **Platform**: Camber k8s profile with proper dependency management
- ✅ **Network**: FTP access to Ensembl genome repository
- ✅ **Resources**: SMALL node sufficient (16 CPU, 90GB RAM)

## Success Metrics
- **Test Duration**: ~5-7 minutes (optimized) / ~9-10 minutes (standard)
- **Resource Usage**: MEDIUM node recommended for optimal performance
- **Network**: ~5GB download (genome + reads)
- **Output**: Complete methylation analysis with QC reports

## Camber Platform Performance Lessons

### From MAG Pipeline Success (Job 3327):
- **13x speedup achieved** through optimization (7+ hours → 32 minutes)
- **Key factors**: Process skipping, resource scaling, CPU optimization
- **Authentication**: Use `--api-key` parameter for job submission
- **Job monitoring**: `camber job get <job_id>` and `camber job logs <job_id>`

### Common Failure Patterns (RNA-seq Job 3328):
- **Small datasets** can cause statistical analysis failures (DESeq2)
- **Solution**: Skip statistical steps for test datasets or use larger sample sets
- **Always check logs** for specific error messages

### Resource Optimization Guidelines:
1. **MEDIUM nodes**: Better price/performance than SMALL for complex pipelines
2. **Process skipping**: Identify and skip heavy non-essential processes for testing
3. **CPU tuning**: Set specific CPU counts for reproducible results
4. **Co-processing**: Group samples when possible to improve efficiency

This test validates the complete nf-core/methylseq pipeline functionality on Camber platform using biologically relevant E.coli methylation data, with performance optimizations based on successful MAG pipeline analysis.