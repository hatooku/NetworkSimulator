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
        received_packets (list): The list of packets that have been received and
            acknowledged.  It is a list, as it should be able to have
            duplicates
        sent_packets (list): The list of packets that have been sent out.
            It is a list, as it should be able to have duplicates
        timed_out_packets (set): The list of packets timed out before acknowledgement
        num_packets_sent (float): Number of packets that have been sent through
            the flow
        num_packets (float):  Number of packets to be sent through the flow
        window_size (float): The size of the window.  Initially 1 for TCP Reno
        ssthreshold (float): Indicates available capacity of the network,
            adjusted with each packet loss

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time,
        window_size=1):
        Flow.__init__(self, ns, flow_id, src, dest, data_amount, start_time,
            window_size)
        self.unacknowledged_packets = set()
        self.received_packets = []
        self.sent_packets = []
        self.timed_out_packets = set()
        self.num_packets_sent = 0
        self.num_packets = int(math.ceil(data_amount/DATA_PACKET_SIZE))
        self.ssthreshold = 10

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
        if self.window_size <= self.ssthreshold:
            self.window_size += 1.0
        else:
            self.window_size += 1.0 / self.window_size

    def update_loss_window_size(self, lost_packet_id, delay=0.0):
        """Method that updates window size, and is called after a packet loss
        occurs.  Sets threshold to half of current window size, retransmits
        lost packet, and begins slow_start again

        """

        self.ssthreshold = self.window_size / 2.0
        self.window_size = 1.0
        self.slow_start = True

        self.create_packet(lost_packet_id, delay)

    def find_unreceived_packet(self):
        current_id = self.received_packets[0]
        for x in self.received_packets[1:]:
            if current_id + 1 < x:
                return current_id
            current_id = x
        return None

    def send_packets(self, delay=0.0):
        """Method sends as many packets as possible, triggering the
        create_packet function.  When a packet is lost, the TCP Reno congestion
        control will be enforced.  A packet is deemed lost when if times out,
        when the received packet set has a gap between received packets, or
        after three duplicate ACKS (avoiding having to wait for timeout).

        Note: The commented out section is the check for the gap between
        received packet.  It was taken out temporarily because it was really
        slowing things down

        delay (float): delay until sending packets. Should only be used for
            initial send.
        """
        while len(self.unacknowledged_packets) < self.window_size:
            if (self.sent_packets.count(self.sent_packets[-1:]) >= 3):
                self.update_loss_window_size(packet_id, delay)
            elif len(self.timed_out_packets) > 0:
                packet_id = min(self.timed_out_packets)
                self.update_loss_window_size(packet_id, delay)
                self.timed_out_packets.remove(packet_id)
            #elif (not all(self.received_packets[i] + 1 == self.received_packets[i + 1] for i in range(0, len(self.received_packets) - 1))):
            #    if self.find_unreceived_packet():
            #        self.update_loss_window_size(self.find_unreceived_packet(), delay)
            elif self.num_packets_sent < self.num_packets:
                self.create_packet(self.num_packets_sent, delay)
                self.num_packets_sent += 1
            else:
                break

    def create_packet(self, packet_id, delay=0.0):
        """Method creates packet and then adds them to event queue to be sent
        to the host, and adds a timing event to ensure that they are resent if
        unacknowledged.

        Args:
            packet_id (int): Unique id identifying the packet
            delay (float): delay until sending packet. Should only be used for
                initial send.

        """
        new_packet = DataPacket(packet_id, self.src.node_id,
            self.dest.node_id, self.flow_id)


        self.unacknowledged_packets.add(new_packet.packet_id)

        # Adding events to queues
        event1 = lambda: self.src.send_packet(new_packet)
        event1_message = "flow.create_packet: Flow" + str(self.flow_id) + \
            ": made data packet " + str(new_packet.packet_id)
        self.ns.add_event(event1, event1_message, delay=delay)

        event2 = lambda: self.time_out(new_packet.packet_id)
        event2_message = "flow.create_packet: Adding to time_out_packets, packet " + \
            str(new_packet.packet_id)
        self.ns.add_event(event2, event2_message, delay=ACK_DELAY + delay)

        # Adding packet to sent packets list
        self.sent_packets.append(new_packet.packet_id)

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
            self.received_packets.append(packet.packet_id)
            self.update_ack_window_size()
            self.update_flow(packet)
