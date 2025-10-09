#!/usr/bin/env nextflow
/*
========================================================================================
    Bacterial Genome Assembly from Oxford Nanopore Data
========================================================================================
    Github : https://github.com/CamberCloud-Inc/prod_apps

    Custom workflow for de novo bacterial genome assembly using Flye assembler
    from Oxford Nanopore long reads with quality control and polishing
----------------------------------------------------------------------------------------
*/

nextflow.enable.dsl = 2

/*
========================================================================================
    VALIDATE & PRINT PARAMETER SUMMARY
========================================================================================
*/

// Print help message
def helpMessage() {
    log.info"""
    ========================================================================
    Bacterial Genome Assembly from Oxford Nanopore Data v1.0
    ========================================================================

    Usage:
    nextflow run main.nf --input samplesheet.csv --outdir results/

    Required Arguments:
      --input              Path to comma-separated file containing information
                          about the samples (sample,fastq)
      --outdir             Output directory for results

    Assembly Options:
      --genome_size        Estimated genome size (default: 5m for bacteria)
      --flye_mode          Flye assembly mode: nano-raw, nano-corr, nano-hq (default: nano-hq)
      --min_read_length    Minimum read length for assembly (default: 1000)
      --min_read_quality   Minimum average read quality (default: 7)
      --polish_iterations  Number of Medaka polishing iterations (default: 1)

    Quality Control:
      --skip_qc            Skip FastQC and NanoPlot quality control
      --skip_filtering     Skip read quality filtering
      --skip_polishing     Skip Medaka polishing

    Resources:
      --max_cpus           Maximum number of CPUs (default: 16)
      --max_memory         Maximum memory (default: 60.GB)
      --max_time           Maximum time (default: 48.h)
    """
}

// Show help message
if (params.help) {
    helpMessage()
    exit 0
}

// Validate required parameters
if (!params.input) {
    log.error "ERROR: --input parameter is required"
    helpMessage()
    exit 1
}

if (!params.outdir) {
    log.error "ERROR: --outdir parameter is required"
    helpMessage()
    exit 1
}

/*
========================================================================================
    CONFIG FILES
========================================================================================
*/

// Set default parameters
params.input = null
params.outdir = './results'
params.genome_size = '5m'
params.flye_mode = 'nano-hq'
params.min_read_length = 1000
params.min_read_quality = 7
params.polish_iterations = 1
params.skip_qc = false
params.skip_filtering = false
params.skip_polishing = false
params.max_cpus = 16
params.max_memory = '60.GB'
params.max_time = '48.h'
params.help = false

/*
========================================================================================
    NAMED WORKFLOWS
========================================================================================
*/

// Import modules
include { NANOPLOT } from './modules/nanoplot'
include { FILTLONG } from './modules/filtlong'
include { FLYE } from './modules/flye'
include { MEDAKA } from './modules/medaka'
include { QUAST } from './modules/quast'
include { MULTIQC } from './modules/multiqc'

workflow {
    // Parse input samplesheet
    Channel
        .fromPath(params.input, checkIfExists: true)
        .splitCsv(header: true)
        .map { row ->
            def meta = [:]
            meta.id = row.sample
            [meta, file(row.fastq, checkIfExists: true)]
        }
        .set { ch_input }

    // QC raw reads with NanoPlot
    if (!params.skip_qc) {
        NANOPLOT(ch_input)
    }

    // Filter reads by length and quality
    if (!params.skip_filtering) {
        FILTLONG(ch_input)
        ch_filtered = FILTLONG.out.reads
    } else {
        ch_filtered = ch_input
    }

    // Assemble with Flye
    FLYE(ch_filtered)

    // Polish assembly with Medaka
    if (!params.skip_polishing) {
        MEDAKA(FLYE.out.assembly, ch_filtered)
        ch_assembly = MEDAKA.out.polished
    } else {
        ch_assembly = FLYE.out.assembly
    }

    // Assess assembly quality with QUAST
    QUAST(ch_assembly)

    // Generate MultiQC report
    MULTIQC(
        NANOPLOT.out.stats.collect().ifEmpty([]),
        FLYE.out.log.collect().ifEmpty([]),
        QUAST.out.results.collect().ifEmpty([])
    )
}

/*
========================================================================================
    COMPLETION
========================================================================================
*/

workflow.onComplete {
    log.info"""
    ========================================================================
    Pipeline completed at: ${workflow.complete}
    Execution status: ${workflow.success ? 'Success' : 'Failed'}
    Duration: ${workflow.duration}
    ========================================================================
    """.stripIndent()
}