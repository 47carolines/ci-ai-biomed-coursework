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
echo "Submitted batch job $JOB_ID"

echo '[Worker] Waiting for simulation completion'

while squeue -j $JOB_ID > /dev/null 2>&1
do
    sleep 5
done

echo '[Worker] Simulation finished'

python check_output.py > freq.txt

cat freq.txt
"""

result = subprocess.run(
    ["ssh", "Node2", "bash", "-lc", worker_cmd],
    capture_output=True,
    text=True
)

print(result.stdout.strip(), flush=True)
print(result.stderr.strip(), flush=True)

log("Controller pipeline finished.")