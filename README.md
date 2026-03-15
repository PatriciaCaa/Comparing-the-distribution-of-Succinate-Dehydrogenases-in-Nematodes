# Comparing-the-distribution-of-Succinate-Dehydrogenases-in-Nematodes
This repository contains the code and resources for a mini project developed during the Programming module of my Bioinformatics MSc.  

The project explores the distribution of the multi-subunit enzyme Succinate Dehydrogenase in selected nematode species using Python and high-performance computing (HPC) tools.

## Overview

The project focuses on automating several steps required to analyse the distribution of Succinate Dehydrogenase across nematode species.  
The script is organised into four main functionalities that streamline tasks such as data retrieval, processing, and preparation of HPC jobs.

---
## Project Workflow

The analysis follows a simple pipeline:

1. Download protein FASTA datasets for selected nematode species from WormBase Parasite.
2. Retrieve PFAM HMM profiles associated with Succinate Dehydrogenase.
3. Run HMMER searches (hmmsearch) against the protein datasets.
4. Parse the HMMER output files.
5. Summarise the distribution of Succinate Dehydrogenase across species.

## Functionalities

### 1. Download FASTA Data

Downloads and extracts protein FASTA files for selected nematode species from the WormBase Parasite FTP.

Example species:
- Brugia malayi

The files are saved in the working directory.

### 2. Retrieve Pfam HMM Profiles

Extracts PFAM identifiers for Succinate Dehydrogenase from a provided TSV file.

The script then downloads the corresponding HMM profiles from the InterPro/Pfam database and decompresses them for further analysis.

### 3. Generate HPC Submission Script

Creates a SLURM shell script used to run HMMER searches on a high-performance computing (HPC) system.

The script prepares commands that run `hmmsearch` using the downloaded HMM profiles against the protein FASTA datasets.

### 4. Parse and Analyse HMMER Outputs

Parses the output files produced by HMMER.

The results can then be summarised and explored using tables or simple visualisations (for example, examining the distribution of Succinate Dehydrogenase across species).

---

## User Guide

### Prerequisites

Python 3.x with the following libraries:

- pandas  
- biopython  
- matplotlib  

Access to a SLURM-based HPC system (optional, for running large HMMER searches).

A Unix/Linux-based environment is recommended.

---
## Project Context

This project was originally developed as part of coursework during my MSc in Bioinformatics and later cleaned and organised for presentation on GitHub.
