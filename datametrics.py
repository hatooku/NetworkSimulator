from matplotlib import pyplot as plt
import numpy as np

from constants import *

class DataMetrics(object):
    """A class that holds all statistical measurements generated by the
    network simulation.

    Attributes:
        buffer_occupancy (dict): holds buffer occupancy data for each link.
            The key is the link_id and the value is an array of
            (time, buffer_occupancy) tuples.
        packet_loss (dict): holds packet loss data for each link.
            The key is the link_id and the value is an array of
            (time, packet_loss) tuples.
        link_rate (dict): holds link rate data for each link.
            The key is the link_id and the value is an array of
            (time, amount of data sent) tuples.
        flow_rate (dict): holds flow rate data for each flow.
            The key is the flow_id and the value is an array of
            (time, amount of data sent) tuples.
        window_size (dict): holds window size data for each flow.
            The key is the flow_id and the value is an array of
            (time, window size) tuples.
        flow_packet_delay (dict): holds roundtrip time data for each flow
            The key is the flow_id and the value is an array of
            (time of acknowledgement, roundtrip time) tuples.
        flow_packet_sent_time (dict): holds data on when each packet was sent,
            to be used for calculating the roundtrip time. The key is the
            (flow_id, packet_id) and the value is the sent time.

    """

    def __init__(self):
        self.buffer_occupancy = {}
        self.packet_loss = {}
        self.link_rate = {}
        self.flow_rate = {}
        self.window_size = {}
        self.flow_packet_delay = {}
        self.flow_packet_sent_time = {}

    def update_buffer_occupancy(self, link_id, buffer_occupancy, time):
        """Add a buffer occupancy data point, or modify a previously added
        point.

        Args:
            link_id (str): the id of the link with the buffer occupancy.
            buffer_occupancy (int): the buffer occupancy of the link in bits.
            time (float): the time of this data point.

        """
        prev_buffer_occupancy = 0
        if link_id not in self.buffer_occupancy:
            self.buffer_occupancy[link_id] = []
        # If there is a previous data point with the same time, update
        # the point.
        elif self.buffer_occupancy[link_id][-1][0] == time:
            prev_buffer_occupancy = self.buffer_occupancy[link_id][-1][1]
            self.buffer_occupancy[link_id].pop()
        data_point = (time, prev_buffer_occupancy + buffer_occupancy)
        self.buffer_occupancy[link_id].append(data_point)

    def update_packet_loss(self, link_id, time):
        """Add a packet loss data point, or modify a previously added point.

        Args:
            link_id (str): the id of the link with the packet loss.
            time (float): the time of this data point.

        """
        prev_dropped_packets = 0
        if link_id not in self.packet_loss:
            self.packet_loss[link_id] = []
        # If there is a previous data point with the same time, update
        # the point.
        elif self.packet_loss[link_id][-1][0] == time:
            prev_dropped_packets = self.packet_loss[link_id][-1][1]
            self.packet_loss[link_id].pop()
        data_point = (time, prev_dropped_packets + 1)
        self.packet_loss[link_id].append(data_point)

    def update_link_rate(self, link_id, amt_sent, time):
        """Add a link rate data point, or modify a previously added point.

        Args:
            link_id (str): the id of the link for this data point.
            amt_sent (float): the amount of data sent by the link in bits.
            time (float): the time of this data point.

        """
        prev_amt_sent = 0
        if link_id not in self.link_rate:
            self.link_rate[link_id] = []
        # If there is a previous data point with the same time, update
        # the point.
        elif self.link_rate[link_id][-1][0] == time:
            prev_amt_sent = self.link_rate[link_id][-1][1]
            self.link_rate[link_id].pop()
        data_point = (time, prev_amt_sent + amt_sent)
        self.link_rate[link_id].append(data_point)

    def update_flow_rate(self, flow_id, amt_sent, time):
        """Add a flow rate data point, or modify a previously added point.

        Args:
            flow_id (str): the id of the flow for the data point.
            amt_sent (float): the amount of data sent by the flow in bits.
            time (float): the time of this data point.

        """
        prev_amt_sent = 0
        if flow_id not in self.flow_rate:
            self.flow_rate[flow_id] = []
        # If there is a previous data point with the same time, update
        # the point.
        elif self.flow_rate[flow_id][-1][0] == time:
            prev_amt_sent = self.flow_rate[flow_id][-1][1]
            self.flow_rate[flow_id].pop()
        data_point = (time, prev_amt_sent + amt_sent)
        self.flow_rate[flow_id].append(data_point)

    def update_window_size(self, flow_id, window_size, time):
        """Add a window size data point, or modify a previously added point.

        Args:
            flow_id (str): the id of the flow for the data point.
            window_size (int): the window size of the flow at the given time.
            time (float): the time of this data point.

        """
        prev_window_size = 0
        if flow_id not in self.window_size:
            self.window_size[flow_id] = []
        # If there is a previous data point with the same time, update
        # the point.
        elif self.window_size[flow_id][-1][0] == time:
            prev_window_size = self.window_size[flow_id][-1][1]
            self.window_size[flow_id].pop()
        data_point = (time, prev_window_size + window_size)
        self.window_size[flow_id].append(data_point)

    def update_packet_send_time(self, flow_id, packet_id, time):
        """Record the most recent time a packet was sent, for use in
        calculating the roundtrip time.

        Args:
            flow_id (str): the id of the flow that the packet belongs to.
            packet_id (int): the id of the packet being sent.
            time (float): the time the packet was last sent.

        """
        self.flow_packet_sent_time[(flow_id, packet_id)] = time

    def update_packet_ack_time(self, flow_id, packet_id, time):
        """Records the acknowledgement of a packet, for use in
        calculating the roundtrip time.

        Args:
            flow_id (str): the id of the flow that the packet belongs to.
            packet_id (int): the id of the packet being sent.
            time (float): the time the packet was acknowledged.

        """
        if (flow_id, packet_id) not in self.flow_packet_sent_time:
            raise Exception("Packet send time not set for packet %s "
                            "in flow %s" % (packet_id, flow_id))
        rtt = time - self.flow_packet_sent_time[(flow_id, packet_id)]
        self._update_flow_packet_delay(flow_id, rtt, time)

    def _update_flow_packet_delay(self, flow_id, packet_delay, time):
        """Records the roundtrip time for a packet in a flow.

        Args:
            flow_id (str): the id of the flow that the packet belongs to.
            packet_delay (int): the roundtrip time of the packet.
            time (float): the time the packet was acknowledged.

        """
        if flow_id not in self.flow_packet_delay:
            self.flow_packet_delay[flow_id] = []
        data_point = (time, packet_delay)
        self.flow_packet_delay[flow_id].append(data_point)

    def plot_buffer_occupancy(self, links=None):
        legend_labels = []
        for link_id in self.buffer_occupancy:
            if links is None or link_id in links:
                all_data = np.array(self.buffer_occupancy[link_id])
                if len(all_data) > 0:
                    time, data = np.array(zip(*all_data))
                    avg_time, avg_data = self.window_average(time, data)
                    plt.plot(avg_time, avg_data, '-')
                    legend_labels.append(link_id)
                    
        plt.legend(legend_labels)
        plt.xlabel('time (s)')
        plt.ylabel('buffer occupancy (pkts)')
        plt.title("Buffer Occupancy")
        plt.show()

    def plot_flow_rate(self, flows=None):
        legend_labels = []
        for flow_id in self.flow_rate:
            if flows is None or flow_id in flows:
                all_data = np.array(self.flow_rate[flow_id])
                if len(all_data) > 0:
                    time, data = np.array(zip(*all_data))
                    avg_time, avg_rate = self.window_rate(time, data)
                    avg_rate = np.around(avg_rate, 2)
                    plt.plot(avg_time, avg_rate * BIT_TO_MEGABIT, '-')
                    legend_labels.append(flow_id)
                    
        plt.legend(legend_labels)
        plt.xlabel('time (s)')
        plt.ylabel('flow rate (Mbps)')
        plt.title("Flow Rate")
        plt.show()

    def plot_link_rate(self, links=None):
        legend_labels = []
        for link_id in self.link_rate:
            if links is None or link_id in links:
                all_data = np.array(self.link_rate[link_id])

                if len(all_data) > 0:
                    time, data = np.array(zip(*all_data))
                   
                    avg_time, avg_rate = self.window_rate(time, data)
                    avg_rate = np.around(avg_rate, 2)
                    plt.plot(avg_time, avg_rate * BIT_TO_MEGABIT, '-')
                    legend_labels.append(link_id)
                    
        plt.legend(legend_labels)
        plt.xlabel('time (s)')
        plt.ylabel('link rate (Mbps)')
        plt.title("Link Rate")
        plt.show()

    def plot_packet_loss(self, links=None):
        legend_labels = []
        for link_id in self.packet_loss:
            if links is None or link_id in links:
                all_data = np.array(self.packet_loss[link_id])
                if len(all_data) > 0:
                    time, data = np.array(zip(*all_data))
                    avg_time, avg_data = self.window_sum(time, data, 100)
                    plt.plot(avg_time, avg_data, '-')
                    legend_labels.append(link_id)
                    
        plt.legend(legend_labels)
        plt.xlabel('Time (s)')
        plt.ylabel('Packet loss (pkts)')
        plt.title("Packet loss")
        plt.show()

    def plot_flow_packet_delay(self, flows=None):
        legend_labels = []
        for flow_id in self.flow_rate:
            if flows is None or flow_id in links:
                all_data = np.array(self.flow_packet_delay[flow_id])
                if len(all_data) > 0:
                    time, data = np.array(zip(*all_data))
                    avg_time, avg_data = self.window_average(time, data)
                    plt.plot(avg_time, avg_data * S_TO_MS, '-')
                    legend_labels.append(flow_id)
                    
        plt.legend(legend_labels)
        plt.xlabel('time (s)')
        plt.ylabel('packet delay (ms)')
        plt.title("Flow Packet Delay")
        plt.show()

    def window_average(self, time, data, window_size=DEFAULT_WINDOW_SIZE):
        # leave out last few elements that don't fit into a full window
        end = window_size * int(len(data)/window_size)
        reshaped_time = time[:end].reshape(-1, window_size)
        reshaped_data = data[:end].reshape(-1, window_size)
        avg_time = np.mean(reshaped_time, axis=1)
        avg_data = np.mean(reshaped_data, axis=1)
        return avg_time, avg_data

    def window_sum(self, time, data, window_size=DEFAULT_WINDOW_SIZE):
        # leave out last few elements that don't fit into a full window
        end = window_size * int(len(data)/window_size)
        reshaped_time = time[:end].reshape(-1, window_size)
        reshaped_data = data[:end].reshape(-1, window_size)
        avg_time = np.mean(reshaped_time, axis=1)
        window_data = np.sum(reshaped_data, axis=1)
        return avg_time, window_data

    def window_rate(self, time, data, window_size=DEFAULT_WINDOW_SIZE):
        # leave out last few elements that don't fit into a full window

        # if there are less than window_size points, window size is set to 2
        if len(data) < window_size: 
         window_size = 2
        end = window_size * int(len(data)/window_size)
        reshaped_time = time[:end].reshape(-1, window_size)
        reshaped_data = data[:end].reshape(-1, window_size)

        sum_data = np.sum(reshaped_data, axis=1)
        delta_t = np.apply_along_axis(lambda t: t[-1] - t[0], 1, reshaped_time)
        avg_rate = sum_data * 1.0 / delta_t
        avg_time = np.mean(reshaped_time, axis=1)
        return avg_time, avg_rate
