Install SLURM
   ```
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
on master node :
```
  sudo cp /etc/munge/munge.key ~
  sudo chmod 777 munge.key
```
copy to all the nodes 
```
for node in vm1 vm2 vm3 vm4 vm5 vm6 vm7; do
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
for all nodes :
```
for node in "${nodes[@]}"; do
    ssh $node "
    sudo apt-get install slurm-wlm -y"
done
```
on vm0 open the config file : `sudo nano /etc/slurm*/slurm.conf`
Copy and modify the config file accordingly. Hostnames in the conf should match with actual hostnames of the machines. Cloudlab tends to have long hostname like vm7.clemson-fab-nf.eva-public-pg0.clemson.cloudlab.us. change them to simpler like vm7 and match them in the conf. Command to see hostname is `hostname` and to change is `sudo hostnamectl set-hostname vm7`: 
```
ControlMachine=Node1
  
MpiDefault=pmi2
ProctrackType=proctrack/linuxproc
ReturnToService=2
SlurmctldPidFile=/var/run/slurmctld.pid
SlurmctldPort=6817
SlurmdPidFile=/var/run/slurmd.pid
SlurmdPort=6818
SlurmdSpoolDir=/var/spool/slurmd
SlurmUser=root
SlurmdUser=root
StateSaveLocation=/var/spool/slurm
SwitchType=switch/none
TaskPlugin=task/none

SchedulerType=sched/backfill
SelectType=select/cons_res
SelectTypeParameters=CR_Core

AccountingStorageType=accounting_storage/slurmdbd
AccountingStorageHost=localhost
ClusterName=cluster
JobAcctGatherType=jobacct_gather/linux
SlurmdLogFile=/var/log/slurm/slurmd.log
SlurmdDebug=debug2

SlurmctldDebug=5
SlurmctldLogFile=/var/log/slurm/slurmctld.log
DebugFlags=gres

NodeName=Node1 NodeAddr=192.168.1.10 CPUs=24 RealMemory=64296 Sockets=24 CoresPerSocket=1 ThreadsPerCore=1 STATE=UNKNOWN
NodeName=Node2 NodeAddr=192.168.1.11 CPUs=24 RealMemory=128000 Sockets=24 CoresPerSocket=1 ThreadsPerCore=1 STATE=UNKNOWN
NodeName=Node3 NodeAddr=192.168.1.12 CPUs=24 RealMemory=128000 Sockets=24 CoresPerSocket=1 ThreadsPerCore=1 STATE=UNKNOWN
NodeName=Node4 NodeAddr=192.168.1.13 CPUs=24 RealMemory=128000 Sockets=24 CoresPerSocket=1 ThreadsPerCore=1 STATE=UNKNOWN
NodeName=vm4 NodeAddr=192.168.1.1 CPUs=40 RealMemory=242000 Sockets=2 CoresPerSocket=10 ThreadsPerCore=2 STATE=UNKNOWN
NodeName=vm5 NodeAddr=192.168.1.2 CPUs=40 RealMemory=242000 Sockets=2 CoresPerSocket=10 ThreadsPerCore=2 STATE=UNKNOWN
NodeName=vm6 NodeAddr=192.168.1.3 CPUs=40 RealMemory=242000 Sockets=2 CoresPerSocket=10 ThreadsPerCore=2 STATE=UNKNOWN
NodeName=vm7 NodeAddr=192.168.1.4 CPUs=40 RealMemory=242000 Sockets=2 CoresPerSocket=10 ThreadsPerCore=2 STATE=UNKNOWN
PartitionName=nodes Nodes=ALL Default=YES MaxTime=INFINITE State=UP
PartitionName=cloudlab Nodes=vm4,vm5,vm6,vm7 Default=NO MaxTime=INFINITE State=UP 
PartitionName=fabric Nodes=Node2,Node3,Node4 Default=NO MaxTime=INFINITE State=UP
JobAcctGatherFrequency=30
```

```
for node in "${nodes[@]}"; do
	scp /etc/slurm*/slurm.conf $node:~/
   ssh $node 'sudo mv ~/slurm.conf /etc/slurm/'
done
```
on worker nodes (add or remove the node names according to cluster configuration)
```
for node in vm1 vm2 vm3 vm4 vm5 vm6 vm7; do
    ssh $node sudo systemctl start slurmd
done
```
on master :
```
sudo apt install slurmdbd -y
sudo nano /etc/slurm/slurmdbd.conf
```
add following in conf : 
```
AuthType=auth/munge
DbdHost=localhost
DbdPort=6819
SlurmUser=root
StorageType=accounting_storage/mysql
StorageHost=localhost
StorageUser=slurm
StorageLoc=slurm_acct_db
LogFile=/var/log/slurm/slurmdbd.log
PidFile=/var/run/slurmdbd.pid
```
run this: 
```
sudo mysql <<'SQL'
CREATE DATABASE IF NOT EXISTS slurm_acct_db;
CREATE USER IF NOT EXISTS 'root'@'localhost';
GRANT ALL PRIVILEGES ON slurm_acct_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
SQL
```

```
sudo systemctl enable slurmdbd
sudo systemctl start slurmdbd
sudo systemctl status slurmdbd
```

```
sudo systemctl start slurmctld
sinfo
```

Do `sinfo` to verify all nodes are setup and in idle. If you see node in `idle` do 
```
sudo scontrol update NodeName=Node1 State=DOWN Reason="resetting"  
sudo scontrol update NodeName=Node1 State=RESUME 
sudo scontrol reconfigure
sudo systemctl restart slurmctld
```
