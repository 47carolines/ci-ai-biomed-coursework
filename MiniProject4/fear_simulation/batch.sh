#!/bin/bash

#SBATCH --job-name=sim
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=worker
#SBATCH --output=slurm_output_%j.txt
#SBATCH --chdir=/home/ubuntu/CI-BioEng-Class/fear_simulation

START=$(date)

eval "$(~/miniconda3/bin/conda shell.bash hook)"
conda activate fear_sim

srun python run_bionet.py config.json

END=$(date)
printf "Start: $START \nEnd:   $END\n"