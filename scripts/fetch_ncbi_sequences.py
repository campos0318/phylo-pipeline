import csv
import os
from datetime import datetime, timezone
from Bio import Entrez
from pathlib import Path


def main():
    # NCBI requires an email address for API requests.
    # Set this in your shell: export NCBI_EMAIL="your_email@example.com"
    Entrez.email = os.environ.get("NCBI_EMAIL")

    if not Entrez.email:
        raise ValueError("Please set the NCBI_EMAIL environment variable before running this script.")

    # Search NCBI for SARS-CoV-2 complete genomes.
    search_term = '("Severe acute respiratory syndrome coronavirus 2"[Organism]) AND complete genome[title]'

    # Use esearch to find accession IDs that match the query.
    handle = Entrez.esearch(
        db="nucleotide",
        term=search_term,
        retmax=50,
        idtype="acc"
    )

    # Parse the NCBI response into a Python dictionary.
    record = Entrez.read(handle)
    handle.close()

    # Extract the list of accession numbers.
    ids = record["IdList"]

    # Create the raw data folder if it does not already exist.
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Download all genomes into one multi-sequence FASTA dataset.
    fasta_handle = Entrez.efetch(
        db="nucleotide",
        id=",".join(ids),
        rettype="fasta",
        retmode="text"
    )
    fasta = fasta_handle.read()
    fasta_handle.close()

    file_path = output_dir / "ncbi_sars_cov_2.fasta"
    with open(file_path, "w") as file:
        file.write(fasta)

    # Save the exact accessions and retrieval time for reproducibility.
    metadata_dir = Path("data/metadata")
    metadata_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = metadata_dir / "ncbi_sars_cov_2_accessions.csv"
    with open(manifest_path, "w", newline="") as manifest_file:
        writer = csv.writer(manifest_file)
        writer.writerow(["accession", "retrieved_at_utc", "search_term"])
        retrieved_at = datetime.now(timezone.utc).isoformat()
        for accession_id in ids:
            writer.writerow([accession_id, retrieved_at, search_term])

    print(f"Saved {file_path} with {len(ids)} genomes")
    print(f"Saved accession manifest to {manifest_path}")


if __name__ == "__main__":
    main()