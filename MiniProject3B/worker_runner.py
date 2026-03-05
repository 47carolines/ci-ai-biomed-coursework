import sys
import subprocess

ie = sys.argv[1]

print("Running simulation with I_E =", ie)

# update parameters file
subprocess.run(["python", "build_network.py"])
subprocess.run(["python", "update_configs.py"])

# run simulation with SLURM
subprocess.run(["sbatch", "batch.sh"])

# check output
subprocess.run(["python", "check_output.py"])