import numpy as np
from bmtk.utils.reports.spike_trains import SpikeTrains

spikes = SpikeTrains.load(
    'output/spikes.h5',
    population='PING-Assembly'
)

ISI = np.diff(np.sort(spikes.get_times(node_id=0)))

firing_rate = 1000 / np.mean(ISI)

print(firing_rate)