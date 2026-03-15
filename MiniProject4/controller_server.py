import sys
import subprocess

def log(msg):
    print(msg, flush=True)

# Get the I_E value from command-line
ie = sys.argv[1]
log(f"Received I_E: {ie}")
log("Starting worker pipeline on Node2")

# Build the full SSH command
worker_cmd = f"""
set -e  # Exit immediately if any command fails

# Activate conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

cd ~/fear_simulation

echo '[Worker] Updating parameters.py'
# Safely update the I_E value
sed -i "s/^I_E = .*/I_E = {ie}/" parameters.py

echo '[Worker] Building network'
python build_network.py --overwrite_config=True

echo '[Worker] Updating configs'
python update_configs.py

echo '[Worker] Submitting SLURM job'
JOB_ID=$(sbatch batch.sh | awk '{{print $4}}')
echo $JOB_ID > job_id.txt
echo "Submitted batch job $JOB_ID"

echo '[Worker] Waiting for simulation completion'
while true
do
    STATUS=$(sacct -j $JOB_ID --format=State --noheader | head -n 1 | tr -d ' ')
    
    if [[ "$STATUS" == "COMPLETED" ]]; then
        echo "[Worker] Simulation completed successfully!"
        break
    elif [[ "$STATUS" == "FAILED" ]]; then
        echo "[Worker] Simulation FAILED!"
        break
    elif [[ -z "$STATUS" ]]; then
        echo "[Worker] Job not yet started, waiting..."
    else
        echo "[Worker] Job status: $STATUS"
    fi
    
    sleep 2
done

echo '[Worker] Checking output'
python check_output.py

echo '[Worker] Pipeline finished.'
"""

# Run the SSH command
worker_cmd = worker_cmd.strip()
process = subprocess.Popen(
    ["ssh", "Node2", "bash", "-lc", worker_cmd],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Stream output live
for line in process.stdout:
    print(line, end="", flush=True)

process.wait()
log("Controller pipeline finished.")