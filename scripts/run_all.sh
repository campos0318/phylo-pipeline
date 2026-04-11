#!/bin/bash

# fail fast
set -euo pipefail

# avoid matching failures like *.fasta when no files exist
shopt -s nullglob

# loop through all FASTA files in the raw data folder
for FILE in data/raw/*.fasta; do
	echo "Processing: $FILE"		#print current file being processed
	bash scripts/run_pipeline.sh "$FILE"	#run main pipeline on each file
done

# print message when finished
echo "All files complete!"
