import sys
import subprocess

def log(msg):
    print(msg)

ie = sys.argv[1]

log(f"Received I_E: {ie}")
log("Launching worker simulation pipeline on Node2...")

worker_cmd = f"""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

cd ~/CI-BioEng-Class/fear_simulation

echo "Updating parameters.py"
sed -i "s/I_E = .*/I_E = {ie}/" parameters.py

echo "Building network"
python build_network.py

echo "Updating configs"
python update_configs.py

echo "Submitting SLURM job"
JOB_ID=$(sbatch batch.sh | awk '{{print $4}}')
echo "Submitted batch job $JOB_ID"

echo "Waiting for simulation completion"

while squeue -j $JOB_ID > /dev/null 2>&1
do
    sleep 5
done

echo "Simulation finished"

python check_output.py > freq.txt

cat freq.txt
"""

freq_result = subprocess.run(
    ["ssh", "Node2", "bash", "-lc", worker_cmd],
    capture_output=True,
    text=True
)

print(freq_result.stdout.strip())
print(freq_result.stderr.strip())