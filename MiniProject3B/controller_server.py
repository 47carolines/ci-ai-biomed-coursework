import sys
import subprocess

ie = sys.argv[1]

print("Received I_E:", ie)

# ---- Run worker simulation pipeline on Node2 ----
worker_cmd = f"""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

cd ~/CI-BioEng-Class/fear_simulation

sed -i "s/I_E = .*/I_E = {ie}/" parameters.py

python build_network.py
python update_configs.py

sbatch batch.sh

sleep 15

python check_output.py > freq.txt

cat freq.txt
"""

freq_result = subprocess.run(
    ["ssh", "Node2", f"bash -lc '{worker_cmd}'"],
    capture_output=True,
    text=True
)

print(freq_result.stdout.strip())
print(freq_result.stderr.strip())