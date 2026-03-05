#!/usr/bin/env python
# coding: utf-8

# Clean Minimal Notebook Template for Mini-Project 3A
# Author: ChatGPT
# Purpose: Create 3-node FABRIC cluster + verify connectivity
# 
# This notebook removes unnecessary complexity from the original template.
# It focuses only on what you need to complete the assignment.

# In[ ]:


STEP 0: Install Dependencies (Run Once)


# In[ ]:


# Uncomment if needed
# !pip install fabrictestbed-extensions pandas


# STEP 1: Authentication + FABRIC Setup

# In[1]:


from fabrictestbed_extensions.fablib.fablib import FablibManager

PROJECT_ID = "7db31408-b695-427c-8856-8761292228b6"

try:
    fablib = FablibManager(project_id=PROJECT_ID)
    fablib.verify_and_configure()
    fablib.save_config()
    fablib.show_config()
    print("✅ FABRIC configuration ready")
except Exception as e:
    print("Auth/setup error:", e)


# STEP 1A: Check for Resource Availability
# 
# Key: Look for site with:
# 
# ✅ High cores_available
# ✅ High ram_available
# ✅ (Ignore GPU columns unless required)

# In[3]:


try:
    resources_json = fablib.list_sites(output='json', quiet=True)

    import pandas as pd

    sites_df = pd.read_json(resources_json)

    display(
        sites_df[
            [
                "name",
                "hosts",
                "cpus",
                "cores_available",
                "ram_available",
                "tesla_t4_available",
                "rtx6000_available",
                "a30_available",
                "a40_available"
            ]
        ]
        .sort_values("cores_available", ascending=False)
    )

    print("✅ Resource check complete")

except Exception as e:
    print("Resource check error:", e)


# STEP 2: Cluster Parameters (Modify if needed)

# In[7]:


NUM_NODES = 3
SITES = "EDUKY"
SLICENAME = "MiniProject3A_Cluster"

INSTANCE_WORKER = "fabric.c8.m16.d100"
INSTANCE_MASTER = "fabric.c8.m16.d100"
IMAGE = "default_ubuntu_20"


# STEP 3: Create Slice Cluster

# In[8]:


try:
    slice_obj = fablib.new_slice(name=SLICENAME)

    node_names = [f"Node{i+1}" for i in range(NUM_NODES)]

    iface_list = []

    for idx in range(NUM_NODES):
        if idx == 0:
            node = slice_obj.add_node(
                name=node_names[idx],
                site=SITES,
                instance_type=INSTANCE_MASTER,
                image=IMAGE
            )
        else:
            node = slice_obj.add_node(
                name=node_names[idx],
                site=SITES,
                instance_type=INSTANCE_WORKER,
                image=IMAGE
            )

        iface = node.add_component(model='NIC_Basic', name=f"nic{idx+1}")
        iface_list.append(iface.get_interfaces()[0])

    print("✅ Cluster definition complete")

except Exception as e:
    print("Cluster definition error:", e)


# STEP 4: Submit Slice (Create Cluster)

# In[9]:


try:
    slice_obj.submit()
    print("✅ Slice submitted. Wait for provisioning...")
except Exception as e:
    print("Slice submission error:", e)


# STEP 5: Assign IPs + Enable Network Interface

# In[ ]:


from ipaddress import IPv4Network
import time

try:
    subnet = IPv4Network("192.168.1.0/24")
    available_ips = list(subnet)[1:]

    time.sleep(30)  # Give time for nodes to boot

    for node in slice_obj.get_nodes():
        iface = node.get_interface(network_name="cluster_network")
        if iface:
            ip_addr = available_ips.pop(0)
            iface.ip_addr_add(addr=ip_addr, subnet=subnet)
            node.execute(f"sudo ifconfig {iface.get_os_interface()} up")

    print("✅ Network interfaces configured")

except Exception as e:
    print("Network config error:", e)


# STEP 6: Connectivity Test (Very Important Check)

# In[12]:


try:
    node1 = slice_obj.get_node(name="Node1")
    stdout, stderr = node1.execute("ping -c 3 192.168.1.2")

    print("Ping Output:")
    print(stdout)
    print(stderr)

    print("✅ Cluster connectivity check complete")

except Exception as e:
    print("Connectivity test error:", e)


# In[13]:


print(slice_obj.get_state())


# In[14]:


node1.execute("wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh")
node1.execute("bash ~/miniconda.sh -b")


# In[15]:


node1.execute("export PATH=~/miniconda3/bin:$PATH")


# In[17]:


node1.execute("~/miniconda3/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main")
node1.execute("~/miniconda3/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r")


# In[18]:


node1.execute("~/miniconda3/bin/conda create -y -n fear_sim python=3.10")


# In[19]:


node1.execute("source ~/miniconda3/bin/activate fear_sim && pip install neuron bmtk mpich")


# In[20]:


node1.execute("source ~/miniconda3/bin/activate fear_sim && pip install neuron bmtk mpich --no-cache-dir")


# In[21]:


node1.execute("source ~/miniconda3/bin/activate fear_sim && python -m pip install neuron")


# In[25]:


node1.execute("source ~/miniconda3/bin/activate fear_sim && conda list")


# In[27]:


node1.execute(
"source ~/miniconda3/bin/activate fear_sim && python -m pip install neuron bmtk mpich --no-cache-dir"
)


# In[30]:


node1.execute("source ~/miniconda3/bin/activate fear_sim && python -c 'import sys; print(\"Python working\")'")


# In[31]:


node1.execute("git clone https://github.com/cyneuro/CI-BioEng-Class.git")


# In[32]:


node1.execute("cd CI-BioEng-Class && ls")


# In[ ]:




