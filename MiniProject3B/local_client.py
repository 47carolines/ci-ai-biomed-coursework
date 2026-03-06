import subprocess
import re

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"


# -------------------------------------------------
# Frequency parsing (robust version)
# -------------------------------------------------
def extract_frequency(text):
    """
    Extract the last floating point number in output.
    This is robust to pipeline logging noise.
    """

    matches = re.findall(r"\d+\.\d+", text)

    if len(matches) == 0:
        return None

    return matches[-1]


# -------------------------------------------------
# Main pipeline
# -------------------------------------------------
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

    # Stream logs live
    for line in process.stdout:
        print(line, end="", flush=True)
        buffer_output += line

    process.wait()

    # Extract frequency
    frequency = extract_frequency(buffer_output)

    if frequency is None:
        print("Failed to extract frequency")
        return

    print(f"Received frequency: {frequency}")


    # -------------------------------------------------
    # Rewrite frequency inside flicker.py safely
    # -------------------------------------------------
    try:
        print("Flashing microbit...")

        with open("flicker.py", "r") as f:
            lines = f.readlines()

        # Replace existing frequency line if present
        found = False

        for i, line in enumerate(lines):
            if "frequency =" in line:
                lines[i] = f"frequency = {frequency}\n"
                found = True
                break

        # If no frequency line exists, insert after imports
        if not found:
            insert_index = 1 if len(lines) > 0 else 0
            lines.insert(insert_index, f"frequency = {frequency}\n")

        with open("flicker.py", "w") as f:
            f.writelines(lines)

        subprocess.run(["uflash", "flicker.py"])

        print("Microbit flashing complete")

    except Exception as e:
        print("Microbit flashing failed:", e)

    print("Pipeline finished.")


# -------------------------------------------------
if __name__ == "__main__":
    main()