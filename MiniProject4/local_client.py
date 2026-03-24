import subprocess
import re
import time

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

    # -------------------------
    # Step A: Run simulation
    # -------------------------
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

    # -------------------------
    # Step B: Decision
    # -------------------------
    frequency = extract_frequency(buffer_output)
    threshold = 5.0

    if frequency is None:
        print("Failed to extract frequency → defaulting to small step")
        frequency = 0.0

    if frequency >= threshold:
        mode = "FULL_MOVEMENT"
        print(f"[Controller] {frequency:.2f} Hz ≥ {threshold} Hz → FULL MOVEMENT")
    else:
        mode = "SMALL_STEP"
        print(f"[Controller] {frequency:.2f} Hz < {threshold} Hz → SMALL STEP")

    print(f"[Decision] Mode selected: {mode}")

    t2 = time.time()

    # -------------------------
    # Step C: Robot execution (REALISTIC MODEL)
    # -------------------------
    print("\n[Robot] Cutebot executing preloaded behavior...")
    print(f"[Robot] Mode received: {mode}")

    # This is your "execution trigger"
    if mode == "FULL_MOVEMENT":
        print("[Robot] Executing full movement sequence")
        # robot already flashed with full routine
    else:
        print("[Robot] Executing small step sequence")
        # robot already flashed with small-step routine

    t3 = time.time()

    # -------------------------
    # Latency report
    # -------------------------
    print("\n[Latency report]")
    print(f"Step A (Simulation)       : {t1 - t0:.3f} s")
    print(f"Step B (Decision)         : {t2 - t1:.3f} s")
    print(f"Step C (Robot execution)  : {t3 - t2:.3f} s")
    print(f"Total pipeline latency    : {t3 - t0:.3f} s")
    print("[Pipeline finished]")

if __name__ == "__main__":
    main()