# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a variant calling workflow application built for the Camber Cloud platform using the nf-core/sarek pipeline. It performs genomic variant detection from whole genome or targeted sequencing data.

## Key Architecture Components

- **app.json**: Main application configuration defining:
  - Pipeline command: `nextflow run nf-core/sarek --input ${input} --outdir ${output} --tools ${tools} -r ${revision}`
  - Job configuration with system size presets
  - Input/output specifications for Stash File integration
  - Tool selection (ASCAT, CNVkit, DeepVariant, freebayes, GATK HaplotypeCaller, Manta, etc.)

- **variant_calling.ipynb**: Tutorial notebook demonstrating:
  - Camber package usage for pipeline execution
  - Job configuration with engine sizing and parallel processing
  - Real-time log monitoring
  - Results visualization and download

- **samplesheet.csv**: Sample input specification following nf-core/sarek format:
  - Format: `patient,sample,lane,fastq_1,fastq_2`
  - Points to S3 storage locations for FASTQ files

## Workflow Execution

The application uses the Camber Cloud platform for execution:

```python
nf_sarek_job = camber.nextflow.create_job(
    pipeline="nf-core/sarek",
    engine_size="MICRO",
    num_engines=4,
    params={
        "--input": "./samplesheet.csv",
        "--outdir": "/camber_outputs",
        "-r": "3.5.1",
        "--tools": "freebayes",
    },
)
```

## Common Development Tasks

- **Run the workflow**: Execute cells in `variant_calling.ipynb`
- **Monitor job status**: Use `nf_sarek_job.status`
- **View logs**: Use `nf_sarek_job.read_logs()`
- **Access results**: Check `jobs/{JOB_ID}` directory in notebook or Stash UI

## File Structure Context

This is one of several Nextflow workflow applications in the parent directory:
- `mag9/`: Metagenomics assembly workflow
- `methylseq/`: DNA methylation analysis workflow  
- `rnaseq/`: RNA sequencing analysis workflow
- `variant-calling/`: Current genomic variant calling workflow

Each application follows the same pattern with app.json configuration, Jupyter notebook tutorial, and sample data files.