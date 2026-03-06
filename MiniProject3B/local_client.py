import subprocess
import re

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"

ie = input("Enter current injection amplitude (nA): ")

result = subprocess.run([
    "ssh",
    "-i", "slice_key",
    "-F", "ssh_config",
    f"ubuntu@{controller_host}",
    f"python3 controller_server.py {ie}"
], capture_output=True, text=True)

match = re.search(r"[\d.]+", result.stdout)

if not match:
    print("Failed to get frequency")
    exit()

frequency = match.group(0)

print("Received frequency:", frequency)

# Update microbit firmware file
with open("flicker.py", "r") as f:
    lines = f.readlines()

lines[0] = f"frequency = {frequency}\n"

with open("flicker.py", "w") as f:
    f.writelines(lines)

# Flash microbit
subprocess.run(["uflash", "flicker.py"])