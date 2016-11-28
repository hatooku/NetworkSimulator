import sys
from packet import Packet, DataPacket, RoutingPacket, AcknowledgementPacket
from constants import *
import math

class Flow(object):
    """A flow class that represents active connections between
    hosts and routers.  Implements TCP tahoe congestion control.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (string): Unique id identifying the flow
        src (Node): The flow's source node id
        dest (Node): The flow's destination node id
        data_amount (float): Data capacity of the flow (bits)
        start_time (float): Start time in seconds
        unacknowledged_packets (set): The list of packets with no acknowledgement
        first_unacknowledged (float): Id of first packet that hasn't been acknowledged
        num_packets (float):  Number of packets to be sent through the flow
        window_size (float): The size of the window
        duplicate_counter (int): Count number of times a duplicate packet is
            received
        canceled_timeouts (list): Contains packet time outs that need to be
            cancelled
        ssthreshold (float): The slow-start threshold
        fast_recovery (bool): Indicates whether or not the flow has entered
            fast recovery mode

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount
        self.start_time = start_time
        self.unacknowledged_packets = set()
        self.first_unacknowledged = 0.0
        self.num_packets = int(math.ceil(data_amount/DATA_PACKET_SIZE))
        self.window_size = 1.0
        self.duplicate_counter = 0
        self.canceled_timeouts = []
        self.ssthreshold = sys.maxint

        # Destination
        self.unreceived_packets = [i for i in range(self.num_packets)]

        self.send_packets(self.start_time)

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

    def check_flow_completion(self):
        """Method that checks if all packets have been acknowledged and
        updates the NetworkSimulator object accordingly.

        """

        if self.first_unacknowledged >= self.num_packets:
            self.ns.decrement_active_flows()

    def slow_start(self):
        return self.window_size < self.ssthreshold

    def update_ack_window_size(self):
        """Method that updates window size when a packet is acknowledged.
        If the window size has reached the threshold, congestion avoidance will
        be switched on.
        """

        if self.slow_start():
            self.window_size += 1.0
            self.ns.record_window_size(self.flow_id, self.window_size)
        else:
            self.window_size += 1.0 / math.floor(self.window_size)
            self.ns.record_window_size(self.flow_id, self.window_size)

    def update_timeout_window_size(self):
        """Method that updates window size after a timeout.

        Sets threshold to half of current window size and retransmits lost packet.
        
        """

        self.ssthreshold = self.window_size / 2.0
        self.window_size = 1.0
        self.ns.record_window_size(self.flow_id, self.window_size)

    def update_fast_retransmit_window_size(self):
        """Method that updates window size during fast retransmit.

        Sets threshold to half of current window size and retransmits lost packet.
        
        """

        self.ssthreshold = self.window_size / 2.0
        self.window_size = 1.0
        self.ns.record_window_size(self.flow_id, self.window_size)

    def clean_unacknowledged(self):
        self.unacknowledged_packets = \
            {packet_id for packet_id in self.unacknowledged_packets \
            if packet_id >= self.first_unacknowledged}

    def update_flow(self, a_packet):
        """Upon receiving an acknowledgement packet, updates the flow's
        attributes

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """

        if a_packet.packet_id > self.first_unacknowledged:
            self.update_ack_window_size()
            self.first_unacknowledged = a_packet.packet_id
            self.duplicate_counter = 0
            self.clean_unacknowledged()
            self.check_flow_completion()
            self.send_packets()
        elif a_packet.packet_id == self.first_unacknowledged:
            self.duplicate_counter += 1
            self.send_packets()

            if self.duplicate_counter == 3:
                self.update_fast_retransmit_window_size()
                self.unacknowledged_packets.remove(self.first_unacknowledged)
                self.create_packet(self.first_unacknowledged)
                self.canceled_timeouts.append(self.first_unacknowledged)

    def time_out(self, packet_id):
        """Method where, if sent packet is still unacknowledged after a period
        of time, packet is considered lost.  Packet is then resent and window
        size is updated.

        Args:
            packet_id (int): packet_id of packet being added to timed_out_packets

        """
        if packet_id in self.canceled_timeouts:
            self.canceled_timeouts.remove(packet_id)
        elif packet_id in self.unacknowledged_packets:
            self.update_timeout_window_size()
            self.unacknowledged_packets.clear()
            self.send_packets()

    def send_packets(self, delay=0.0):
        """Method sends as many packets as possible, triggering the
        create_packet function.

        delay (float): delay until sending packets. Should only be used for
            initial send.
        """
        cur = self.first_unacknowledged
        while len(self.unacknowledged_packets) < int(self.window_size) and cur < self.num_packets:
            if cur not in self.unacknowledged_packets:
                self.create_packet(cur, delay)
            cur += 1

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


    def make_acknowledgement_packet(self, src, dest):
        """Method makes the AcknowledgementPacket and triggers the send_packet
        method for the host if applicable

        Args:
            src (Node): The packet's source node
            dest (Node): The packet's destination node

        """

        if len(self.unreceived_packets) > 0:
            next_expected = self.unreceived_packets[0]
        else:
            next_expected = self.num_packets
        new_packet = AcknowledgementPacket(next_expected, src, dest, self.flow_id)

        event = lambda: self.src.send_packet(new_packet)
        event_message = "flow.make_acknowledgement_packet(): Flow" + \
            str(self.flow_id) + ": made acknowledgment packet " + str(next_expected)
        self.ns.add_event(event, event_message)

    def receive_packet(self, packet):
        """Method receives a given packet.  If it's a data packet, send an
        acknowledgement packet.  If it's an acknowledgement packet, update_flow

        args:
            packet (Packet): packet object being received

        """
        if isinstance(packet, DataPacket):
            assert packet.src == self.src.node_id
            assert packet.dest == self.dest.node_id
            self.acknowledge(packet)
        elif isinstance(packet, AcknowledgementPacket):
            assert packet.src == self.dest.node_id
            assert packet.dest == self.src.node_id
            self.update_flow(packet)

    def acknowledge(self, packet):
        """Method that triggers the send_packet function for the host if
        applicable by sending the acknowledgement packet

        Args:
            packet (Packet): The packet attempting to be acknowledged

        """
        if packet.packet_id in self.unreceived_packets:
            self.unreceived_packets.remove(packet.packet_id)

        self.make_acknowledgement_packet(packet.dest, packet.src)
