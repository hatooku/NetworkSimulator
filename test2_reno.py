from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test2_reno.json")
ns.run(verbose=False)

ns.data_metrics.plot_link_rate(["L1", "L2", "L3"])
ns.data_metrics.plot_buffer_occupancy(["L1", "L2", "L3"])
ns.data_metrics.plot_packet_loss(["L1", "L2", "L3"])
ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_flow_window_size()
ns.data_metrics.plot_flow_packet_delay(window_size=0.05)
