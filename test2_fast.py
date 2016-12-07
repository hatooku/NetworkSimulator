from src import *

ns = NetworkSimulator()
ns.populate("network_descriptions/test2_fast.json")
ns.run(verbose=False)

ns.data_metrics.plot_link_rate(["L1", "L2", "L3"], window_size=0.2)
ns.data_metrics.plot_buffer_occupancy(["L1", "L2", "L3"])
ns.data_metrics.plot_packet_loss(["L1", "L2", "L3"])
ns.data_metrics.plot_flow_rate(window_size=0.2)
ns.data_metrics.plot_flow_window_size(window_size=0.1, sliding_window=5)
ns.data_metrics.plot_flow_packet_delay(window_size=0.05)
