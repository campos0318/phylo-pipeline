# SARS-CoV-2 Genomic Surveillance Pipeline

A reproducible bioinformatics pipeline for sequence quality control, multiple sequence alignment, and phylogenetic analysis of SARS-CoV-2 genomes.

The pipeline accepts one or more FASTA datasets, performs sequence-level quality control and filtering, generates multiple sequence alignments with MAFFT, constructs maximum-likelihood phylogenetic trees with IQ-TREE, and records dataset-specific pipeline logs.

This project was developed as a portfolio project to demonstrate practical skills in bioinformatics scripting, reproducible analysis, sequence quality control, phylogenetics, and command-line workflow automation.

---

## Workflow

The pipeline follows this workflow:

```text
FASTA input
    ↓
Sequence quality control
    ↓
QC filtering
    ↓
MAFFT multiple sequence alignment
    ↓
IQ-TREE ModelFinder
    ↓
Maximum-likelihood phylogenetic analysis
    ↓
Ultrafast bootstrap support
```

Each FASTA file placed in `data/raw/` is processed independently.

---

## Requirements

* Python 3
* Bash
* MAFFT
* IQ-TREE

The pipeline was developed and tested in Ubuntu/WSL.

### Software Versions

Versions used during development:

* MAFFT 7.505
* IQ-TREE 2.0.7

The recorded software environment is documented in `software_versions.txt`.

---

## Sequence Quality Control

Sequence quality control is performed by `scripts/qc_sequences.py` before sequences are aligned.

The QC process evaluates:

* Sequence length
* Ambiguous `N` bases
* Invalid nucleotide characters
* Duplicate sequences

Each sequence receives a `PASS` or `FAIL` status. Failure reasons are recorded for sequences that do not meet the current QC criteria.

### Current QC Criteria

| Metric                  | Criterion                                                   |
| ----------------------- | ----------------------------------------------------------- |
| Minimum sequence length | 29,000 bp                                                   |
| Maximum ambiguous bases | 1,000 `N` bases                                             |
| Invalid characters      | Any non-`A`, `C`, `G`, `T`, or `N` character causes failure |
| Duplicate sequences     | Flagged for review but do not currently cause failure       |

The current thresholds are provisional and have not been validated for routine operational SARS-CoV-2 genomic surveillance.

### QC Output

QC results are written to:

```text
data/processed/<dataset>_qc.csv
```

Sequences that pass QC are written to:

```text
data/processed/<dataset>_filtered.fasta
```

Only sequences passing QC are subsequently aligned with MAFFT.

---

## Project Structure

```text
phylo_pipeline/
├── data/
│   ├── raw/                    # Input FASTA files
│   ├── processed/              # QC results and filtered sequences
│   └── aligned/                # MAFFT alignments
├── results/
│   └── trees/                  # IQ-TREE phylogenetic results
├── scripts/
│   └── qc_sequences.py         # Sequence quality control
├── logs/                       # Dataset-specific pipeline logs
├── run_pipeline.sh             # Main pipeline workflow
├── software_versions.txt       # Software versions used
├── .gitignore
└── README.md
```

Generated data, alignments, phylogenetic results, and logs are excluded from version control.

---

## Running the Pipeline

### 1. Place FASTA files in the input directory

```text
data/raw/
```

The pipeline accepts multiple `.fasta` files and processes each dataset independently.

### 2. Run the pipeline

```bash
./run_pipeline.sh
```

If necessary, make the script executable:

```bash
chmod +x run_pipeline.sh
```

### 3. Pipeline steps

For each FASTA dataset, the pipeline:

1. Performs sequence quality control.
2. Writes QC results to a CSV file.
3. Writes sequences passing QC to a filtered FASTA file.
4. Aligns filtered sequences using MAFFT with `--auto`.
5. Uses IQ-TREE ModelFinder to select a substitution model.
6. Constructs a maximum-likelihood phylogenetic tree.
7. Performs 1,000 ultrafast bootstrap replicates.
8. Records pipeline output in a dataset-specific log file.

If no sequences pass QC, the dataset is skipped and the pipeline continues to the next input dataset.

---

## Analysis Settings

### MAFFT

Multiple sequence alignment is performed using:

```bash
mafft --auto
```

MAFFT automatically selects an appropriate alignment strategy based on the input dataset.

### IQ-TREE

Phylogenetic analysis uses:

```bash
-m MFP
```

to allow IQ-TREE ModelFinder to evaluate nucleotide substitution models and select a best-fit model.

The pipeline uses:

```bash
-bb 1000
```

to generate 1,000 ultrafast bootstrap replicates.

Threads are automatically determined using:

```bash
-nt AUTO
```

---

## Example Run

The pipeline was tested using a practice dataset containing 50 SARS-CoV-2 genome sequences.

### Quality Control

```text
Sequences analyzed: 50
Sequences passing QC: 50 (100.0%)
Sequences failing QC: 0 (0.0%)
```

### Multiple Sequence Alignment

MAFFT produced an alignment containing:

```text
50 sequences
29,918 alignment columns
```

### Phylogenetic Analysis

IQ-TREE ModelFinder selected:

```text
GTR+F+I
```

as the best-fit model according to BIC for this practice dataset.

The analysis generated 1,000 ultrafast bootstrap replicates and produced a maximum-likelihood phylogenetic tree along with associated IQ-TREE output files.

These results demonstrate successful execution of the complete workflow from FASTA input through phylogenetic analysis.

---

## Reproducibility

The pipeline is designed to make analyses repeatable across datasets.

Reproducibility features include:

* Automated processing of multiple FASTA datasets
* Explicit QC criteria
* Consistent alignment and phylogenetic analysis settings
* Recorded software versions
* Dataset-specific log files
* Automated creation of required output directories
* Separation of raw input, processed data, alignments, results, and logs

The pipeline can be rerun on additional FASTA datasets using the same documented workflow and analysis settings.

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

---

## Future Development

Potential extensions include:

* Additional sequence QC metrics and threshold validation
* Integration of sample metadata
* Geographic and temporal filtering
* Integration of publicly available SARS-CoV-2 genomic datasets
* Phylogenetic visualization and reporting
* Additional automated testing
* Workflow implementation using Nextflow
* Expansion toward a more complete genomic surveillance workflow
