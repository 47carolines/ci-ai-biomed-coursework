import numpy as np
from bmtk.utils.reports.spike_trains import SpikeTrains

# Load spikes from the simulation
spikes = SpikeTrains.load('output/spikes.h5', population='PING-Assembly')

# Get spike times for the first neuron
times = np.sort(spikes.get_times(node_id=0))

# Compute inter-spike intervals (ISI)
if len(times) < 2:
    firing_rate = 0.0  # Not enough spikes to compute rate
else:
    ISI = np.diff(times)  # in ms
    mean_ISI = np.mean(ISI)
    if mean_ISI == 0 or np.isnan(mean_ISI):
        firing_rate = 0.0
    else:
        firing_rate = 1000 / mean_ISI  # Convert to Hz

print(firing_rate)