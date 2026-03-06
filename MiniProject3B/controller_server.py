import sys
import subprocess

ie = sys.argv[1]

print("Received I_E:", ie)

subprocess.run([
    "ssh",
    "Node2",
    update_cmd
], shell=True)

# ---- Run worker simulation pipeline ----
worker_cmd = f"""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

cd ~/CI-BioEng-Class/fear_simulation

sed -i 's/I_E = .*/I_E = {ie}/' parameters.py

python build_network.py
python update_configs.py

sbatch batch.sh

sleep 15

python check_output.py > freq.txt

cat freq.txt
"""

freq_result = subprocess.run(
    ["ssh", "Node2", worker_cmd],
    capture_output=True,
    text=True,
    shell=True
)

print(freq_result.stdout.strip())