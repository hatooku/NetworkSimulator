from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test0_fast.json")
ns.run(verbose=False)

ns.data_metrics.plot_link_rate()
ns.data_metrics.plot_buffer_occupancy()
ns.data_metrics.plot_packet_loss()
ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_flow_window_size()
ns.data_metrics.plot_flow_packet_delay()
