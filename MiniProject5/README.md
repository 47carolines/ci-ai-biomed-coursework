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

## Part 2: 🔐 Allowing Caroline’s SSH Access (FABRIC Controller)

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

Once you have completed this step, please send Caroline the Hostname/Management IP Address of your virtual machine so she can test login. It should look something like this: `2001:1948:417:7:f816:3eff:fe92:eb83`

You can find it in FABRIC in the right hand side details column:
![alt text](<Screenshot 2026-04-08 at 19.54.12.png>)
