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