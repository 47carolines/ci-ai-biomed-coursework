#!/usr/bin/env python
# coding: utf-8

# # Creating a cluster/slice

# ## Please read carefully all the instructions. Specially the comments given in each cell. These comments are pertinent to run a cluster successfully. 
# 
# If the fabric environment is not set please read through the topic <code>FABRIC Environment Setup</code> in <code>start_here.ipynb</code> notebook given under <code>jupyter-example</code> folder in fabric's JupyterHub.
# 
# <b> At first read the comments in the cell and then only run the cell. </b>

# ## STEP-1

# In[ ]:


# Run this cell
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
try:
    # Update this line to specify your project id
    project_id = "7db31408-b695-427c-8856-8761292228b6"

    fablib = fablib_manager(
        project_id=project_id
    )
    fablib.show_config()
    fablib.verify_and_configure()
    fablib.save_config()
except Exception as e:
    print(f"Exception: {e}")


# In[158]:


# slice_name='GPU_Variant_Calling_FIU'
# node_name='Node2'
# slice = fablib.get_slice(slice_name)
# node = slice.get_node(node_name)
# node.os_reboot()


# In[2]:


# Run this cell
# To find all the available resources at this time
# run the cell below for easier readability 
try:
    resources = fablib.list_sites()
except Exception as e:
    print(f"Exception: {e}")


# In[3]:


# for easier readability of available resources
import pandas as pd 
pd.DataFrame(resources.data)[['Hosts','CPUs','Name','Cores Available','Ram Available','Tesla T4 Available','RTX6000 Available','A30 Available','A40 Available']]


# ## Step-2: Creating a cluster from an instance type.

# In[40]:


# Run this cell
# Initialize the variables appropriately. 
# Number of nodes in the cluster.
num_nodes=6

# Give a cluster name
slice_name='DeepPrep'

# Make it True if you want to include persistence storage to a single node. KEEP IT FALSE FOR THE TIME BEING.
storage=False

# get attached to the cluster. By default adding NVMe is false.
add_NVMe = True

# Make it True if you want to include GPUs to different nodes in the cluster [depends on availability].
add_gpu=True

# By default master node will not have GPUs in it. For CPU only cluster False means lower resources then the workers.
master_gpu=False

# If only t4 gpu needs to be added.
add_t4=True

# If only rtx gpu needs to be added.
add_rtx=True

# If only rtx gpu needs to be added.
add_a40=False


# Site name, pick one site from the above list of resources.
site='GPN'

# Select node resource:- It follows the pattern fabric.c#N.m#N.d#N , where c:cores, m:primary memory, d:disk and #N: capacity.
# eg: fabric.c4.m8.d50 means cores:4, Memory:8Gb, disk:50Gb  
# List of node instance type is provided in - https://github.com/fabric-testbed/InformationModel/blob/master/fim/slivers/data/instance_sizes.json
#instance_worker='fabric.c24.m128.d500'
instance_worker='fabric.c24.m64.d1000'

# The resources of master node. It is better to be less than the worker nodes.
instance_master='fabric.c8.m64.d500'

# Operation system, Linux distribution e.g. default_ubuntu_18, default_ubuntu_20, etc.
image='default_ubuntu_20'


# In[41]:


import pandas as pd

try:
    json_format=fablib.list_sites(output='json',quiet=True)
except Exception as e:
    print(f"Exception: {e}")

sites_df=pd.read_json(json_format)
site_df=sites_df[sites_df['name']==site]
type_t4=site_df['tesla_t4_available'].values
type_rtx=site_df['rtx6000_available'].values
type_a40=site_df['a40_available'].values

nvme_available=site_df['nvme_available'].values
print("Number of Nvidia t4 available now at",site,"is:", type_t4[0])
print("Number of Nvidia rtx6000 available now at",site,"is:", type_rtx[0])
print("Number of Nvidia A40 available now at",site,"is:", type_a40[0])
print("Number of NVMe available now at",site,"is:", nvme_available[0])

max_type_t4 = type_t4[0]
max_type_rtx = type_rtx[0]
max_type_a40 = type_a40[0]

total_gpus = max_type_t4 + max_type_rtx + max_type_a40



# In[42]:


# The max available GPU for the chosen site is mentioned above, to change it please make changes to the variables below.
# By default initialized with the available GPUs for the site.

custom_number_of_t4 = max_type_t4
custom_number_of_rtx = max_type_rtx
custom_number_of_a40 = max_type_a40


# custom_number_of_t4 = 3
# custom_number_of_rtx =4

if custom_number_of_t4 < max_type_t4 or custom_number_of_rtx < max_type_rtx:
    max_type_t4 = custom_number_of_t4
    max_type_rtx = custom_number_of_rtx
    total_gpus = max_type_t4 + max_type_rtx
print(total_gpus)
gpu_names=[]

for i in range(1,total_gpus+1):
    gpu_names.append("GPU_{0}".format(i))
 
print(gpu_names)
temp_t4=max_type_t4
temp_rtx=max_type_rtx

######################################################
#####                  NVMe                      #####
######################################################

# Assumption: If the number of available NVMes' are less than the number of cluster node minus the master NVMes' will not

if nvme_available >= num_nodes-1 and add_NVMe == True:
    add_NVMe = True
print(add_NVMe)


# In[43]:


# Run this cell

node_names=[]
nic_names=[]
iface_names=[]
nvme_names=[]
network_name='cluster_network'
storage_name = 'gaf-storage'

for i in range(1,num_nodes+1):
    node_names.append("Node{0}".format(i))
    nic_names.append("Nic{0}".format(i))
    iface_names.append("iface{0}".format(i))
    nvme_names.append("nvme{0}".format(i))

print(node_names)
print(nic_names)
print(iface_names)
print(nvme_names)


# In[44]:


# Only run when persistence storage needed to be attached. 
if storage == True:
    import traceback
    from plugins import Plugins
    try:
        Plugins.load()
    except Exception as e:
        traceback.print_exc()
print(temp_t4)
print(temp_rtx)


# In[45]:


print(add_a40)


# In[46]:


# # Run this cell, Visit the link below to find different instance type options. 
# # Read the comments carefully given below and make changes as necessary. 
# ## Allocating 2 A40 GPUs on VM1 (worker node) and VM0 as managing node
# try:
#     slice=fablib.new_slice(name=slice_name)
#     for i in range(num_nodes):
#         if master_gpu == False and i == 0:
#             node=slice.add_node(name=node_names[i],
#                                 site=site, 
#                                 instance_type=instance_master,
#                                 image=image)
#             iface_names[i]=node.add_component(model='NIC_Basic', name=node_names[i]).get_interfaces()[0]
#         else:
#             node=slice.add_node(name=node_names[i],
#                                 site=site,
#                                 instance_type=instance_worker,
#                                 image=image)
#             iface_names[i]=node.add_component(model='NIC_Basic',name=node_names[i]).get_interfaces()[0]
#             if add_gpu == True:
#                 print(i)
#                 if add_a40 == True  and i == 1: # Attach 2-A40 GPUs on VM1 machine
#                     node.add_component(model='GPU_A40', name=gpu_names[i-1])
#                     node.add_component(model='GPU_A40', name=gpu_names[i-2])
#                     print("allocated 2 A40 GPUs")
#                     type_a40 = type_a40 - 2 
#                 else: 
#                     print("No GPUs available")
#             if add_NVMe == True:
#                 node.add_component(model='NVME_P4510', name=nvme_names[i-1])
#             else:
#                 print("NVMe not avail")
# except Exception as e:
#     print(f'Exception: {e}') 


# In[47]:


# # Run this cell, Visit the link below to find different instance type options. 
# # Read the comments carefully given below and make changes as necessary. 

# try:
#     slice=fablib.new_slice(name=slice_name)
    
#     for i in range(num_nodes):
#         if master_gpu == False and i == 0:
#             node=slice.add_node(name=node_names[i],
#                                 site=site, 
#                                 instance_type=instance_master,
#                                 image=image)
#             iface_names[i]=node.add_component(model='NIC_Basic', name=node_names[i]).get_interfaces()[0]
        
#         else:
#             node=slice.add_node(name=node_names[i],
#                                 site=site,
#                                 instance_type=instance_worker,
#                                 image=image)
#             iface_names[i]=node.add_component(model='NIC_Basic',name=node_names[i]).get_interfaces()[0]
            
#             if add_gpu == True:
#                 print(i)
#                 if add_t4 == True and temp_t4 > 1 and i==1: # allocating 2 T4
#                     node.add_component(model='GPU_TeslaT4', name=gpu_names[i-1])
#                     node.add_component(model='GPU_TeslaT4', name=gpu_names[i-2])
#                     temp_t4 = temp_t4 - 2 
#                     print("allocated 2T4")
#                 if add_t4 == True and temp_t4 > 0 and i==2: # allocating 1 T4
#                     node.add_component(model='GPU_TeslaT4', name=gpu_names[i-1])
#                     temp_t4 = temp_t4 - 1 
#                     print("allocated 1T4")
#                 # if add_rtx == True and temp_rtx >2 and i==3: # allocating 3rtx
#                 #     node.add_component(model='GPU_RTX6000',name=gpu_names[i-1])
#                 #     node.add_component(model='GPU_RTX6000',name=gpu_names[i-2])
#                 #     node.add_component(model='GPU_RTX6000',name=gpu_names[i-3])
#                 #     temp_rtx = temp_rtx - 3
#                 #     print("allocated 3rtx")
#                 if add_rtx == True and temp_rtx >1 and i==3: # allocating 2 T4
#                     node.add_component(model='GPU_RTX6000',name=gpu_names[i-1])
#                     node.add_component(model='GPU_RTX6000',name=gpu_names[i-2])
#                     temp_rtx = temp_rtx - 2
#                     print("allocated 2rtx")
#                 if add_rtx == True and temp_rtx >0 and i==4: # allocating 1 rtx
#                     node.add_component(model='GPU_RTX6000',name=gpu_names[i-1])
#                     temp_rtx = temp_rtx - 1
#                     print("allocated 1rtx")
#                 else: 
#                     print("No GPUs available")
#             if add_NVMe == True:
#                 node.add_component(model='NVME_P4510', name=nvme_names[i-1])
# except Exception as e:
#     print(f'Exception: {e}') 


# In[48]:


# Run this cell, Visit the link below to find different instance type options. 
# Read the comments carefully given below and make changes as necessary. 

try:
    slice=fablib.new_slice(name=slice_name)
    
    for i in range(num_nodes):
        if master_gpu == False and i == 0:
            node=slice.add_node(name=node_names[i],
                                site=site, 
                                instance_type=instance_master,
                                image=image)
            iface_names[i]=node.add_component(model='NIC_Basic', name=node_names[i]).get_interfaces()[0]
        
        else:
            node=slice.add_node(name=node_names[i],
                                site=site,
                                instance_type=instance_worker,
                                image=image)
            iface_names[i]=node.add_component(model='NIC_Basic',name=node_names[i]).get_interfaces()[0]
            
            if add_gpu == True:
                print(i)
                if add_t4 == True and temp_t4 > 1 and i==1: # allocating 2 T4
                    node.add_component(model='GPU_TeslaT4', name=gpu_names[i-1])
                    node.add_component(model='GPU_TeslaT4', name=gpu_names[i-2])
                    temp_t4 = temp_t4 - 2 
                    print("allocated 2T4")
                if add_t4 == True and temp_t4 > 0 and i==2: # allocating 1 T4
                    node.add_component(model='GPU_TeslaT4', name=gpu_names[i-1])
                    temp_t4 = temp_t4 - 1 
                    print("allocated 1T4")
                if add_rtx == True and temp_rtx >2 and i==3: # allocating 3rtx
                    node.add_component(model='GPU_RTX6000',name=gpu_names[i-1])
                    node.add_component(model='GPU_RTX6000',name=gpu_names[i-2])
                    node.add_component(model='GPU_RTX6000',name=gpu_names[i-3])
                    temp_rtx = temp_rtx - 3
                    print("allocated 3rtx")
                if add_rtx == True and temp_rtx >1 and i==4: # allocating 2 T4
                    node.add_component(model='GPU_RTX6000',name=gpu_names[i-1])
                    node.add_component(model='GPU_RTX6000',name=gpu_names[i-2])
                    temp_rtx = temp_rtx - 2
                    print("allocated 2rtx")
                if add_rtx == True and temp_rtx >0 and i==5: # allocating 1 rtx
                    node.add_component(model='GPU_RTX6000',name=gpu_names[i-1])
                    temp_rtx = temp_rtx - 1
                    print("allocated 1rtx")
                else: 
                    print("No GPUs available")
            if add_NVMe == True:
                node.add_component(model='NVME_P4510', name=nvme_names[i-1])
            else:
                print("NVMe not avail")
except Exception as e:
    print(f'Exception: {e}') 


# In[49]:


# Run this cell
try:
    net_cluster=slice.add_l2network(name=network_name, interfaces=iface_names[:])
except Exception as e:
    print(f"Exception: {e}")


# In[50]:


# Run this cell
# If this cell get executed successfully then IP address of the nodes will be displayed which can be used to ssh into the respective nodes.
# If there is an error while creating the slice/cluster, repeat from the third code cell block.
try:
    slice.submit()
except Exception as e:
    print(f'Exception: {e}')
    


# ## Step-3: Configuring the network and setting up the cluster

# In[51]:


# try:
#     slice=fablib.get_slice(name="GPU_Variant_Calling_FIU") # Put the cluster name that you want to delete
#     # slice.delete()
# except Exception as e:
#     print(f"Exception: {e}")


# In[52]:


#Run this cell
from ipaddress import IPv4Address, IPv4Network
try:
    subnet=IPv4Network("192.168.1.0/24")
    available_ips=list(subnet)[1:]
except Exception as e:
    print(f"Exception: {e}")


# In[53]:


try:
   for node in slice.get_nodes():
       node_iface=node.get_interface(network_name=network_name)
       # print(node_iface)
       stdout, stderr = node.execute(f'ip addr show {node_iface.get_os_interface()}')
       # print(stdout,stderr)
except Exception as e:
   print(f"Exception: {e}")


# In[54]:


#Run this cell
#%%capture
try:
    for node in slice.get_nodes():
        node_iface=node.get_interface(network_name=network_name)
        node_IP_addr=available_ips.pop(0)
        node_iface.ip_addr_add(addr=node_IP_addr, subnet=subnet)
        stdout, stderr = node.execute(f'ip addr show {node_iface.get_os_interface()}')
        _, _ = node.execute('sudo apt-get update')
        stdout, stderr = node.execute('sudo apt install net-tools')        
        stdout, stderr = node.execute(f'sudo ifconfig {node_iface.get_os_interface()} up')
except Exception as e:
    print(f"Exception: {e}")


# In[55]:


#Run this cell
# If the ping is successful, that means the nodes are connected properly if there is any error then may need to recreate the cluster or further have to look into it. 
try:
    node1=slice.get_node(name='Node1')
    stdout,stderr=node1.execute(f' ping -c 3 192.168.1.4')
    print(stdout)
    print(stderr)
except Exception as e:
    print(f'Exception: {e}')


# In[56]:


# Run this cell
# Function to create a file that contains IPs and hostnames related to it.

def append_line(file_path,text):
    with open(file_path,"a+") as file_des:
        file_des.seek(0)
        data=file_des.read(-1)
        if len(data)>0:
            file_des.write("\n")
        file_des.write(text)


# In[57]:


# Run this cell

import os

if os.path.isfile('/home/fabric/work/hosts') or os.path.isfile('/home/fabric/work/ips.txt') or os.path.isfile('/home/fabric/work/workers'):
    os.system("rm /home/fabric/work/hosts")
    os.system("rm /home/fabric/work/ips.txt")
    os.system("rm /home/fabric/work/workers")    
else:
    print("does not exist")

if os.path.isfile('/home/fabric/work/gpu_ips.txt'):
    os.system("rm /home/fabric/work/gpu_ips.txt")
    
#os.system("rm /home/fabric/work/ips.txt")


# In[ ]:


# Run this cell

# Capturing the IP addresses, this step needs to be integrated with the IP assigning stage, coded above. Or it may stay independent.
import os

i=1
local_host="127.0.0.1 localhost"
path_to_host_file="/home/fabric/work/hosts"
path_to_ip_file="/home/fabric/work/ips.txt"
path_to_worker_ip="/home/fabric/work/workers"
path_to_gpu_ips="/home/fabric/work/gpu_ips.txt"
gpu_name="NVIDIA"

append_line(path_to_host_file,local_host)

try:
    for node in slice.get_nodes():
        stdout, stderr=node.execute("hostname -I")
        IP=stdout.split(" ")[1]
        node_name="node{0}".format(i)
        vm_names="vm{0}".format(i-1)
        append_line(path_to_ip_file,IP)
        
        stdout, stderr=node.execute("hostname")
        line=IP+" "+node_name+" "+vm_names+" "+stdout
        append_line(path_to_host_file,line)
      
    
        if(i>1):
            append_line(path_to_worker_ip,vm_names)
            #append_line(path_to_worker_ip,IP)
        
        print(line)
        print(stderr)
        
        stdout_gpu, _=node.execute('lspci | grep NVIDIA')   
        if gpu_name in stdout_gpu:
            stdout_ip, _=node.execute('hostname -I')
            ip=stdout_ip.split(" ")[1]
            append_line(path_to_gpu_ips,ip)
            #print(ip)
        
        i=i+1
except Exception as e:
    print(f"Exception: {e}")
    
print(IP)


# In[ ]:


# Run this cell
try:
    for node in slice.get_nodes():
        stdout, stderr=node.execute(f'sudo cp /etc/hosts /etc/hosts_backup') # if you run the command twice the back up will be overwritten, a conditional block should be written
        output_host_copy=node.upload_file(path_to_host_file,"/home/ubuntu/hosts")
        output_ip_copy=node.upload_file(path_to_ip_file,"/home/ubuntu/ips.txt")
        output_worker_copy=node.upload_file(path_to_worker_ip,"/home/ubuntu/workers")
        stdout_host_copy,stderr_host_copy=node.execute(f'sudo cp /home/ubuntu/hosts /etc/hosts')
        if os.path.isfile('/home/fabric/work/gpu_ips.txt'):
            output_gpu_copy=node.upload_file(path_to_gpu_ips,"/home/ubuntu/gpu_ips.txt")
        print(stderr)
        print(stderr_host_copy)
except Exception as e:
    print(f"Exception : {e}")
    


# In[ ]:


# Run this cell

import os

output=os.system('ssh-keygen -q -t rsa -N "" -f /home/fabric/work/id_rsa > /dev/null 2>&1')


# In[ ]:


# Run this cell

try:
    for node in slice.get_nodes():
        output_private=node.upload_file("/home/fabric/work/id_rsa","/home/ubuntu/.ssh/id_rsa")
        output_public=node.upload_file("/home/fabric/work/id_rsa.pub","/home/ubuntu/.ssh/id_rsa.pub")
        
        stdout, stderr=node.execute(f' cat /home/ubuntu/.ssh/id_rsa.pub >> /home/ubuntu/.ssh/authorized_keys')
        stdout, stderr=node.execute(f' chmod 600 /home/ubuntu/.ssh/id_rsa*')
        
        print(output_private)
        print(output_public)
        print(stderr)
        #print(stdout)
        
except Exception as e:
    print(f"Exception: {e}")


# In[ ]:


# Run this cell. This is the last cell to run. Please read the comments in the next few cells to know how to extend the lease time and how to delete a slice/cluster. 

from ipaddress import ip_address, IPv6Address
try:
    for node in slice.get_nodes():
        if type(ip_address(node.get_management_ip())) is IPv6Address:
            node.upload_file("/home/fabric/work/nat64.sh", "/home/ubuntu/nat64.sh")
            #stdout, stderr=node.execute(f' chmod +x /home/ubuntu/nat64.sh && sudo bash /home/ubuntu/nat64.sh')
            stdout, stderr=node.execute(f' chmod +x /home/ubuntu/nat64.sh && sudo bash /home/ubuntu/nat64.sh > /dev/null 2>&1')
            print(stdout)
            print(stderr)
except Exception as e:
    print(f"Exception: {e}")
    


# ## Step-4: Deleting and extending lease of a slice

# In[ ]:


# # Run this cell ONLY when you want to delete the cell
# # To delete a slice/cluster.
# try:
#     slice=fablib.get_slice(name="AVAH") # Put the cluster name that you want to delete
#     slice.delete()
# except Exception as e:
#     print(f"Exception: {e}")


# In[ ]:


# # Run this cell ONLY when you want to exted the time of the slice. Or to extend the lease time of the slice/cluster.

# import datetime
# slice_name='demo' # Give the cluster/slice name that you want to extend

# #Set end host to now plus 1 day
# new_end_date = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S %z")
# #new_end_date = (datetime.now(timezone.utc) + timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S %z")
# print(type(new_end_date), new_end_date)
# try:
#     slice=fablib.get_slice(name=slice_name)
#     slice.renew('2023-05-31 18:04:26 +0000') # Give the new lease end date and time of the slice. One can increase it by 7 days from the day of creation of the slice/cluster. 
    
#     #print(f"Lease End (UTC)        : {slice.get_lease_end()}")
# except Exception as e:
#     print(f"Exception: {e}")


# In[ ]:


# # Run this cell ONLY to observe the new lease time.

# slice_name='cluster_exp' # Give the slice/cluster name that you just extended. 
# try:
#     slice = fablib.get_slice(name=slice_name)
#     print(f"{slice}")
# except Exception as e:
#     print(f"Exception: {e}")


# In[ ]:


# # Run this cell ONLY to observe the new lease time.

# slice_name='cluster_gpu' # Give the slice/cluster name that you just extended. 
# try:
#     slice = fablib.get_slice(name=slice_name)
#     gpu_name="NVIDIA"
#     for node in slice.get_nodes():
#         #stdout, stderr=node.execute(f'sudo cp /etc/hosts /etc/hosts_backup') # if you run the command twice the back up will be overwritten, a conditional block should be written
#         stdout_gpu, _=node.execute('lspci | grep NVIDIA')   
#         if gpu_name in stdout_gpu:
#             stdout_ip, _=node.execute('hostname -I')
#             ip=stdout_ip.split(" ")[1]
#             print(ip)
# except Exception as e:
#     print(f"Exception: {e}")

