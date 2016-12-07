from src import *

ns = NetworkSimulator()
ns.populate("network_descriptions/test0_reno.json")
ns.run(verbose=False)

ns.data_metrics.plot_link_rate()
ns.data_metrics.plot_buffer_occupancy()
ns.data_metrics.plot_packet_loss()
ns.data_metrics.plot_flow_rate(window_size=0.2, sliding_window=10)
ns.data_metrics.plot_flow_window_size()
ns.data_metrics.plot_flow_packet_delay()
