import subprocess

ie = input("Enter current injection amplitude (nA): ")

subprocess.run([
    "ssh",
    "-i", "slice_key",
    "-F", "ssh_config",
    "ubuntu@2610:1e0:1700:206:f816:3eff:fefe:fc1b",
    f"python controller_script.py {ie}"
])