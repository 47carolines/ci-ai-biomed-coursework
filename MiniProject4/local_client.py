import subprocess
import re
import time

controller_host = "2610:1e0:1700:206:f816:3eff:fe86:38c9"

# -------------------------------------------------
# Frequency parsing
# -------------------------------------------------
def extract_frequency(text):
    matches = re.findall(r"\d+\.\d+", text)
    return float(matches[-1]) if matches else None

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
    if frequency is None:
        print("Failed to extract frequency, defaulting to small step")
        frequency = 0.0

    print(f"[Controller] Received frequency: {frequency}")

    threshold = 15.0  # Hz threshold
    cutebot_script = "cutebot_pattern.py" if frequency >= threshold else "cutebot_step.py"
    print(f"[Decision] Flashing Cutebot with {cutebot_script}")

    t2 = time.time()  # Step C start

    # Step C: Flash Cutebot
    try:
        subprocess.run(["python3", cutebot_script], check=True)
        print("[Robot] Cutebot executed successfully")
    except Exception as e:
        print("[Robot] Cutebot execution failed:", e)

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