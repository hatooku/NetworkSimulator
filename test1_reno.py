from src import *

ns = NetworkSimulator()
ns.populate("network_descriptions/test1_reno.json")
ns.run(verbose=False)

ns.data_metrics.plot_link_rate(["L1", "L2"])
ns.data_metrics.plot_buffer_occupancy(["L1", "L2"], window_size=0.05)
ns.data_metrics.plot_packet_loss(["L1", "L2"])
ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_flow_window_size()
ns.data_metrics.plot_flow_packet_delay()
