# Phylogenetics Pipeline

Simple reproducible pipeline for multiple sequence alignment and phylogenetic tree building using MAFFT and IQ-TREE.

---

## Requirements

* MAFFT
* IQ-TREE

Install:

```bash
sudo apt update
sudo apt install mafft iqtree
```

---

## Run

Make scripts executable (first time only):

```bash
chmod +x scripts/run_pipeline.sh scripts/run_all.sh
```

Run on a single FASTA file:

```bash
./scripts/run_pipeline.sh data/raw/your_sequences.fasta
```

Run on all FASTA files:

```bash
./scripts/run_all.sh
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
