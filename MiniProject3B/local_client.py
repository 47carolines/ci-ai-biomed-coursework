import subprocess
import re

controller_host = "2610:1e0:1700:206:f816:3eff:fefe:fc1b"

def main():

    ie = input("Enter current injection amplitude (nA): ")

    print(f"Sending I_E = {ie} to controller node...")

    cmd = f"python3 controller_server.py {ie}"

    # Stream output live from controller node
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

    # Live logging
    output_buffer = ""

    for line in process.stdout:
        print(line, end="", flush=True)
        output_buffer += line

    process.wait()

    print("Controller pipeline finished.")

    # Extract frequency
    match = re.search(r"[\d]+\.?[\d]*", output_buffer)

    if not match:
        print("Failed to get frequency from controller output.")
        return

    frequency = match.group(0)

    print(f"Received frequency: {frequency}")

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


if __name__ == "__main__":
    main()