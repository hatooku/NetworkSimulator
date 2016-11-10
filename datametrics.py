class DataMetrics(object):

    def __init__(self):
        self.buffer_occupancy = {}
        self.packet_loss = {}
        self.link_rate = {}
        self.flow_rate = {}
        self.window_size = {}
        self.flow_packet_delay = {}
        self.flow_packet_sent_time = {}

    def update_buffer_occupancy(self, link_id, buffer_occupancy, time):
        if link_id not in self.buffer_occupancy:
            self.buffer_occupancy[link_id] = []
        data_point = (time, buffer_occupancy)
        self.buffer_occupancy[link_id].append(data_point)

    def update_packet_loss(self, link_id, num_packets_lost, time):
        if link_id not in self.packet_loss:
            self.packet_loss[link_id] = []
        data_point = (time, num_packets_lost)
        self.packet_loss[link_id].append(data_point)

    def update_link_rate(self, link_id, amt_sent, time):
        if link_id not in self.link_rate:
            self.link_rate[link_id] = []
        data_point = (time, amt_sent)
        self.link_rate[link_id].append(data_point)

    def update_flow_rate(self, flow_id, amt_sent, time):
        if flow_id not in self.flow_rate:
            self.flow_rate[flow_id] = []
        data_point = (time, amt_sent)
        self.flow_rate[flow_id].append(data_point)

    def update_window_size(self, flow_id, window_size, time):
        if flow_id not in self.window_size:
            self.window_size[flow_id] = []
        data_point = (time, window_size)
        self.window_size[flow_id].append(data_point)

    def update_packet_send_time(self, flow_id, packet_id, time):
        if (flow_id, packet_id) in self.flow_packet_sent_time:
            raise Exception("Packet send time already set for packet %s "
                            "in flow %s" % (packet_id, flow_id))
        self.flow_packet_sent_time[(flow_id, packet_id)] = time

    def update_packet_ack_time(self, flow_id, packet_id, time):
        if (flow_id, packet_id) not in self.flow_packet_sent_time:
            raise Exception("Packet send time not set for packet %s "
                            "in flow %s" % (packet_id, flow_id))
        rtt = time - self.flow_packet_sent_time([flow_id, packet_id])
        self._update_flow_packet_delay(flow_id, rtt, time)

    def _update_flow_packet_delay(self, flow_id, packet_delay, time):
        if flow_id not in self.flow_packet_delay:
            self.flow_packet_delay = []
        data_point = (time, packet_delay)
        self.flow_packet_delay[flow_id] = data_point
