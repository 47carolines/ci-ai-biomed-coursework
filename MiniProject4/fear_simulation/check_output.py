import numpy as np
from bmtk.utils.reports.spike_trains import SpikeTrains

# Load spike trains
spikes = SpikeTrains.load(
    'output/spikes.h5',
    population='PING-Assembly'
)

# Get spike times for the first cell
times = np.sort(spikes.get_times(node_id=0))

if len(times) < 2:
    firing_rate = 0.0
else:
    ISI = np.diff(times)  # inter-spike intervals in ms
    firing_rate = 1000 / np.mean(ISI)  # Hz

print(firing_rate)