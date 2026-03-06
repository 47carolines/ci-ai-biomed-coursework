import subprocess

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"

ie = input("Enter current injection amplitude (nA): ")

# Send I_E to controller node
result = subprocess.run([
    "ssh",
    "-i", "slice_key",
    "-F", "ssh_config",
    f"ubuntu@{controller_host}",
    f"python3 controller_server.py {ie}"
], capture_output=True, text=True)

# Controller should print frequency
frequency = result.stdout.strip()

print("Received frequency:", frequency)

# Launch microbit flicker
subprocess.run([
    "python3",
    "flicker.py",
    frequency
])