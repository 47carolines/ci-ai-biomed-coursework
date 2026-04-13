import subprocess
import re
import os
import time

# -------------------------------------------------
# VM CONFIG
# -------------------------------------------------
VMS = [
    "2001:1948:417:7:f816:3eff:fe92:eb83" # add other VMs as needed
]

KEY = os.path.expanduser("~/.ssh/fabric_sliver_key")
CONFIG = os.path.expanduser("~/.ssh/config.txt")

# -------------------------------------------------
# HEX MAPPING (DEPLOYMENT LAYER)
# -------------------------------------------------
ACTION_TO_HEX = {
    "FAST_MOVE": "microbit-full-move.hex",
    "MOVE": "microbit-small-step.hex",
    "IDLE": "microbit-FLashing-Heart.hex"
}

# -------------------------------------------------
# VM EXECUTION LAYER
# -------------------------------------------------
def run_vm(vm, I_E):
    cmd = f"""
    set -e
    cd ~/fear_simulation

    echo "=============================="
    echo "[VM] Starting simulation with I_E={I_E}"
    echo "=============================="

    echo "[Step] Updating parameters"
    python update_params.py {I_E}

    echo "[Step] Running simulation"
    python run_bionet.py config.json

    echo "[Step] Extracting output"
    python check_output.py

    echo "[VM] Done"
    """

    process = subprocess.Popen(
        [
            "ssh",
            "-i", KEY,
            "-F", CONFIG,
            f"ubuntu@{vm}",
            cmd
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    output = ""
    for line in process.stdout:
        print(line, end="", flush=True)  # 👈 LIVE LOGGING
        output += line

    process.wait()
    return output


# -------------------------------------------------
# PARSE FREQUENCY OUTPUT
# -------------------------------------------------
def extract_freq(output):
    match = re.search(r"([\d.]+)\s*Hz", output)
    return float(match.group(1)) if match else 0.0


# -------------------------------------------------
# COLLECT ALL VM RESULTS
# -------------------------------------------------
def run_all(I_E_values):
    freqs = []

    for vm, I_E in zip(VMS, I_E_values):
        print(f"[VM] Running {vm} with I_E={I_E}")
        out = run_vm(vm, I_E)
        freq = extract_freq(out)

        print(f"[VM] {vm} → {freq:.2f} Hz")
        freqs.append(freq)

    return freqs


# -------------------------------------------------
# DECISION CONTROLLER (YOUR LOGIC, CLEANED)
# -------------------------------------------------
def decision_controller(freqs):
    avg_freq = sum(freqs) / len(freqs)

    breathing = 0.2 + (avg_freq / 50)
    breathing = min(max(breathing, 0.2), 2.0)

    if avg_freq > 18:
        action = "FAST_MOVE"
    elif avg_freq > 12:
        action = "MOVE"
    else:
        action = "IDLE"

    return {
        "action": action,
        "breathing": breathing,
        "avg_freq": avg_freq,
        "raw": freqs
    }


# -------------------------------------------------
# DEPLOY HEX (MICRO:BIT OR SIMULATED)
# -------------------------------------------------
def deploy_hex(hex_file):
    MICROBIT_DRIVE = "/Volumes/MICROBIT"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, hex_file)

    print(f"[Deploy] Using {hex_file}")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing hex file: {full_path}")

    timeout = 10
    while timeout > 0 and not os.path.exists(MICROBIT_DRIVE):
        time.sleep(1)
        timeout -= 1

    if not os.path.exists(MICROBIT_DRIVE):
        raise FileNotFoundError("Micro:bit not mounted")

    subprocess.run(["cp", full_path, MICROBIT_DRIVE])
    print(f"[Deploy] {hex_file} → MICROBIT SUCCESS")


# -------------------------------------------------
# MAIN HUB PIPELINE
# -------------------------------------------------
def main(I_E_values):
    print("\n=== HUB START ===")

    # Step 1: run VMs
    freqs = run_all(I_E_values)

    # Step 2: decision
    result = decision_controller(freqs)

    print("\n=== DECISION ===")
    print(result)

    # Step 3: map to hex
    action = result["action"]
    hex_file = ACTION_TO_HEX[action]

    print(f"[Hub] Action → {action}")
    print(f"[Hub] Deploying → {hex_file}")

    # Step 4: deploy
    deploy_hex(hex_file)

    print("\n=== HUB COMPLETE ===")


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    I_E_VALUES = [10]  # example inputs
    main(I_E_VALUES)