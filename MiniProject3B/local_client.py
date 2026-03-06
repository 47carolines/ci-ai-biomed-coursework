import subprocess
import re

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"

def log(msg):
    print(msg, flush=True)

ie = input("Enter current injection amplitude (nA): ")

log(f"Sending I_E = {ie} to controller node...")

# Send request to controller node
cmd = f"python3 controller_server.py {ie}"

result = subprocess.run([
    "ssh",
    "-i", "slice_key",
    "-F", "ssh_config",
    f"ubuntu@{controller_host}",
    cmd
], text=True, capture_output=True)

output = result.stdout + result.stderr

log("===== Controller Output =====")
log(output)

# Extract frequency
match = re.search(r"[\d]+\.?[\d]*", output)

if not match:
    log("Failed to extract frequency.")
    exit()

frequency = match.group(0)

log(f"Received frequency: {frequency}")

# Update microbit firmware file
try:
    print("Updating flicker firmware...")
    with open("flicker.py", "r") as f:
        lines = f.readlines()

    lines[0] = f"frequency = {frequency}\n"

    with open("flicker.py", "w") as f:
        f.writelines(lines)

    print("Flashing microbit...")
    subprocess.run(["uflash", "flicker.py"])

    print("Microbit flashing complete.")

except Exception as e:
    print("Flashing failed:", e)

print("Pipeline finished.")