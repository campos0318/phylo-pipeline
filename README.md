# Genomic Surveillance Pipeline for SARS-CoV-2

Genomic surveillance is a key public health tool for monitoring pathogen transmission, identifying low-quality sequence data, and inferring relationships among circulating variants. This project builds a simplified SARS-CoV-2 surveillance workflow that mirrors the early stages of outbreak genomics analysis.

The pipeline accepts FASTA sequence files, filters low-quality genomes, aligns sequences with MAFFT, and infers evolutionary relationships using IQ-TREE. It is designed as a beginner-friendly portfolio project to demonstrate practical skills in Python scripting, command-line automation, sequence quality control, and public health genomics.

---

## Project goal

This project demonstrates a streamlined genomic surveillance workflow used to support pathogen monitoring and outbreak investigation. In a public health context, sequence data are screened for quality before being used to assess diversity, detect problematic samples, and infer transmission relationships.

The workflow emphasizes:

- sequence quality control before downstream analysis
- reproducible processing of multiple input datasets
- alignment of high-quality genomes for phylogenetic inference
- generation of interpretable outputs suitable for surveillance reporting

---

## Workflow

```text
FASTA input
  ↓
QC filtering and sequence validation
  ↓
Filtered sequences exported to FASTA
  ↓
Multiple sequence alignment with MAFFT
  ↓
Model selection with IQ-TREE
  ↓
Maximum-likelihood phylogeny and bootstrap support
  ↓
Results saved to processed and tree output folders
```

Each FASTA file in `data/raw/` is processed independently, with logs written for that dataset.

---

## Tools and methods

- Python 3 for sequence parsing and QC logic
- Bash for pipeline orchestration
- MAFFT for multiple sequence alignment
- IQ-TREE for phylogenetic tree construction and model selection
- CSV and FASTA outputs for reproducible results

### Versions used

- MAFFT 7.505
- IQ-TREE 2.0.7

Software versions are recorded in `software_versions.txt`.

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

## How to run the pipeline

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

The pipeline will automatically:

- check each dataset for quality issues
- export passing sequences to a filtered FASTA file
- align sequences with MAFFT
- run IQ-TREE model selection and tree inference
- save results in `data/processed/`, `data/aligned/`, and `results/trees/`

### Option 2: download SARS-CoV-2 genomes from NCBI GenBank

This project also includes a beginner-friendly script that fetches SARS-CoV-2 genome records directly from NCBI and saves them into `data/raw/`. FASTA files and generated analysis outputs are ignored by Git, while the metadata template and accession manifest provide a reproducible record of the inputs.

First, set your email for the NCBI API:

```bash
export NCBI_EMAIL="your_email@example.com"
```

If you are using a Conda environment, activate it first:

```bash
conda activate phylo_pipeline
```

Then run:

```bash
python scripts/fetch_ncbi_sequences.py
```

The script searches NCBI for SARS-CoV-2 complete genomes, downloads up to 50 FASTA records, and saves them together in `data/raw/ncbi_sars_cov_2.fasta`. It also records the exact accession IDs and retrieval time in `data/metadata/ncbi_sars_cov_2_accessions.csv`. Keeping the genomes in one multi-sequence FASTA file allows the pipeline to align them and infer one phylogenetic tree. Once the file is present, you can run the same pipeline script as above.

This option demonstrates a simple automated data acquisition step that is common in real-world genomic surveillance workflows.

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

## Why this is relevant to public health genomics

This project mirrors key steps used in pathogen surveillance:

- screening raw sequence data for low-quality genomes
- reducing noisy data before comparative analysis
- aligning genomes to compare relationships among isolates
- generating phylogenetic trees as a visual summary of sample relatedness

This is a useful foundation for understanding how genomic tools can support outbreak response, sequence surveillance, and pathogen monitoring.

---

## Skills demonstrated

This project highlights practical experience in:

- bioinformatics workflow development
- FASTA parsing and quality control
- command-line data analysis
- reproducible research practices
- phylogenetic analysis and tree inference
- data organization and reporting for public health applications

---

## Future improvements

This project is intentionally beginner-friendly, but it can be expanded into a more operational genomic surveillance workflow. Potential next steps include:

- adding metadata such as collection date, location, and patient ID
- validating QC thresholds against a real surveillance dataset
- integrating lineage assignment tools or public genomic reference data
- summarizing QC results in a human-readable report
- generating tree visualizations for presentations and outbreak summaries
- adding geographic and temporal filtering for surveillance-style analyses
- implementing additional automated testing and workflow robustness checks
- exploring a workflow management system such as Nextflow for larger-scale deployment

---

## Resume-ready project summary

Developed a reproducible SARS-CoV-2 genomic surveillance pipeline that applies sequence quality control, performs multiple sequence alignment, and infers phylogenetic relationships using MAFFT and IQ-TREE. The project automates processing from raw FASTA input through QC filtering, alignment, and tree generation to support outbreak-focused genomic analysis and public health surveillance workflows.

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
