from flow import Flow
from constants import *

class FAST_TCP(Flow):
    """A flow class that represents active connections between
    hosts and routers.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (string): Unique id identifying the flow
        src (Node): The flow's source node id
        dest (Node): The flow's destination node id
        data_amount (float): Data capacity of the flow (bits)

        gamma (float): A constant used to update the window size
        alpha (float): A constant used to update the window size
        last_rtt (float): The roundtrip time of the last acknowledged packet
        base_rtt (float): The shortest roundtrip time of all acknowledge packets

    Inherited Attributes:
        start_time (float): Start time in seconds
        unacknowledged_packets (set): The list of packets with no 
            acknowledgement
        num_packets (float):  Number of packets to be sent through the flow
        window_size (float): The size of the window

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time):
        Flow.__init__(self, ns, flow_id, src, dest, data_amount, start_time)
        self._gamma = FAST_GAMMA
        self._alpha = FAST_ALPHA
        self.last_rtt = float('inf')
        self.base_rtt = float('inf')

        self.schedule_next_update()

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, gamma):
        raise AttributeError("Cannot modify the constant gamma.")

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        raise AttributeError("Cannot modify the constant alpha.")

    def update_flow(self, a_packet):
        """Upon receiving an acknowledgement packet, updates the flow's
        attributes

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """
        # Calculate the roundtrip time of the packet being acknowledged.
        rtt = self.ns.cur_time - a_packet.timestamp
        self.last_rtt = rtt
        self.base_rtt = min(self.base_rtt, rtt)
        self.ns.record_packet_rtt_time(self.flow_id, rtt)

        if a_packet.packet_id > self.first_unacknowledged:
            self.first_unacknowledged = a_packet.packet_id
            self.duplicate_counter = 0
            self.clean_unacknowledged()
            self.check_flow_completion()
            self.send_packets()
        elif a_packet.packet_id == self.first_unacknowledged:
            self.duplicate_ack()

            if self.duplicate_counter == 3:
                self.unacknowledged_packets.remove(self.first_unacknowledged)
                self.create_packet(self.first_unacknowledged)
                self.canceled_timeouts.append(self.first_unacknowledged)

    def time_out(self, packet_id):
        if packet_id in self.canceled_timeouts:
            self.canceled_timeouts.remove(packet_id)
        if packet_id in self.unacknowledged_packets:
            self.unacknowledged_packets.remove(packet_id)
            assert(len(self.unacknowledged_packets) + 1 == int(self.window_size))
            self.send_packets()

    def update_window_size(self):
        """Updates the window size periodically according to the FAST-TCP 
        algorithm.

        """
       
        if self.last_rtt < float('inf'):
            self.window_size = min(2 * self.window_size, \
                (1 - self.gamma) * self.window_size + \
                self.gamma * (self.base_rtt / self.last_rtt * self.window_size \
                    + self.alpha))

            self.send_packets()
            self.ns.record_window_size(self.flow_id, self.window_size)

        self.schedule_next_update()

    def schedule_next_update(self):
        """Schedules the next window size update in the network simulator."""

        next_update_event = lambda: self.update_window_size()
        next_description = \
            "FAST_TCP.update_window_size on flow %s" % self.flow_id
        self.ns.add_event(next_update_event,
            next_description,
            delay=FAST_WINDOW_UPDATE_PERIOD)