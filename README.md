# Phylogenetics Pipeline

Simple pipeline for building phylogenetic trees using MAFFT and IQ-TREE.

---

## Requirements

* MAFFT
* IQ-TREE

Install on Ubuntu:

```bash
sudo apt update
sudo apt install mafft iqtree
```

---

## Usage

Run on a single FASTA file:

```bash
bash scripts/run_pipeline.sh data/raw/your_sequences.fasta
```

Run on all FASTA files:

```bash
bash scripts/run_all.sh
```

---

## Output

* Alignment → `data/aligned/`
* Trees → `results/trees/`
* Logs → `logs/`

---

## Notes

* Uses automatic model selection (`-m MFP`)
* Runs 1000 bootstrap replicates

---
