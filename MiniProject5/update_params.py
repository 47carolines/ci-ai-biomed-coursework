# update_params.py
import sys

ie = sys.argv[1]

with open('parameters.py', 'r') as f:
    lines = f.readlines()

with open('parameters.py', 'w') as f:
    for line in lines:
        if line.lstrip().startswith('I_E ='):
            indent = line[:len(line) - len(line.lstrip())]
            f.write(f"{indent}I_E = {ie}\n")
        else:
            f.write(line)