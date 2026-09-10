# SARS-CoV-2 Genomic Surveillance Pipeline

A reproducible bioinformatics pipeline for multiple sequence alignment and phylogenetic analysis of SARS-CoV-2 genomes using MAFFT and IQ-TREE.

The pipeline is designed to support genomic surveillance workflows by processing multiple FASTA datasets, generating sequence alignments, building maximum-likelihood phylogenetic trees, and recording pipeline output in per-dataset log files.

---

## Requirements

* MAFFT
* IQ-TREE

Install on Ubuntu/WSL:

```bash
sudo apt update
sudo apt install mafft iqtree
```

Software versions used for development are documented in `software_versions.txt`.

---

## Project Structure

```text
phylo_pipeline/
├── data/
│   ├── raw/          # Input FASTA files
│   └── aligned/      # MAFFT alignments
├── results/
│   └── trees/        # IQ-TREE outputs
├── scripts/          # Supporting scripts
├── logs/             # Pipeline logs
├── run_pipeline.sh   # Main pipeline
└── software_versions.txt
```

---

## Run the Pipeline

Make the pipeline executable:

```bash
chmod +x run_pipeline.sh
```

Place one or more FASTA files in:

```text
data/raw/
```

Then run:

```bash
./run_pipeline.sh
```

The pipeline automatically processes every `.fasta` file in `data/raw/`.

For each dataset, the pipeline:

1. Performs multiple sequence alignment with MAFFT.
2. Uses IQ-TREE ModelFinder to select an appropriate substitution model.
3. Builds a maximum-likelihood phylogenetic tree.
4. Performs 1,000 ultrafast bootstrap replicates.
5. Saves pipeline output to a dataset-specific log file.

---

## Output

For each input FASTA file:

* **Alignments** → `data/aligned/`
* **Phylogenetic trees and IQ-TREE results** → `results/trees/`
* **Pipeline logs** → `logs/`

For example, an input file named `<dataset>.fasta` produces:

```text
data/raw/<dataset>.fasta
        ↓
data/aligned/<dataset>_aligned.fasta
        ↓
results/trees/<dataset>.*
        +
logs/<dataset>_pipeline.log
```

The same workflow applies to any FASTA dataset placed in `data/raw/`.

---

## Reproducibility

The pipeline records the versions of the primary bioinformatics tools used during development.

Current versions:

* MAFFT 7.505
* IQ-TREE 2.0.7

See `software_versions.txt` for the recorded software environment.

---

## Analysis Settings

* MAFFT alignment strategy: `--auto`
* IQ-TREE model selection: `-m MFP`
* Bootstrap replicates: 1,000 ultrafast bootstraps (`-bb 1000`)
* IQ-TREE threads: automatically determined (`-nt AUTO`)

---

## Future Development

Planned extensions include:

* Sequence and metadata quality control
* Automated metadata extraction
* Geographic and temporal filtering
* Integration of public SARS-CoV-2 genomic datasets
* Phylogenetic visualization and interpretation
* Expansion toward a genomic surveillance workflow
* Workflow automation with Nextflow

---

