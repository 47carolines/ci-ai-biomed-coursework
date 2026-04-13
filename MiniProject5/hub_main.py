import subprocess
import re
import os
import time

# -------------------------------------------------
# INPUT STIMULUS SOURCES (TEAM MEMBERS / BRAIN AREAS)
# -------------------------------------------------
VM_STIMULUS_MAP = {
    "vm1": "2001:1948:417:7:f816:3eff:fe92:eb83", # Caroline (Low)
    "vm2": "2001:1948:417:7:f816:3eff:fe5e:1458", # Scott (Medium)
    "vm3": "2001:1948:417:7:f816:3eff:fed1:1280" # Noor (High)
}

KEY = os.path.expanduser("~/.ssh/fabric-sliver-key")
CONFIG = os.path.expanduser("~/.ssh/config.txt")

# -------------------------------------------------
# MOTOR OUTPUT MAPPING (CUTEBOT ACTION LAYER)
# -------------------------------------------------
ACTION_TO_HEX = {
    "FAST_MOVE": "microbit-full-move.hex",
    "MOVE": "microbit-small-step.hex",
    "IDLE": "microbit-FLashing-Heart.hex"
}

# -------------------------------------------------
# STIMULUS EXECUTION LAYER (VM = BRAIN AREA INPUT)
# -------------------------------------------------
def run_vm(vm_id, I_E):
    vm_ip = VM_STIMULUS_MAP[vm_id]

    print("\n======================================")
    print(f"[STIMULUS] Team Member / Brain Area: {vm_id}")
    print(f"[THALAMUS HUB] Dispatching stimulus to {vm_ip}")
    print(f"[PARAMETER] I_E = {I_E}")
    print("======================================")

    cmd = f"""
    set -e

    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate fear_sim

    cd ~/fear_simulation

    echo "[VM-{vm_id}] Stimulus received by cortical area"
    echo "[VM-{vm_id}] Running neural simulation pipeline"

    python update_params.py {I_E}
    python build_network.py
    python update_configs.py
    python run_bionet.py config.json
    python check_output.py

    echo "[VM-{vm_id}] Output ready"
    """

    process = subprocess.Popen(
        [
            "ssh",
            "-i", KEY,
            "-F", CONFIG,
            f"ubuntu@{vm_ip}",
            cmd
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    output = ""
    for line in process.stdout:
        print(line, end="", flush=True)
        output += line

    process.wait()
    return output


# -------------------------------------------------
# OUTPUT EXTRACTION (NEURAL RESPONSE)
# -------------------------------------------------
def extract_freq(output):
    match = re.search(r"([\d.]+)\s*Hz", output)
    return float(match.group(1)) if match else 0.0


# -------------------------------------------------
# COLLECT ALL BRAIN AREA RESPONSES
# -------------------------------------------------
def run_all(vm_inputs):
    freqs = []

    for vm_id, I_E in vm_inputs:
        print("\n--------------------------------------")
        print(f"[HUB] Receiving stimulus from {vm_id}")
        print("--------------------------------------")

        out = run_vm(vm_id, I_E)
        freq = extract_freq(out)

        print(f"[RESULT] {vm_id} → {freq:.2f} Hz neural response")
        freqs.append(freq)

    return freqs


# -------------------------------------------------
# DECISION COORDINATION CONTROLLER (THRESHOLD + INTEGRATION)
# -------------------------------------------------
def decision_controller(freqs):
    avg_freq = sum(freqs) / len(freqs)

    breathing = 0.2 + (avg_freq / 50)
    breathing = min(max(breathing, 0.2), 2.0)

    if avg_freq > 19:
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
# CUTEBOT EXECUTION LAYER
# -------------------------------------------------
def deploy_hex(hex_file):
    MICROBIT_DRIVE = "/Volumes/MICROBIT"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, hex_file)

    print(f"[CUTEBOT] Deploying motor program: {hex_file}")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing hex file: {full_path}")

    timeout = 10
    while timeout > 0 and not os.path.exists(MICROBIT_DRIVE):
        time.sleep(1)
        timeout -= 1

    if not os.path.exists(MICROBIT_DRIVE):
        raise FileNotFoundError("Micro:bit not mounted")

    subprocess.run(["cp", full_path, MICROBIT_DRIVE])

    print(f"[CUTEBOT] Execution successful → movement triggered")


# -------------------------------------------------
# MAIN HUB (INPUT → INTEGRATION → OUTPUT)
# -------------------------------------------------
def main(vm_inputs):
    print("\n=== INPUT/OUTPUT HUB (THALAMUS ANALOGUE) START ===")

    # Step 1: collect stimuli from brain areas
    freqs = run_all(vm_inputs)

    # Step 2: integrate signals
    result = decision_controller(freqs)

    print("\n=== DECISION COORDINATION RESULT ===")
    print(result)

    # Step 3: motor mapping
    action = result["action"]
    hex_file = ACTION_TO_HEX[action]

    print(f"[HUB] Coordinated output → {action}")
    print(f"[HUB] Sending to Cutebot → {hex_file}")

    # Step 4: execute movement
    deploy_hex(hex_file)

    print("\n=== SYSTEM COMPLETE ===")


# -------------------------------------------------
# ENTRY POINT (TEAM MEMBER SIMULATION)
# -------------------------------------------------
if __name__ == "__main__":

    vm_inputs = [
        ("vm1", 0.5),
        ("vm2", 0.9),
        ("vm3", 1.2)
    ]

    main(vm_inputs)