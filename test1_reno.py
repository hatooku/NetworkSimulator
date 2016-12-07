from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test1_reno.json")
ns.run(verbose=False)

ns.data_metrics.plot_flow_window_size(window_size=0.1, sliding_window=5)
ns.data_metrics.plot_flow_packet_delay()
ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_link_rate(["L1", "L2"])
ns.data_metrics.plot_buffer_occupancy(["L1", "L2"])
ns.data_metrics.plot_packet_loss(["L1", "L2"])
