from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test2.json")
ns.run(verbose=False)

ns.data_metrics.plot_flow_packet_delay()
ns.data_metrics.plot_link_rate()
ns.data_metrics.plot_buffer_occupancy()
ns.data_metrics.plot_flow_rate()