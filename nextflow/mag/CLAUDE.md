export CAMBER_API_KEY=1904da271777049d9b595662d1d5291f86c6d89b

# MAG Testing Instructions for LLM Agents

## Overview
This directory contains everything needed to test the nf-core/mag pipeline on the Camber platform using minigut metagenomics test data from the official nf-core/test-datasets repository.

## ✅ WORKING SOLUTION

### Quick Start (Working Command)
```bash
cd /home/ubuntu/prod_apps/nextflow/mag

# Upload samplesheet to root stash directory (CRITICAL for file permissions)
camber stash cp samplesheet.csv stash://username/

# Run mag test with official nf-core test data
camber job create --engine nextflow \
  --cmd "nextflow run nf-core/mag --input samplesheet.csv -r 3.0.1 --skip_krona --skip_gtdbtk --skip_maxbin2 --skip_prokka --skip_prodigal" \
  --path "stash://username/" --size medium
```

**CRITICAL**: Must use root stash directory (`stash://username/`) not subdirectories for proper file permissions.

### Required Files

**Official Test Samplesheet** (`samplesheet.csv`):
```csv
sample,group,short_reads_1,short_reads_2,long_reads
test_minigut,0,https://github.com/nf-core/test-datasets/raw/mag/test_data/test_minigut_R1.fastq.gz,https://github.com/nf-core/test-datasets/raw/mag/test_data/test_minigut_R2.fastq.gz,
test_minigut_sample2,0,https://github.com/nf-core/test-datasets/raw/mag/test_data/test_minigut_sample2_R1.fastq.gz,https://github.com/nf-core/test-datasets/raw/mag/test_data/test_minigut_sample2_R2.fastq.gz,
```

**Alternative: Full-size Test Data** (for comprehensive testing):
Based on Bertrand et al. Nature Biotechnology (2019) gut metagenome data:
- CAPES S11: ERR3201918 (Illumina), ERR3201942 (ONT)
- CAPES S21: ERR3201928 (Illumina), ERR3201952 (ONT)  
- CAPES S7: ERR3201914 (Illumina), ERR3201938 (ONT)

**Run Script** (`run_mag.sh`):
```bash
#!/bin/bash

kraken2_db="https://raw.githubusercontent.com/nf-core/test-datasets/mag/test_data/minigut_kraken.tgz"
centrifuge_db="https://raw.githubusercontent.com/nf-core/test-datasets/mag/test_data/minigut_cf.tar.gz"
busco_db="https://busco-data.ezlab.org/v5/data/lineages/bacteria_odb10.2024-01-08.tar.gz"
gtdb_db="https://data.ace.uq.edu.au/public/gtdb/data/releases/release220/220.0/auxillary_files/gtdbtk_package/full_package/gtdbtk_r220_data.tar.gz"

nextflow run nf-core/mag \
    -r 3.4.0 \
    --input samplesheet.csv \
    --outdir /camber_outputs \
    --kraken2_db "$kraken2_db" \
    --centrifuge_db "$centrifuge_db" \
    --busco_db "$busco_db" \
    --gtdb_db "$gtdb_db" \
    --skip_krona true \
    --skip_gtdbtk true \
    --skip_maxbin2 true
```

## Test Results

### ✅ Test Results Summary
- **Job ID 3307-3314**: FAILED - Various permission issues with subdirectory stash paths
- **Job ID 3315**: SUCCESS - Running with root stash directory (`stash://username/`)
- **Engine Size**: MEDIUM required (SMALL insufficient)
- **Key Solution**: Root stash directory required for .params file creation permissions
- **Status**: Pipeline executing successfully with processes running:
  - BOWTIE2_PHIX_REMOVAL_BUILD, FASTP, FASTQC_RAW, BOWTIE2_PHIX_REMOVAL_ALIGN

### Expected Pipeline Processes
When successful, the MAG pipeline should run these processes:
1. **FASTQC** - Quality control of raw reads
2. **FASTP** - Read preprocessing and adapter trimming  
3. **KRAKEN2_KRAKEN2** - Taxonomic classification
4. **CENTRIFUGE_CENTRIFUGE** - Alternative taxonomic classification
5. **MEGAHIT** - Metagenomic assembly
6. **QUAST** - Assembly quality assessment
7. **BOWTIE2_BUILD** - Reference indexing
8. **BOWTIE2_ALIGN** - Read mapping to assemblies
9. **METABAT2_METABAT2** - Genome binning
10. **CHECKM_LINEAGEWF** - Bin quality assessment
11. **GTDBTK_CLASSIFYWF** - Taxonomic classification of MAGs
12. **BUSCO** - Completeness assessment
13. **MULTIQC** - Comprehensive QC report

## Key Success Factors Discovered

### 1. Root Stash Directory is Essential
- **✅ WORKING**: `--path "stash://username/"` (root directory)
- **❌ FAILED**: `--path "stash://username/subdirectory/"` (permission denied)
- **Critical**: .params_YYYY-MM-DD_HH-mm-ss.json file creation requires root stash permissions

### 2. Resource Requirements
- **✅ MEDIUM instance required**: More resource-intensive than methylseq  
- **❌ SMALL instance insufficient**: Failed due to resource constraints
- **Memory**: Higher requirements for metagenomics assembly and binning

### 3. Database Management
- **✅ Test profile handles databases**: No manual database downloads needed
- **❌ Manual database URLs**: Can cause timeouts and storage issues
- **Skip resource-intensive steps**: --skip_krona --skip_gtdbtk --skip_maxbin2

## Key Configuration Differences from Methylseq

### 1. Database Requirements
- **MAG pipeline requires multiple databases**: Kraken2, Centrifuge, BUSCO, GTDB
- **Large database sizes**: GTDB alone is ~27GB
- **Network-intensive**: Downloads multiple databases during execution

### 2. Resource Requirements
- **Higher memory usage**: Metagenomics assembly and binning
- **Longer runtime**: Multiple assembly and classification steps
- **Storage intensive**: Large intermediate files and databases

### 3. Test Data Characteristics
- **Metagenomics data**: Mixed microbial community reads
- **Two samples**: test_minigut and test_minigut_sample2
- **Paired-end Illumina**: No long reads in current test
- **Small test dataset**: Subset of gut microbiome data

## Troubleshooting

### Issue 1: "Cannot create work-dir" Permission Error
**Cause**: Nextflow trying to create work directory in read-only location
**Solution**: Specify alternative work directory with `-w` parameter

### Issue 2: Database Download Failures
**Cause**: Large database files may timeout or fail to download
**Solution**: Use smaller test databases or skip resource-intensive steps

### Issue 3: Memory/Resource Constraints
**Cause**: MAG pipeline is more resource-intensive than methylseq
**Solution**: May need larger instance size or resource optimization

## Database URLs Used
- **Kraken2**: https://raw.githubusercontent.com/nf-core/test-datasets/mag/test_data/minigut_kraken.tgz
- **Centrifuge**: https://raw.githubusercontent.com/nf-core/test-datasets/mag/test_data/minigut_cf.tar.gz  
- **BUSCO**: https://busco-data.ezlab.org/v5/data/lineages/bacteria_odb10.2024-01-08.tar.gz
- **GTDB**: https://data.ace.uq.edu.au/public/gtdb/data/releases/release220/220.0/auxillary_files/gtdbtk_package/full_package/gtdbtk_r220_data.tar.gz

## Debug Commands
```bash
# Check job status
camber job get <job_id>

# View logs  
camber job logs <job_id>

# Check stash contents
camber stash ls stash://username/mag_test/

# Get user info
camber me
```

## Expected Output
Successful completion should show:
- Status: `COMPLETED`
- Assembled contigs and bins
- Taxonomic classifications
- Quality assessment reports
- Metagenome-assembled genomes (MAGs)

## Technical Notes
- ✅ **Test Data**: Official nf-core minigut metagenomics reads
- ⚠️ **Databases**: Multiple large databases required
- ⚠️ **Platform**: Work directory permissions need resolution
- ⚠️ **Resources**: May require larger than SMALL instance
- ✅ **Network**: HTTP/FTP access to test datasets and databases

## Success Criteria
- **Test Duration**: Expected >30 minutes (more complex than methylseq)
- **Resource Usage**: Potentially requires MEDIUM or LARGE node
- **Network**: >30GB download (databases + reads)
- **Output**: Complete metagenomics analysis with MAGs and taxonomic classification

This test validates the complete nf-core/mag pipeline functionality on Camber platform using official test metagenomics data.

