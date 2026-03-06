import subprocess
import re

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"

def log(msg):
    print(msg)

ie = input("Enter current injection amplitude (nA): ")

log(f"Sending I_E = {ie} to controller node...")

# Send request to controller node
result = subprocess.run([
    "ssh",
    "-i", "slice_key",
    "-F", "ssh_config",
    f"ubuntu@{controller_host}",
    f"python3 controller_server.py {ie}"
], capture_output=True, text=True)

stdout = result.stdout + result.stderr

log("Controller response:")
log(stdout)

# Extract frequency
match = re.search(r"[\d]+\.?[\d]*", stdout)

if not match:
    print("Failed to get frequency from controller output.")
    exit()

frequency = match.group(0)

print(f"Received frequency: {frequency}")

# Update microbit firmware file
try:
    with open("flicker.py", "r") as f:
        lines = f.readlines()

    lines[0] = f"frequency = {frequency}\n"

    with open("flicker.py", "w") as f:
        f.writelines(lines)

    print("Flashing flicker.py to microbit...")
    subprocess.run(["uflash", "flicker.py"])

except Exception as e:
    print("Microbit flashing failed:", e)

print("Pipeline finished.")