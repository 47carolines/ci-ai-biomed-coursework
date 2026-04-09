# Virtual Machine Setup for Mini-Project 5

## Part 1: Creating and SSHing into FABRIC VM

Disclaimer: This documentation assumes you have a FABRIC account, you are in the CI4Neuroscience Project, and you have set up a sliver and bastion keys for your account and that you have them locally on your computer. If not, please watch and follow along Ajay's FABRIC setup video from Week 3 on Canvas.

1. Go to FABRIC Portal website here: https://portal.fabric-testbed.net/ and Log in using your umsystem credentials.
2. Click on Experiments in the top navbar and then click Projects & Slices, then click CI4Neuroscience. Then click Slices, and click the Create Slice button.
3. Enter the following node information:

Step 2: Add Nodes Section
* Site: UTAH
* Node Name: firstname-node
* Cores: 4
* RAM (GB): 8
* Disk (GB): 50
* OS Image: Ubuntu 22

Step 4: Create Slice Section
* Slice Name: firstname-slice
* Lease End Time: 2026-4-16 00:00:00
* SSH Keys: fabric-sliver-key (or whatever you named your sliver key)

Double check your setup matches this picture and then click Create Slice when you are ready. Wait up to 2-3 minutes for the slice to provision.
* ![alt text](<Screenshot 2026-04-08 at 19.44.11.png>)

One the slice status is Green or StableOk, click the white square which is your node in your topology. Then you should be able to see the SSH Command. Click the copy icon on the SSH Command it and go to a terminal on your computer. It should look something like this, but with your unique hostname:
```
ssh -F <path to SSH config file> -i <path to private sliver key> ubuntu@2001:1948:417:7:f816:3eff:fe92:eb83
```
![alt text](<Screenshot 2026-04-08 at 19.54.12.png>)

Navigate to the folder you have your config and private sliver key in. Enter the SSH command and you should be inside the node.
![alt text](image.png)

## Part 2: Setting up the Environment

### 🔐 Allowing Caroline’s SSH Access (FABRIC Controller)

To allow the central controller (Caroline) to SSH into your VM, you must add her **FABRIC sliver public key** to your VM’s authorized keys.

This enables secure access for orchestration and automation using FABRIC’s SSH system.

---

### 📌 Caroline’s Public FABRIC Key

Add the following public key to your VM:

```text
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDTJwsTLfX7wjHCMdP4t2GPjqJIDNKp1rZye1ZtayD1q44HXNJLsgmzVXif4y/A6UAwoAcdYnM6aDB3UWHalRgg= fabric-sliver-key
```
1. Open authorized keys file
```
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
```

2. Add Caroline’s key
	*	Paste the key above on a new line
	*	Do not modify or wrap the key
	*	Ensure each key in the file is on its own line

3. Save and exit nano
    *	Press CTRL + X
    *	Press Y
    *	Press Enter

4. Set correct permissions
```
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Verification

Caroline can now access your VM using:
```
ssh -F ~/.ssh/config -i ~/.ssh/fabric_sliver_key ubuntu@<vm-name>
```

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

## Part 3: Run the network

Run these commands to build the network:
```
cd ~/fear_simulation
python build_network.py
python update_configs.py
```

Run `python run_bionet.py config.json` to run the simulation.

Run `python check_output.py` to compute the oscillation frequency. 