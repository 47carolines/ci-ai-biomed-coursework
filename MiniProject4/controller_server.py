import sys
import subprocess

def log(msg):
    print(msg, flush=True)

# -------------------------------------------------
# Get I_E value from command-line
# -------------------------------------------------
ie = sys.argv[1]
log(f"Received I_E: {ie}")
log("Starting worker pipeline on Node2")

# -------------------------------------------------
# SSH commands to run on Node2
# -------------------------------------------------
worker_cmd = f"""
set -e  # Exit immediately if any command fails

# Activate conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

cd ~/fear_simulation

echo '[Worker] Updating parameters.py'
python update_params.py {ie}

echo '[Worker] Building network'
python build_network.py

echo '[Worker] Updating configs'
python update_configs.py

echo '[Worker] Submitting SLURM job'
JOB_ID=$(sbatch --partition=debug batch.sh | awk '{{print $4}}')
echo "Submitted batch job $JOB_ID"
echo $JOB_ID > job_id.txt

# -------------------------------------------------
# Wait for SLURM job completion using squeue
# -------------------------------------------------
echo '[Worker] Waiting for simulation completion'
while true; do
    STATUS=$(squeue -j $JOB_ID -h -o "%T" | tr -d ' ')
    
    if [[ -z "$STATUS" ]]; then
        echo "[Worker] Job finished (not in queue anymore)"
        break
    elif [[ "$STATUS" == "COMPLETED" ]]; then
        echo "[Worker] Simulation completed successfully!"
        break
    elif [[ "$STATUS" == "FAILED" ]]; then
        echo "[Worker] Simulation FAILED!"
        break
    else
        echo "[Worker] Job status: $STATUS"
    fi
    sleep 2
done

echo '[Worker] Pipeline finished.'
"""

# -------------------------------------------------
# Run the SSH command from controller
# -------------------------------------------------
worker_cmd = worker_cmd.strip()
process = subprocess.Popen(
    ["ssh", "Node2", "bash", "-lc", worker_cmd],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Stream logs live
for line in process.stdout:
    print(line, end="", flush=True)

process.wait()
log("Controller pipeline finished.")