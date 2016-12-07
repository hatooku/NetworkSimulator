from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test1_fast.json")
ns.run(verbose=False)

ns.data_metrics.plot_link_rate(["L1", "L2"])
ns.data_metrics.plot_buffer_occupancy(["L1", "L2"], window_size=0.05)
ns.data_metrics.plot_packet_loss(["L1", "L2"])
ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_flow_window_size()
ns.data_metrics.plot_flow_packet_delay()
