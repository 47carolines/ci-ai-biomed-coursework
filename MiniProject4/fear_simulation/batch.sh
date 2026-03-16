#!/bin/bash

#SBATCH --job-name=sim          # Job name
#SBATCH -N 1                    # Nodes
#SBATCH -n 1                    # Total tasks
#SBATCH --ntasks-per-node=1     # Tasks per node
#SBATCH --partition=debug      # Queue
#SBATCH --output=slurm_output_%j.txt  # SLURM output file
#SBATCH --chdir=/home/ubuntu/fear_simulation  # Working directory

# Record start time
START=$(date)

# Activate conda environment
eval "$(~/miniconda3/bin/conda shell.bash hook)"
conda activate fear_sim

# Print debug info
echo "----------------------------------------"
echo "[DEBUG] SLURM running on: $(hostname)"
echo "[DEBUG] Current working directory: $(pwd)"
echo "[DEBUG] I_E in parameters.py:"
grep 'I_E' parameters.py
echo "----------------------------------------"

# Rebuild network
echo "[Worker] Building network"
python build_network.py

# Update configs if needed
echo "[Worker] Updating configs"
python update_configs.py

# Run the simulation
echo "[Worker] Running simulation"
srun python run_bionet.py config.json

# Optionally run check_output.py for firing rate
echo "[Worker] Calculated firing rate:"
python check_output.py

# Record end time
END=$(date)
echo "Start: $START"
echo "End:   $END"