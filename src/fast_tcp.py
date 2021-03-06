from flow import Flow
from constants import *

class FAST_TCP(Flow):
    """A flow class that represents active connections between
    hosts and routers.

    Attributes: 
        gamma (float): A constant used to update the window size
        alpha (float): A constant used to update the window size
        last_rtt (float): The round trip time of the last acknowledged packet
        base_rtt (float): The shortest round trip time of all acknowledged
                           packets

    Inherited Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (string): Unique id identifying the flow
        src (Node): The flow's source node id
        dest (Node): The flow's destination node id
        data_amount (float): Data capacity of the flow (bits)
        start_time (float): Start time in seconds
        unacknowledged_packets (set): The list of packets with no 
            acknowledgement 
        first_unacknowledged (int): The packet id of the first unacknowledged
            packet (i.e., the next packet expected to be acknowledged)
        num_packets (float):  Number of packets to be sent through the flow
        window_size (float): The size of the window
        canceled_timeouts (list): Contains packet time outs that need to
            be canceled

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
        # Calculate the round trip time of the packet being acknowledged.
        rtt = self.ns.cur_time - a_packet.timestamp
        self.last_rtt = rtt
        self.base_rtt = min(self.base_rtt, rtt)
        self.ns.record_packet_rtt_time(self.flow_id, rtt)

        if a_packet.packet_id > self.first_unacknowledged:
            self.first_unacknowledged = a_packet.packet_id
            self.clean_unacknowledged()
            self.check_flow_completion()
            self.send_packets()

    def time_out(self, packet_id):
        """Method where, if sent packet is still unacknowledged after a period
        of time, packet is considered lost.  Packet is then resent.

        Args:
            packet_id (int): packet_id of packet checking if timed out.
                                    
        """
        if packet_id in self.canceled_timeouts:
            self.canceled_timeouts.remove(packet_id)
        elif packet_id in self.unacknowledged_packets:
            self.create_packet(packet_id)

    def update_window_size(self):
        """Updates the window size periodically according to the FAST-TCP 
        algorithm.

        """
        if self.last_rtt < float('inf'):
            self.window_size = min(2 * self.window_size, \
                (1 - self.gamma) * self.window_size + \
                self.gamma * (self.base_rtt / self.last_rtt * self.window_size \
                    + self.alpha))
            self.record_window_size()

        self.schedule_next_update()

    def schedule_next_update(self):
        """Schedules the next window size update in the network simulator."""

        next_update_event = lambda: self.update_window_size()
        next_description = \
            "FAST_TCP.update_window_size on flow %s" % self.flow_id
        self.ns.add_event(next_update_event,
            next_description,
            delay=FAST_WINDOW_UPDATE_PERIOD)