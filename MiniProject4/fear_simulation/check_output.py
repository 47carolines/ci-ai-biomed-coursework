import numpy as np
from bmtk.utils.reports.spike_trains import SpikeTrains

# Load spikes from the simulation
spikes = SpikeTrains.load('output/spikes.h5', population='PING-Assembly')

# Initialize list to collect individual neuron firing rates
firing_rates = []

# Iterate over all neurons in the population
for node_id in spikes.node_ids:
    times = np.sort(spikes.get_times(node_id=node_id))
    
    if len(times) < 2:
        continue  # Not enough spikes to compute rate
    ISI = np.diff(times)  # inter-spike intervals in ms
    mean_ISI = np.mean(ISI)
    if mean_ISI > 0 and not np.isnan(mean_ISI):
        firing_rates.append(1000 / mean_ISI)  # Convert to Hz

# Compute network-wide mean firing rate
if firing_rates:
    network_firing_rate = np.mean(firing_rates)
else:
    network_firing_rate = 0.0

print(network_firing_rate)