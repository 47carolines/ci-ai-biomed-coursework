## Setting up the fear simulation

We are going to be setting up the fear simulation that we covered in Mini-Project 1A on the Virtual Machine.

### Install Miniconda:
We need to install Miniconda so we can have Conda to manage our packages and environment. Download miniconda:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
Once downloaded, Install miniconda with this command:
```
bash Miniconda3-latest-Linux-x86_64.sh
```
make sure to review and accept the license agreement. Just install in the default location and proceed with initialization. In order to get changes to take effect, type `exit` to exit the shell and then re-ssh in by entering the SSH command.

You can remove the installation script once installed
```
rm Miniconda3-latest-Linux-x86_64.sh
```

### Create fear_sim environment:
You may be asked to accept the Terms of Service, just say accept and install new packages.
```
conda create --name fear_sim python=3.10
conda activate fear_sim
```
### Install Python libraries:
```
pip install neuron
pip install bmtk
```

### Clone fear_sim environment from GitHub:
```
git clone https://github.com/cyneuro/CI-BioEng-Class.git
```
### Move fear_simulation to home directory and remove other files
```
mv ~/CI-BioEng-Class/fear_simulation ~/
rm -rf CI-BioEng-Class
```

### Compile the modfiles
In order to compile the modfiles you will have to install make, gcc, and libc headers.
```
sudo apt update
sudo apt install -y build-essential
```
Now compile the modfiles:
```
cd fear_simulation/components/mechanisms
nrnivmodl .
```

5. Add `update_params.py` script to `fear_simulation` folder so we can update params on command
6. Update `check_output.py` to new code that doesnt include uflash and other things
7. Update `parameters.py` to remove comments to increase the chance of things updating correctly. 
8. make sure to have `build_network.py` updated to include overwrite_config=True so we can rerun

## Part 3: Run the network

Run these commands to build the network:
```
cd ~/fear_simulation
python build_network.py
python update_configs.py
```

Run `python run_bionet.py config.json` to run the simulation.

Run `python check_output.py` to compute the oscillation frequency. 