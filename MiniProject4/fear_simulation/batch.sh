#!/bin/bash

#SBATCH --job-name=sim          # Name of the job
#SBATCH -N 1                    # Number of nodes
#SBATCH -n 1                    # Total number of tasks
#SBATCH --ntasks-per-node=1     # Tasks per node
#SBATCH --partition=worker      # Partition/queue to submit to
#SBATCH --output=slurm_output_%j.txt  # SLURM output file
#SBATCH --chdir=/home/ubuntu/fear_simulation  # Working directory

# Record start time
START=$(date)

# Activate conda environment
eval "$(~/miniconda3/bin/conda shell.bash hook)"
conda activate fear_sim

# Optional: rebuild network configs (overwrite if they exist)
python build_network.py

# Run the simulation
srun python run_bionet.py config.json

# Record end time
END=$(date)
printf "Start: $START \nEnd:   $END\n"