#!/bin/bash
# Auto-generated deployment script
# Run this to deploy all modified apps

set -e

echo 'Deploying hicar-enhancer-promoter-analysis...'
camber app delete hicar-enhancer-promoter-analysis || true
camber app create --file /Users/david/git/prod_apps/nextflow/hicar/enhancer-promoter-loops/app.json
echo 'Done: hicar-enhancer-promoter-analysis'

echo 'Deploying longraredisease-diagnostic-wgs...'
camber app delete longraredisease-diagnostic-wgs || true
camber app create --file /Users/david/git/prod_apps/nextflow/longraredisease/diagnostic-wgs/app.json
echo 'Done: longraredisease-diagnostic-wgs'

echo 'Deploying scflow-cell-type-annotation...'
camber app delete scflow-cell-type-annotation || true
camber app create --file /Users/david/git/prod_apps/nextflow/scflow/cell-type-annotation/app.json
echo 'Done: scflow-cell-type-annotation'

echo 'Deploying ddamsproteomics-tmt-labeling...'
camber app delete ddamsproteomics-tmt-labeling || true
camber app create --file /Users/david/git/prod_apps/nextflow/ddamsproteomics/tmt-labeling/app.json
echo 'Done: ddamsproteomics-tmt-labeling'

echo 'Deploying imcyto-imaging-mass-cytometry...'
camber app delete imcyto-imaging-mass-cytometry || true
camber app create --file /Users/david/git/prod_apps/nextflow/imcyto/imaging-mass-cytometry/app.json
echo 'Done: imcyto-imaging-mass-cytometry'

echo 'Deploying cellpainting-phenotypic-profiling...'
camber app delete cellpainting-phenotypic-profiling || true
camber app create --file /Users/david/git/prod_apps/nextflow/cellpainting/phenotypic-profiling/app.json
echo 'Done: cellpainting-phenotypic-profiling'

echo 'Deploying molkart-spatial-multiomics...'
camber app delete molkart-spatial-multiomics || true
camber app create --file /Users/david/git/prod_apps/nextflow/molkart/spatial-multiomics/app.json
echo 'Done: molkart-spatial-multiomics'

echo 'Deploying pathogensurveillance-clinical-surveillance...'
camber app delete pathogensurveillance-clinical-surveillance || true
camber app create --file /Users/david/git/prod_apps/nextflow/pathogensurveillance/clinical-surveillance/app.json
echo 'Done: pathogensurveillance-clinical-surveillance'

echo 'Deploying alleleexpression-ase-analysis...'
camber app delete alleleexpression-ase-analysis || true
camber app create --file /Users/david/git/prod_apps/nextflow/alleleexpression/ase-analysis/app.json
echo 'Done: alleleexpression-ase-analysis'

echo 'Deploying tumourevo-tumor-phylogeny...'
camber app delete tumourevo-tumor-phylogeny || true
camber app create --file /Users/david/git/prod_apps/nextflow/tumourevo/tumor-phylogeny/app.json
echo 'Done: tumourevo-tumor-phylogeny'

echo 'Deploying lncpipe-lncrna-discovery...'
camber app delete lncpipe-lncrna-discovery || true
camber app create --file /Users/david/git/prod_apps/nextflow/lncpipe/lncrna-discovery/app.json
echo 'Done: lncpipe-lncrna-discovery'

echo 'Deploying callingcards-tf-binding...'
camber app delete callingcards-tf-binding || true
camber app create --file /Users/david/git/prod_apps/nextflow/callingcards/tf-binding/app.json
echo 'Done: callingcards-tf-binding'

echo 'Deploying drugresponseeval-drug-screening...'
camber app delete drugresponseeval-drug-screening || true
camber app create --file /Users/david/git/prod_apps/nextflow/drugresponseeval/drug-screening/app.json
echo 'Done: drugresponseeval-drug-screening'

echo 'Deploying evexplorer-molecular-evolution...'
camber app delete evexplorer-molecular-evolution || true
camber app create --file /Users/david/git/prod_apps/nextflow/evexplorer/molecular-evolution/app.json
echo 'Done: evexplorer-molecular-evolution'

echo 'Deploying viralintegration-hpv-integration...'
camber app delete viralintegration-hpv-integration || true
camber app create --file /Users/david/git/prod_apps/nextflow/viralintegration/hpv-integration/app.json
echo 'Done: viralintegration-hpv-integration'

echo 'Deploying denovotranscript-de-novo-transcriptome...'
camber app delete denovotranscript-de-novo-transcriptome || true
camber app create --file /Users/david/git/prod_apps/nextflow/denovotranscript/de-novo-transcriptome/app.json
echo 'Done: denovotranscript-de-novo-transcriptome'

echo 'Deploying denovohybrid-hybrid-assembly...'
camber app delete denovohybrid-hybrid-assembly || true
camber app create --file /Users/david/git/prod_apps/nextflow/denovohybrid/hybrid-assembly/app.json
echo 'Done: denovohybrid-hybrid-assembly'

echo 'Deploying ssds-single-strand-dna...'
camber app delete ssds-single-strand-dna || true
camber app create --file /Users/david/git/prod_apps/nextflow/ssds/single-strand-dna/app.json
echo 'Done: ssds-single-strand-dna'

echo 'Deploying tbprofiler-tb-genomics...'
camber app delete tbprofiler-tb-genomics || true
camber app create --file /Users/david/git/prod_apps/nextflow/tbanalyzer/tb-genomics/app.json
echo 'Done: tbprofiler-tb-genomics'

echo 'Deploying seqinspector-sequencing-qc...'
camber app delete seqinspector-sequencing-qc || true
camber app create --file /Users/david/git/prod_apps/nextflow/seqinspector/sequencing-qc/app.json
echo 'Done: seqinspector-sequencing-qc'

echo 'Deploying coproid-ancient-dna...'
camber app delete coproid-ancient-dna || true
camber app create --file /Users/david/git/prod_apps/nextflow/coproid/ancient-dna/app.json
echo 'Done: coproid-ancient-dna'

echo 'Deploying mitodetect-mitochondrial-variants...'
camber app delete mitodetect-mitochondrial-variants || true
camber app create --file /Users/david/git/prod_apps/nextflow/mitodetect/mitochondrial-variants/app.json
echo 'Done: mitodetect-mitochondrial-variants'

echo 'Deploying proteinfamilies-protein-families...'
camber app delete proteinfamilies-protein-families || true
camber app create --file /Users/david/git/prod_apps/nextflow/proteinfamilies/protein-families/app.json
echo 'Done: proteinfamilies-protein-families'

echo 'Deploying genomeannotator-eukaryote-annotation...'
camber app delete genomeannotator-eukaryote-annotation || true
camber app create --file /Users/david/git/prod_apps/nextflow/genomeannotator/eukaryote-annotation/app.json
echo 'Done: genomeannotator-eukaryote-annotation'

echo 'Deploying genomeassembler-long-read-assembly...'
camber app delete genomeassembler-long-read-assembly || true
camber app create --file /Users/david/git/prod_apps/nextflow/genomeassembler/short-read-assembly/app.json
echo 'Done: genomeassembler-long-read-assembly'

echo 'Deploying genomeqc-genome-qc...'
camber app delete genomeqc-genome-qc || true
camber app create --file /Users/david/git/prod_apps/nextflow/genomeqc/genome-qc/app.json
echo 'Done: genomeqc-genome-qc'

echo 'Deploying bamtofastq-bam-conversion...'
camber app delete bamtofastq-bam-conversion || true
camber app create --file /Users/david/git/prod_apps/nextflow/bamtofastq/bam-conversion/app.json
echo 'Done: bamtofastq-bam-conversion'

echo 'Deploying createtaxdb-taxonomy-db...'
camber app delete createtaxdb-taxonomy-db || true
camber app create --file /Users/david/git/prod_apps/nextflow/createtaxdb/taxonomy-db/app.json
echo 'Done: createtaxdb-taxonomy-db'

echo 'Deploying stableexpression-housekeeping-genes...'
camber app delete stableexpression-housekeeping-genes || true
camber app create --file /Users/david/git/prod_apps/nextflow/stableexpression/housekeeping-genes/app.json
echo 'Done: stableexpression-housekeeping-genes'

echo 'Deploying mhcquant-immunopeptidomics...'
camber app delete mhcquant-immunopeptidomics || true
camber app create --file /Users/david/git/prod_apps/nextflow/mhcquant/immunopeptidomics/app.json
echo 'Done: mhcquant-immunopeptidomics'

echo 'Deploying methylong-long-read-methylation...'
camber app delete methylong-long-read-methylation || true
camber app create --file /Users/david/git/prod_apps/nextflow/methylong/long-read-methylation/app.json
echo 'Done: methylong-long-read-methylation'

echo 'Deploying neutronstar-10x-assembly...'
camber app delete neutronstar-10x-assembly || true
camber app create --file /Users/david/git/prod_apps/nextflow/neutronstar/neutron-star-analysis/app.json
echo 'Done: neutronstar-10x-assembly'

echo 'Deploying rangeland-remote-sensing...'
camber app delete rangeland-remote-sensing || true
camber app create --file /Users/david/git/prod_apps/nextflow/rangeland/remote-sensing/app.json
echo 'Done: rangeland-remote-sensing'

