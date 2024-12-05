# Comparing-the-distribution-of-Succinate-Dehydrogenases-in-Nematodes
This repository contains the code and resources for a Mini Project conducted as part of the Programming module for my Bioinformatics degree, focusing on the use of functions, where we analyse the distribution of the multi-subunit enzyme Succinate Dehydrogenase in selected nematode species using Python and high-performance computing (HPC) tools.

## Overview

The project focuses on automating data preparation and analysis to study the distribution of Succinate Dehydrogenase. The program includes four key functionalities, designed to streamline tasks like data retrieval, processing, and HPC job preparation.

---

## Functionalities

**1. Download FASTA Data**

    Fetches and unpacks protein FASTA files for three nematode species from WormBase Parasite FTP.
    Example species: Brugia malayi
    Files are saved in the working directory.

**2. Retrieve Pfam HMM Profiles**

    Extracts PFAM identifiers for Succinate Dehydrogenase from a provided TSV file.
    Downloads the corresponding PFAM HMM profiles from the EBI database.
    Saves and decompresses HMM profiles in the working directory.

**3. Generate HPC Submission Script**

    Creates a shell script for submitting jobs to the SLURM scheduler on the University of Leicester’s ALICE HPC system.
    Includes instructions for running HMMer searches with downloaded HMMs against the FASTA files.

**4. Parse and Analyze HMMer Outputs**

    Parses the output files from HMMer.
    Summarizes and analyzes data using tables and graphs (e.g., visualizing distribution).

---

## User Guide

Prerequisites

    Python 3.x with the following libraries:
        pandas
        biopython
        matplotlib
    SLURM scheduler access to ALICE HPC.
    Unix-based environment.
