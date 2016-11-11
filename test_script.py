from networksimulator import NetworkSimulator

ns = NetworkSimulator()
ns.populate("test1.json")
ns.run()

ns.data_metrics.plot_buffer_occupancy()