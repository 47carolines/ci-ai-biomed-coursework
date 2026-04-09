import subprocess
import re

VMS = [
    "ubuntu@vm1-ip",
    "ubuntu@vm2-ip",
    "ubuntu@vm3-ip"
]

KEY = "~/.ssh/fabric_key"

def run_vm(vm, I_E):
    cmd = f"""
    ssh -i {KEY} {vm} '
    cd ~/fear_simulation &&
    python update_params.py {I_E} &&
    python run_bionet.py config.json &&
    python check_output.py
    '
    """

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def extract_freq(output):
    match = re.search(r"([\d.]+)\s*Hz", output)
    return float(match.group(1)) if match else 0


def run_all(I_E_values):
    freqs = []

    for vm, I_E in zip(VMS, I_E_values):
        print(f"Running VM {vm} with I_E={I_E}")
        out = run_vm(vm, I_E)
        freq = extract_freq(out)
        freqs.append(freq)

    return freqs