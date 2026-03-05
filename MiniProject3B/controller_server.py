import sys
import subprocess

ie = sys.argv[1]

print("Received I_E:", ie)

# send command to worker
subprocess.run([
    "ssh",
    "Node2",
    f"python worker.py {ie}"
])