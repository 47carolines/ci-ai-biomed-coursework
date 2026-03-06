import sys
import subprocess

def log(msg):
    print(msg, flush=True)

ie = sys.argv[1]

log(f"Received I_E: {ie}")
log("Starting worker pipeline on Node2")

worker_cmd = f"""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

cd ~/CI-BioEng-Class/fear_simulation

echo '[Worker] Updating parameters.py'
sed -i "s/I_E = .*/I_E = {ie}/" parameters.py

echo '[Worker] Building network'
python build_network.py

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
    if [[ "$STATUS" == "COMPLETED" || "$STATUS" == "FAILED" || "$STATUS" == "" ]]; then
        break
    fi
    sleep 2
done

echo '[Worker] Simulation finished'

python check_output.py
"""

process = subprocess.Popen(
    ["ssh", "Node2", "bash", "-lc", worker_cmd],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

for line in process.stdout:
    print(line, end="", flush=True)

process.wait()

print("Controller pipeline finished.", flush=True)