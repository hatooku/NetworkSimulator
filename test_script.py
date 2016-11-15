from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test0.json")
ns.run(verbose=False)

ns.data_metrics.plot_flow_rate()
ns.data_metrics.plot_link_rate()
ns.data_metrics.plot_packet_loss()