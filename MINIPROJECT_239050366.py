#### Mini Project -  Comparing the distribution of Succinate Dehydrogenases in Nematodes

import os
import shutil
import requests
import gzip

## 1 - Get FASTA data

def download_protein_FASTA(url, folder_name="."):
    local_filename = os.path.join(folder_name, url.split('/')[-1])

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None  

    if local_filename.endswith('.gz'):
        decompressed_filename = local_filename[:-3]  
        with gzip.open(local_filename, 'rb') as f_in, open(decompressed_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        return decompressed_filename
    else:
        return local_filename[:-3]

# Examples of 3 urls to use from https://parasite.wormbase.org/ftp.html
urls = [
    'https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS18/species/caenorhabditis_tribulationis/PRJEB12608/caenorhabditis_tribulationis.PRJEB12608.WBPS18.protein.fa.gz',
    'https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS18/species/bursaphelenchus_xylophilus/PRJEA64437/bursaphelenchus_xylophilus.PRJEA64437.WBPS18.protein.fa.gz',
    'https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS18/species/ditylenchus_dipsaci/PRJNA498219/ditylenchus_dipsaci.PRJNA498219.WBPS18.protein.fa.gz',
]

# Download and decompress each file in the current working directory
fastas = []
for url in urls:
    fastas.append(download_protein_FASTA(url))
    
### 2 - Get Pfam HMM profiles

import subprocess
import pandas as pd

def get_Pfam_HMM():
    
    df = pd.read_csv('SearchResults-succinatedehydrogenase.tsv', sep="\t")
    identifier = df.loc[df['Accession'].str.startswith('PF'),'Accession'].tolist()
    for PFAM in identifier:
        Pfam_HMM = f'wget https://www.ebi.ac.uk/interpro/wwwapi//entry/pfam/{PFAM}?annotation=hmm -O {PFAM}.gz && gunzip {PFAM}.gz' # This will download the PFAM HMMs and uncompress them subsequently
        subprocess.call(Pfam_HMM, shell=True)
    return identifier
   
hmms = get_Pfam_HMM()

### 3 - Prepare HPC HMMer run


def generate_shell_SLURM(fastas, hmms):
    script_name = input("please enter the name you wish to call your alice script (with .sh at the end): ")

    script_content = """#!/usr/bin/bash
    #SBATCH --job-name=SLURM_test 
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=02:00:00 
    #SBATCH --mem=8gb 
    #SBATCH --mail-type=BEGIN,END,FAIL
    #SBATCH --mail-user=vpc5@student.le.ac.uk  
    #SBATCH --export=NONE

    # setting files/directories
    out='/home/r/vpc5/Mini_project'
    dbase1='/scratch/strubio/vpc5/'
    hmm='/scratch/strubio/vpc5/hmms'

    #hmmsearch='/home/r/vpc5/bin/hmmsearch'

    #executable from ALICE
    hmmsearch='/cm/shared/spack/opt/spack/linux-rocky9-x86_64_v3/gcc-12.3.0/hmmer-3.3.2-ipmjfm2vvzhroirpnpn5i4rw5wptqf7r/bin/hmmsearch'

    #module needed for using HPC installed software
    #module load gcc/12.3.0-yxgv2bl
    #module load openmpi/4.1.5-fzc7xdf
    #module load hmmer/3.3.2-ipmjfm2

    for hmm in hmms:
        for fasta in fastas:
            file.write("hmmsearch --tblout ${output_dir}/"+ "-" + hmm + ".out -E 0.1 --noali ${hmm_dir}/" + hmm + ".hmm ${fasta_dir}/" + fasta + "\n")"""

    with open(script_name, 'w') as file:
        file.write(script_content)
    
generate_shell_SLURM(fastas, hmms)




















  




