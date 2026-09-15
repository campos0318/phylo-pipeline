# Sequence Quality Control
# SARS-CoV-2 Genomic Surveillance Pipeline

import csv


# Input and output files
input_file = "data/raw/practice.fasta"
output_file = "data/processed/practice_qc.csv"


# QC thresholds
# These values are provisional and should be validated for SARS-CoV-2 surveillance.
MIN_SEQUENCE_LENGTH = 29000
MAX_AMBIGUOUS_BASES = 1000


# Read FASTA file
def read_fasta():
    """Read accession numbers and sequences from a FASTA file."""

    accession_numbers = []
    sequences = []
    current_sequence = ""

    with open(input_file, "r") as fasta_file:
        for line in fasta_file:

            # FASTA headers begin with ">"
            if line.startswith(">"):

                # Save previous sequence before starting a new one
                if current_sequence:
                    sequences.append(current_sequence)
                    current_sequence = ""

                # Extract accession number from header
                header_parts = line.split(" ")
                accession = header_parts[0]
                accession_numbers.append(accession[1:])

            else:
                current_sequence += line.strip()

        # Save final sequence
        if current_sequence:
            sequences.append(current_sequence)

    return accession_numbers, sequences


# Calculate sequence length
def calculate_length(sequences):
    """Calculate the length of each sequence."""

    sequence_lengths = []

    for sequence in sequences:
        length = len(sequence)
        sequence_lengths.append(length)

    return sequence_lengths


# Count ambiguous bases (N)
def count_ambiguous(sequences):
    """Count ambiguous N bases in each sequence."""

    ambiguous_counts = []

    for sequence in sequences:
        ambiguous_counts.append(sequence.count("N"))

    return ambiguous_counts


# Identify invalid characters
def find_invalid_chars(sequences):
    """Identify non-ACGTN characters in each sequence."""

    invalid_counts = []
    invalid_types = []

    for sequence in sequences:
        current_sequence_invalid = []

        for base in sequence:
            if base not in "ACGTN":
                current_sequence_invalid.append(base)

        invalid_counts.append(len(current_sequence_invalid))
        invalid_types.append(
            ", ".join(sorted(set(current_sequence_invalid))) or "None"
        )

    return invalid_counts, invalid_types


# Check for duplicate sequences
def check_duplicates(sequences):
    """Determine whether each sequence is duplicated."""

    duplicate_status = []

    for sequence in sequences:
        count = sequences.count(sequence)
        duplicate_status.append(count > 1)

    return duplicate_status


# Store the QC results
def store_qc_results(
    accession_numbers,
    sequence_lengths,
    ambiguous_counts,
    invalid_counts,
    invalid_types,
    duplicate_status
):
    """Combine QC metrics into a list of dictionaries."""

    qc_results = []

    for i in range(len(accession_numbers)):
        result = {
            "accession": accession_numbers[i],
            "length": sequence_lengths[i],
            "ambiguous_count": ambiguous_counts[i],
            "invalid_count": invalid_counts[i],
            "invalid_types": invalid_types[i],
            "duplicate": duplicate_status[i],
        }

        qc_results.append(result)

    return qc_results


# Determine QC status
def determine_qc_status(qc_results):
    """Determine whether each sequence passes QC and identify failure reasons."""
    for result in qc_results:
        qc_reasons = []

        if result["length"] < MIN_SEQUENCE_LENGTH:
            qc_reasons.append("Sequence too short")
        if result["ambiguous_count"] > MAX_AMBIGUOUS_BASES:
            qc_reasons.append("Sequence has too many ambiguous (N) bases")
        if result["invalid_count"] > 0:
            qc_reasons.append("Sequence has invalid characters")

        if qc_reasons:
            qc_status = "FAIL"
        else:
            qc_status = "PASS"

        result["qc_status"] = qc_status
        result["qc_reasons"] = qc_reasons


# Write results to a CSV file
def write_qc_results(qc_results):
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
        for result in qc_results:
            result_copy = result.copy()
            result_copy["qc_reasons"] = ", ".join(result_copy["qc_reasons"]) or "None"
            writer.writerow(result_copy)


# Print QC summary
def print_qc_summary(qc_results):
    """Print a summary of sequence QC results."""

    total_sequences = len(qc_results)
    passing_sequences = 0
    failing_sequences = 0

    for result in qc_results:
        if result["qc_status"] == "PASS":
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
accession_numbers, sequences = read_fasta()
sequence_lengths = calculate_length(sequences)
ambiguous_counts = count_ambiguous(sequences)
invalid_counts, invalid_types = find_invalid_chars(sequences)
duplicate_status = check_duplicates(sequences)

qc_results = store_qc_results(
    accession_numbers,
    sequence_lengths,
    ambiguous_counts,
    invalid_counts,
    invalid_types,
    duplicate_status
)

# Determine QC status
determine_qc_status(qc_results)

# Write QC results to CSV
write_qc_results(qc_results)

# Print QC summary
print_qc_summary(qc_results)
