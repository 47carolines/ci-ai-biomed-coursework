import os
import numpy as np
from bmtk.utils.reports.spike_trains import SpikeTrains

spikes_file = os.path.join(os.path.dirname(__file__), 'output', 'spikes.h5')

spikes = SpikeTrains.load(spikes_file, population='PING-Assembly')
times = np.sort(spikes.get_times(node_id=0))

if len(times) < 2:
    firing_rate = 0.0
else:
    ISI = np.diff(times)
    firing_rate = 1000 / np.mean(ISI)

print(firing_rate)