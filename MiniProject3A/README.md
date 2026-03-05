# Slurm Installation and Configuration on 3-node cluster 

This repository contains scripts to set up and configure a Slurm cluster (vm0 master and vm1,vm2 as worker nodes). The scripts are designed to automate the installation and configuration process for the master node and worker nodes.
---

Step: 1 Run the below chunk on `vm0` (worker node):
```
nodes=(vm0 vm1 vm2)
for node in "${nodes[@]}"; do
  ssh $node "
  sudo apt update
  sudo apt-get install libmunge-dev libmunge2 munge
  sudo apt install -y slurmdbd mariadb-server
  sudo systemctl enable --now mariadb
  sudo systemctl enable munge
  sudo systemctl start munge
  sudo munge -n | unmunge | grep STATUS"
done
```

Step: 2 Copying munge key on worker nodes (run it on `vm0`):  
```
sudo cp /etc/munge/munge.key ~
sudo chmod 777 munge.key
```

```
for node in vm1 vm2; do
	scp ~/munge.key $node:~/
done
for node in "${nodes[@]}"; do
    ssh $node "
    sudo rm /etc/munge/munge.key
    sudo cp ~/munge.key /etc/munge/
    sudo chmod 400 /etc/munge/munge.key
    sudo chmod 700 /etc/munge/
    sudo chown munge:munge /etc/munge/munge.key
    sudo systemctl restart munge
    sudo systemctl status munge --no-pager"
done
for node in "${nodes[@]}"; do
    ssh $node "
    sudo systemctl restart munge "
done
```

Step: 3 Installing slurm-wlm on all nodes:  
```
for node in "${nodes[@]}"; do
    ssh $node "
    sudo apt-get install slurm-wlm -y"
done
```

Step: 4 Copy the `slurm.conf` file at `/etc/slurm/slurm.conf` and `/etc/slurm-llnl/slurm.conf` (_you can create slurm directory if it doesnot exist in /etc directory_)  

Step: 5 Copying slurm.conf in other worker nodes:  

```
for node in "${nodes[@]}"; do
	scp /etc/slurm*/slurm.conf $node:~/
   ssh $node 'sudo mv ~/slurm.conf /etc/slurm/'
done
```
😎😎😎😎😎😎Eureka, You made it.😎😎😎😎😎😎

Execute the `sinfo` command on `vm0` to make sure its working. It should show,
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
nodes*       up   infinite      2   idle Node[2-3]
fabric       up   infinite      2   idle Node[2-3]

## Testing
Modify accordingly and Execute the script `job_deployment_script.sh` on master node to deploy jobs on worker node.  
You may use, `squeue` to see the status of your job.  
After job completion you should have output_12345.txt or error_12345.txt in your worker node. 
