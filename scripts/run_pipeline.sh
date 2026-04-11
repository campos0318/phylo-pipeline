#!/bin/bash

# strict mode: stop on errors, undefined variables, and pipeline failures
set -euo pipefail

# get input FASTA file from first argument
INPUT=$1

# check that input file exists
if [ ! -f "$INPUT" ]; then
	echo "Error: input file not found: $INPUT"
	exit 1
fi

# create output directories if they don't exist
mkdir -p data/aligned results/trees logs

# extract base filename (remove path and .fasta extension)
BASENAME=$(basename "$INPUT" .fasta)

# define log file for this run
LOGFILE="logs/${BASENAME}.log"

# send all terminal output to both screen and log file
exec > >(tee -a "$LOGFILE") 2>&1

#print start timestamp
echo "Start: $(date)"

#print status update
echo "Running MAFFT..."

# run MAFFT multiple sequence alignment
mafft "$INPUT" > data/aligned/${BASENAME}_aligned.fasta

#print status update
echo "Running IQ-TREE..."

# run IQ-TREE with model selection and bootstrapping
iqtree2 -s data/aligned/${BASENAME}_aligned.fasta \
	-m MFP \
	-bb 1000 \
	-nt AUTO \
	-pre results/trees/${BASENAME}

# print end timestamp
echo "End: $(date)"

# print status update
echo "Done!"
