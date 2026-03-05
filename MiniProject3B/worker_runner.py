import sys
import subprocess

ie = sys.argv[1]

cmd = f"""
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fear_sim

python build_network.py
python update_configs.py
sbatch batch.sh
python check_output.py
"""

subprocess.run(["ssh", "Node2", cmd])