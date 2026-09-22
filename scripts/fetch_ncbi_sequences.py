import os
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

    print(f"Saved {file_path} with {len(ids)} genomes")


if __name__ == "__main__":
    main()