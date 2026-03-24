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

    t0 = time.time()  # Step A start

    # Step A: Run simulation on controller node
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
    t1 = time.time()  # Step B start

    # Step B: Decision
    frequency = extract_frequency(buffer_output)
    threshold = 5.0  # Hz
    if frequency is None:
        print("Failed to extract frequency, defaulting to small step")
        frequency = 0.0

    # Log clearly above/below threshold
    if frequency >= threshold:
        print(f"[Controller] Frequency {frequency:.2f} Hz >= {threshold} Hz → using full movement")
        cutebot_script = "cutebot_move_task.hex"
    else:
        print(f"[Controller] Frequency {frequency:.2f} Hz < {threshold} Hz → using small step")
        cutebot_script = "cutebot_step.hex"

    print(f"[Decision] Flashing Cutebot with {cutebot_script}")

    # Step C: Flash Cutebot
    t2 = time.time()
    try:
        subprocess.run(["uflash", cutebot_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[Robot] Cutebot execution failed: {e}")
    t3 = time.time()

    # Latency summary
    print("\n[Latency report]")
    print(f"Step A (Simulation)       : {t1 - t0:.3f} s")
    print(f"Step B (Decision)         : {t2 - t1:.3f} s")
    print(f"Step C (Robot execution)  : {t3 - t2:.3f} s")
    print(f"Total pipeline latency    : {t3 - t0:.3f} s")
    print("[Pipeline finished]")

if __name__ == "__main__":
    main()