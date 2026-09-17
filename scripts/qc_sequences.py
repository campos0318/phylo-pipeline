# Sequence Quality Control
# SARS-CoV-2 Genomic Surveillance Pipeline

import csv
import os
import sys


# Input and output files
input_file = sys.argv[1]
basename = os.path.splitext(os.path.basename(input_file))[0]

output_file = f"data/processed/{basename}_qc.csv"
filtered_file = f"data/processed/{basename}_filtered.fasta"


# QC thresholds
# These values are provisional and should be validated for SARS-CoV-2 surveillance.
MIN_SEQUENCE_LENGTH = 29000
MAX_AMBIGUOUS_BASES = 1000


# Read FASTA file
def read_fasta():
    """Read accession numbers and sequences from a FASTA file."""

    sequence_records = []
    current_accession = ""
    current_sequence = ""

    with open(input_file, "r") as fasta_file:
        for line in fasta_file:

            # FASTA headers begin with ">"
            if line.startswith(">"):

                # Save previous sequence before starting a new one
                if current_sequence:
                    sequence_records.append({
                        "accession": current_accession,
                        "sequence": current_sequence
                    })
                    current_sequence = ""

                # Extract accession number from header
                header_parts = line.strip().split(" ")
                accession = header_parts[0]
                current_accession = accession[1:]

            else:
                current_sequence += line.strip()

        # Save final sequence
        if current_sequence:
            sequence_records.append({
                "accession": current_accession,
                "sequence": current_sequence
            })

    return sequence_records


# Calculate sequence length
def calculate_length(sequence_records):
    """Calculate the length of each sequence."""

    for record in sequence_records:
        record["length"] = len(record["sequence"])


# Count ambiguous bases (N)
def count_ambiguous(sequence_records):
    """Count ambiguous N bases in each sequence."""

    for record in sequence_records:
        record["ambiguous_count"] = record["sequence"].count("N")


# Identify invalid characters
def find_invalid_chars(sequence_records):
    """Identify non-ACGTN characters in each sequence."""

    for record in sequence_records:
        current_sequence_invalid = []

        for base in record["sequence"]:
            if base not in "ACGTN":
                current_sequence_invalid.append(base)

        record["invalid_count"] = len(current_sequence_invalid)
        record["invalid_types"] = (
            ", ".join(sorted(set(current_sequence_invalid))) or "None"
        )


# Check for duplicate sequences
def check_duplicates(sequence_records):
    """Determine whether each sequence is duplicated."""

    for record in sequence_records:
        count = 0

        for other_record in sequence_records:
            if record["sequence"] == other_record["sequence"]:
                count += 1

        record["duplicate"] = count > 1


# Determine QC status
def determine_qc_status(sequence_records):
    """Determine whether each sequence passes QC and identify failure reasons."""

    for record in sequence_records:
        qc_reasons = []

        if record["length"] < MIN_SEQUENCE_LENGTH:
            qc_reasons.append("Sequence too short")
        if record["ambiguous_count"] > MAX_AMBIGUOUS_BASES:
            qc_reasons.append("Sequence has too many ambiguous (N) bases")
        if record["invalid_count"] > 0:
            qc_reasons.append("Sequence has invalid characters")

        if qc_reasons:
            qc_status = "FAIL"
        else:
            qc_status = "PASS"

        record["qc_status"] = qc_status
        record["qc_reasons"] = qc_reasons


# Write sequences that pass QC to a FASTA file
def write_filtered_fasta(sequence_records):
    """Write sequences that pass QC to a FASTA file."""

    with open(filtered_file, "w") as fasta_file:
        for record in sequence_records:
            if record["qc_status"] == "PASS":
                fasta_file.write(f">{record['accession']}\n")
                fasta_file.write(f"{record['sequence']}\n")


# Write results to a CSV file
def write_qc_results(sequence_records):
    """Write QC results to a CSV file."""

    with open(output_file, "w", newline="") as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "accession",
                "length",
                "ambiguous_count",
                "invalid_count",
                "invalid_types",
                "duplicate",
                "qc_status",
                "qc_reasons"
            ]
        )

        writer.writeheader()

        # Convert QC reasons list to a string for CSV output
        for record in sequence_records:
            result_copy = record.copy()
            del result_copy["sequence"]
            result_copy["qc_reasons"] = ", ".join(result_copy["qc_reasons"]) or "None"
            writer.writerow(result_copy)


# Print QC summary
def print_qc_summary(sequence_records):
    """Print a summary of sequence QC results."""

    total_sequences = len(sequence_records)

    if total_sequences == 0:
        print("No sequences found.")
        return

    passing_sequences = 0
    failing_sequences = 0

    for record in sequence_records:
        if record["qc_status"] == "PASS":
            passing_sequences += 1
        else:
            failing_sequences += 1

    passing_percent = (passing_sequences / total_sequences) * 100
    failing_percent = (failing_sequences / total_sequences) * 100

    print("QC Summary")
    print("----------")
    print(f"Sequences analyzed: {total_sequences}")
    print(f"Sequences passing QC: {passing_sequences} ({passing_percent:.1f}%)")
    print(f"Sequences failing QC: {failing_sequences} ({failing_percent:.1f}%)")


# Run QC pipeline
sequence_records = read_fasta()
calculate_length(sequence_records)
count_ambiguous(sequence_records)
find_invalid_chars(sequence_records)
check_duplicates(sequence_records)

# Determine QC status
determine_qc_status(sequence_records)

# Write filtered FASTA
write_filtered_fasta(sequence_records)

# Write QC results to CSV
write_qc_results(sequence_records)

# Print QC summary
print_qc_summary(sequence_records)