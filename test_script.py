from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test1.json")
ns.run(verbose=True)

#ns.data_metrics.plot_flow_window_size()

ns.data_metrics.plot_flow_packet_delay()
ns.data_metrics.plot_link_rate(links=['L0', 'L1', 'L2'])
ns.data_metrics.plot_buffer_occupancy(links=['L0', 'L1', 'L2'])
ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_packet_loss()