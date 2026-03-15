#### Mini Project - Comparing the distribution of Succinate Dehydrogenases in Nematodes

import os
import shutil
import requests
import gzip
import subprocess
import pandas as pd

## 1 - Get FASTA data

def download_protein_FASTA(url, folder_name="."):
    os.makedirs(folder_name, exist_ok=True)

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
        return local_filename


# Examples of 3 urls to use from https://parasite.wormbase.org/ftp.html
urls = [
    'https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS18/species/caenorhabditis_tribulationis/PRJEB12608/caenorhabditis_tribulationis.PRJEB12608.WBPS18.protein.fa.gz',
    'https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS18/species/bursaphelenchus_xylophilus/PRJEA64437/bursaphelenchus_xylophilus.PRJEA64437.WBPS18.protein.fa.gz',
    'https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS18/species/ditylenchus_dipsaci/PRJNA498219/ditylenchus_dipsaci.PRJNA498219.WBPS18.protein.fa.gz',
]

# Download and decompress each file into a fasta folder
fastas = []
for url in urls:
    fasta_file = download_protein_FASTA(url, folder_name="fastas")
    if fasta_file is not None:
        fastas.append(os.path.basename(fasta_file))


### 2 - Get Pfam HMM profiles

def get_Pfam_HMM():
    os.makedirs("hmms", exist_ok=True)

    df = pd.read_csv('SearchResults-succinatedehydrogenase.tsv', sep="\t")
    identifier = df.loc[df['Accession'].str.startswith('PF'), 'Accession'].tolist()

    for PFAM in identifier:
        Pfam_HMM = f'wget https://www.ebi.ac.uk/interpro/wwwapi/entry/pfam/{PFAM}?annotation=hmm -O hmms/{PFAM}.gz && gunzip -f hmms/{PFAM}.gz'
        subprocess.call(Pfam_HMM, shell=True)

    return identifier


hmms = get_Pfam_HMM()


### 3 - Prepare HPC HMMer run

def generate_shell_SLURM(fastas, hmms):
    script_name = input("Please enter the name you wish to call your alice script (with .sh at the end): ")

    os.makedirs("results", exist_ok=True)

    with open(script_name, 'w') as file:
        file.write("#!/usr/bin/bash\n")
        file.write("#SBATCH --job-name=SLURM_test\n")
        file.write("#SBATCH --nodes=1\n")
        file.write("#SBATCH --tasks-per-node=1\n")
        file.write("#SBATCH --time=02:00:00\n")
        file.write("#SBATCH --mem=8gb\n")
        file.write("#SBATCH --mail-type=BEGIN,END,FAIL\n")
        file.write("#SBATCH --mail-user=your_email@example.com\n")
        file.write("#SBATCH --export=NONE\n\n")

        file.write("# Load HMMER module if needed on your HPC\n")
        file.write("module load hmmer\n\n")

        file.write("# Run hmmsearch for each HMM against each FASTA file\n")
        for hmm in hmms:
            for fasta in fastas:
                output_file = f"results/{fasta}-{hmm}.out"
                command = f"hmmsearch --tblout {output_file} -E 0.1 --noali hmms/{hmm} fastas/{fasta}\n"
                file.write(command)

    print(f"{script_name} has been created.")


generate_shell_SLURM(fastas, hmms)



  




