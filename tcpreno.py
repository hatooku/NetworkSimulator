import sys
from packet import Packet, DataPacket, RoutingPacket, AcknowledgementPacket
from flow import Flow
from constants import *
import math

class TcpReno(Flow):
    """A flow subclass that represents active connections between
    hosts and routers and employs TCP Reno congestion control.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (string): Unique id identifying the flow
        src (Node): The flow's source node id
        dest (Node): The flow's destination node id
        data_amount (float): Data capacity of the flow (bits)

        start_time (float): Start time in seconds
        unacknowledged_packets (set): The list of packets with no acknowledgement
        timed_out_packets (set): The list of packets timed out before acknowledgement
        num_packets_sent (float): Number of packets that have been sent through
            the flow
        num_packets (float):  Number of packets to be sent through the flow
        window_size (float): The size of the window.  Initially 1 for TCP Reno
        slow_start (bool): True value indicates if TCP reno is in it's
            slow_start phase.  False value indicates that it is in it's
            congestion avoidance phase
        ssthreshold (float): Indicates available capacity of the network,
            adjusted with each packet loss

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time,
        window_size=1):
        Flow.__init__(self, ns, flow_id, src, dest, data_amount, start_time,
            window_size)
        self.unacknowledged_packets = set()
        self.timed_out_packets = set()
        self.num_packets_sent = 0
        self.num_packets = int(math.ceil(data_amount/DATA_PACKET_SIZE))
        self.slow_start = True
        self.ssthreshold = ns.num_active_flows # Seems jank

        self.send_packets(start_time)

    @property
    def flow_id(self):
        return self._flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        raise AttributeError("Cannot modify id of a flow.")

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        raise AttributeError("Cannot modify a flow's source node id.")

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, dest):
        raise AttributeError("Cannot modify a flow's destination node id.")

    def update_ack_window_size(self):
        """Method that updates window size when a packet is acknowledged.
        If the window size has reached the threshold, congestion avoidance will
        be switched on.

        """
        if self.slow_start:
            self.window_size += 1.0
        else:
            self.window_size += 1.0 / self.window_size

        # Should this come before the above if condition?
        if self.window_size >= self.ssthreshold:
            self.slow_start = False

    def update_loss_window_size(self, lost_packet_id, delay=0.0):
        """Method that updates window size, and is called after a packet loss
        occurs.  Sets threshold to half of current window size, retransmits
        lost packet, and begins slow_start again

        """

        self.ssthreshold = self.window_size / 2.0
        self.window_size = 1.0
        self.slow_start = True

        self.create_packet(lost_packet_id, delay)

    def send_packets(self, delay=0.0):
        """Method sends as many packets as possible, triggering the
        create_packet function.  When packet is time out, calls TCP Reno
        congestion control to resize the threshold.

        delay (float): delay until sending packets. Should only be used for
            initial send.
        """
        while len(self.unacknowledged_packets) < self.window_size:
            if len(self.timed_out_packets) > 0:
                packet_id = min(self.timed_out_packets)
                self.update_loss_window_size(packet_id, delay)
                self.timed_out_packets.remove(packet_id)
            elif self.num_packets_sent < self.num_packets:
                self.create_packet(self.num_packets_sent, delay)
                self.num_packets_sent += 1
            else:
                break

    def receive_packet(self, packet):
        """Method receives a given packet.  If it's a data packet, send an
        acknowledgement packet.  If it's an acknowledgement packet, update_flow
        and window size

        args:
            packet (Packet): packet object being received

        """
        if isinstance(packet, DataPacket):
            self.acknowledge(packet)
        elif isinstance(packet, AcknowledgementPacket):
            self.update_ack_window_size()
            self.update_flow(packet)
