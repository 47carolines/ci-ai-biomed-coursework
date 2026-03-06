import subprocess
import re

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"

def extract_frequency(text):
    # Look for lines mentioning oscillation or Hz
    candidates = [
        line for line in text.split("\n")
        if "Hz" in line or "oscillat" in line
    ]

    for line in reversed(candidates):
        match = re.search(r"\d+\.\d+", line)
        if match:
            return match.group(0)

    return None

def main():

    ie = input("Enter current injection amplitude (nA): ")

    print(f"Sending I_E = {ie} to controller node...")

    cmd = f"python3 controller_server.py {ie}"

    process = subprocess.Popen(
        [
            "ssh",
            "-i", "slice_key",
            "-F", "ssh_config",
            f"ubuntu@{controller_host}",
            cmd
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    buffer_output = ""

    for line in process.stdout:
        print(line, end="", flush=True)
        buffer_output += line

    process.wait()

    frequency = extract_frequency(buffer_output)

    if frequency is None:
        print("Failed to extract frequency")
        return

    print(f"Received frequency: {frequency}")

    # Flash microbit firmware
    try:
        print("Flashing flicker.py to microbit")

        with open("flicker.py", "r") as f:
            lines = f.readlines()

        lines[0] = f"frequency = {frequency}\n"

        with open("flicker.py", "w") as f:
            f.writelines(lines)

        subprocess.run(["uflash", "flicker.py"])

        print("Microbit flashing complete")

    except Exception as e:
        print("Microbit flashing failed:", e)

    print("Pipeline finished")

if __name__ == "__main__":
    main()