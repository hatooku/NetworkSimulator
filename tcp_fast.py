from flow import flow

class tcp_flow(flow):
	def __init__(self, ns, flow_id, src, dest, data_amount, start_time, gamma, alpha):
		Flow.__init__(self, ns, flow_id, src, dest, data_amount)
		self.window_size = 1
		self._gamma = gamma
		self.alpha = alpha