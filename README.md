# Genomic Surveillance Pipeline for SARS-CoV-2

This project is a beginner-friendly SARS-CoV-2 genomic surveillance workflow built for a public health genomics portfolio. It takes FASTA sequence data, removes low-quality genomes, aligns the remaining sequences, and infers a phylogenetic tree using MAFFT and IQ-TREE.

## Why this project matters

- Demonstrates core bioinformatics workflows used in outbreak surveillance.
- Applies sequence QC, alignment, and phylogenetic inference to SARS-CoV-2 data.
- Shows how raw genomic data can be turned into an interpretable public health product.

## Workflow overview

```text
FASTA input
  ↓
QC filtering and sequence validation
  ↓
Filtered sequences exported to FASTA
  ↓
Multiple sequence alignment with MAFFT
  ↓
Model selection and tree inference with IQ-TREE
  ↓
Results saved to processed, aligned, and tree output folders
```

Each FASTA file in `data/raw/` is processed independently, and logs are written for each dataset.

## Tools used

- Python 3 for sequence parsing and QC logic
- Bash for workflow automation
- MAFFT for alignment
- IQ-TREE for model selection and maximum-likelihood phylogeny
- CSV and FASTA outputs for traceable results

### Versions used

- MAFFT 7.505
- IQ-TREE 2.0.7

Software versions are recorded in `software_versions.txt`.

---

## Repository structure

```text
phylo_pipeline/
├── data/
│   ├── raw/                    # Input FASTA sequence files
│   ├── processed/             # QC CSVs and filtered FASTA outputs
│   ├── aligned/               # MAFFT alignment files
│   └── metadata/              # Tracked templates and NCBI accession manifests
├── logs/                      # Dataset-specific execution logs
├── results/
│   └── trees/                 # IQ-TREE output and phylogenetic files
├── scripts/
│   ├── fetch_ncbi_sequences.py # NCBI data acquisition script
│   └── qc_sequences.py         # Quality control script
├── run_pipeline.sh            # Main pipeline workflow
├── software_versions.txt      # Software environment record
├── README.md
└── .gitignore
```

---

## Quick start

### Option 1: use local FASTA files

1. Add one or more FASTA files to `data/raw/`.
2. Run the workflow from the project root:

```bash
./run_pipeline.sh
```

If needed, make the script executable:

```bash
chmod +x run_pipeline.sh
```

### Option 2: download SARS-CoV-2 genomes from NCBI GenBank

This project also includes a beginner-friendly script that fetches SARS-CoV-2 genome records directly from NCBI and saves them into `data/raw/`.

```bash
export NCBI_EMAIL="your_email@example.com"
conda activate phylo_pipeline
python scripts/fetch_ncbi_sequences.py
```

The script downloads up to 50 complete SARS-CoV-2 genome records and saves them together in `data/raw/ncbi_sars_cov_2.fasta`. It also records the accession IDs and retrieval timestamp in `data/metadata/ncbi_sars_cov_2_accessions.csv`.

After the file is present, run:

```bash
./run_pipeline.sh
```

---

## Example dataset results

The local practice dataset contains 50 SARS-CoV-2 genome sequences. FASTA files and generated outputs are not committed to the repository; the summaries below document a representative local run.

### QC summary

```text
Sequences analyzed: 50
Sequences passing QC: 50 (100.0%)
Sequences failing QC: 0 (0.0%)
```

### Alignment summary

```text
50 sequences
29,918 alignment columns
```

### Phylogenetic summary

```text
Best-fit model selected by IQ-TREE: GTR+F+I
Ultrafast bootstrap replicates: 1000
```

These outputs show a successful end-to-end workflow from raw FASTA sequence input to phylogenetic inference.

---

## Sequence QC logic

The QC script evaluates sequence quality before alignment.

Current checks include:

- minimum sequence length threshold
- maximum allowed ambiguous bases (`N`)
- invalid nucleotide characters
- duplicate sequence detection

Each sequence is assigned a `PASS` or `FAIL` status, and failing sequences are excluded from the alignment step.

### Example QC thresholds

| Metric | Threshold |
| --- | --- |
| Minimum sequence length | 29,000 bp |
| Maximum ambiguous bases | 1,000 `N` bases |
| Invalid characters | Any non-`A`, `C`, `G`, `T`, or `N` character fails |
| Duplicate sequences | Flagged for review |

These thresholds are simple and reproducible, but should be validated against a real-world surveillance dataset before operational use.

---

## Why this matters for public health genomics

This project follows the same general logic used in pathogen surveillance workflows:

- screen raw sequence data for poor-quality genomes
- remove problematic records before downstream analysis
- align genomes to compare relationships among samples
- generate a phylogenetic tree to summarize possible transmission patterns

---

## Skills demonstrated

- Bioinformatics workflow development
- FASTA parsing and sequence QC
- Command-line automation
- Reproducible analysis practices
- Phylogenetic inference and tree generation
- Data organization for public health applications

---

## Future improvements

Potential next steps include:

- adding collection date, location, and sample metadata
- validating QC thresholds against a real surveillance dataset
- integrating lineage assignment or reference-based analysis
- generating publication-style tree visualizations
- adding geographic and temporal filtering
- improving workflow robustness with automated testing
- moving the project to a workflow manager such as Nextflow

---

## Limitations

This project is intended as a reproducible portfolio and learning project rather than a validated operational genomic surveillance system.

Current limitations include:

* QC thresholds are provisional and have not been validated for routine SARS-CoV-2 surveillance.
* Duplicate sequences are flagged but do not currently cause a sequence to fail QC.
* The pipeline currently accepts FASTA sequence data but does not yet integrate sample metadata.
* Geographic and temporal filtering have not yet been implemented.
* Phylogenetic tree generation is implemented, but downstream phylogenetic interpretation is outside the current scope.
* The current workflow is implemented primarily with Bash and Python and has not yet been converted to a workflow management system such as Nextflow.
