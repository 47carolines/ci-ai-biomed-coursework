import subprocess
import re
import time
import os
import shutil

controller_host = "2610:1e0:1700:206:f816:3eff:fe86:38c9"

# -------------------------------------------------
# Frequency parsing
# -------------------------------------------------
def extract_frequency(text):
    match = re.search(r"FiringRate:\s+(\d+\.\d+)", text)
    return float(match.group(1)) if match else None

# -------------------------------------------------
# Main pipeline
# -------------------------------------------------
def main():
    ie = input("Enter current injection amplitude (nA): ")
    print(f"Sending I_E = {ie} to controller node...")

    t0 = time.time()

    # -------------------------------------------------
    # Step A: Run simulation on controller node
    # -------------------------------------------------
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
    t1 = time.time()

    # -------------------------------------------------
    # Step B: Decision
    # -------------------------------------------------
    frequency = extract_frequency(buffer_output)
    threshold = 5.0  # Hz

    if frequency is None:
        print("Failed to extract frequency, defaulting to small step")
        frequency = 0.0

    if frequency >= threshold:
        print(f"[Controller] Frequency {frequency:.2f} Hz >= {threshold} Hz → full movement")
        hex_file = "microbit-full-move.hex"
    else:
        print(f"[Controller] Frequency {frequency:.2f} Hz < {threshold} Hz → small step")
        hex_file = "microbit-small-step.hex"

    print(f"[Decision] Deploying {hex_file}")

    # -------------------------------------------------
    # Step C: Deploy via USB (MakeCode style)
    # -------------------------------------------------
    t2 = time.time()

    MICROBIT_DRIVE = "/Volumes/MICROBIT"

    try:
        if not os.path.exists(MICROBIT_DRIVE):
            raise FileNotFoundError("Micro:bit not mounted")

        # Resolve relative path from script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_hex_path = os.path.join(script_dir, hex_file)

        shutil.copy(full_hex_path, MICROBIT_DRIVE)
        print(f"[Robot] Copied {full_hex_path} → MICROBIT")

    except Exception as e:
        print(f"[Robot] Deployment failed: {e}")

    t3 = time.time()

    # -------------------------------------------------
    # Latency report
    # -------------------------------------------------
    print("\n[Latency report]")
    print(f"Step A (Simulation)       : {t1 - t0:.3f} s")
    print(f"Step B (Decision)         : {t2 - t1:.3f} s")
    print(f"Step C (Robot execution)  : {t3 - t2:.3f} s")
    print(f"Total pipeline latency    : {t3 - t0:.3f} s")
    print("[Pipeline finished]")


if __name__ == "__main__":
    main()