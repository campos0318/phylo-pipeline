#!/bin/bash

# strict mode: stop on errors, undefined variables, and pipeline failures
set -euo pipefail

# avoid errors if there are no FASTA files
shopt -s nullglob

# create output directories if they don't exist
mkdir -p data/raw data/processed data/aligned results/trees scripts logs

# loop through all FASTA files in the raw data folder
for INPUT in data/raw/*.fasta; do
	
	# extract base filename (remove path and .fasta extension)
	BASENAME=$(basename "$INPUT" .fasta)

	# define log file for this dataset
	LOGFILE="logs/${BASENAME}_pipeline.log"

	# send pipeline output to both the terminal and the log file
	(
		echo "========================================"
		echo "Processing: $INPUT"
		echo "Start: $(date)"
		echo "========================================"

		# print software versions
		echo "MAFFT Version:"
		mafft --version

		echo "IQ-TREE Version:"
		iqtree2 --version

		# run MAFFT multiple sequence alignment
		echo "Running MAFFT..."
		ALIGNMENT="data/aligned/${BASENAME}_aligned.fasta"
		mafft --auto "$INPUT" > "$ALIGNMENT"

		# run IQ-TREE with model selection and bootstrapping
		echo "Running IQ-TREE..."
		TREE_PREFIX="results/trees/${BASENAME}"
		iqtree2 -s "$ALIGNMENT" \
			-m MFP \
			-bb 1000 \
			-nt AUTO \
			-pre "$TREE_PREFIX" \
			-redo

		echo "Done: $BASENAME"
		echo "END: $(date)"
	) 2>&1 | tee -a "$LOGFILE"

done

echo "All files complete!"


