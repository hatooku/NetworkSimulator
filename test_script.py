from networksimulator import NetworkSimulator


ns = NetworkSimulator()
ns.populate("test0.json")
ns.run(verbose=True)

ns.data_metrics.plot_flow_packet_delay()
ns.data_metrics.plot_link_rate(["L2", "L4", "L5", "L0"])
ns.data_metrics.plot_buffer_occupancy()
ns.data_metrics.plot_flow_rate()