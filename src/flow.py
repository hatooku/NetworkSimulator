import sys
from packet import Packet, DataPacket, RoutingPacket, AcknowledgementPacket
from constants import *
import math

class Flow(object):
    """A flow class that represents active connections between
    hosts and routers.  Implements TCP Tahoe congestion control.

    Attributes:
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
        duplicate_counter (int): Count number of times a duplicate packet is
            received
        canceled_timeouts (list): Contains packet time outs that need to
            be canceled
        ssthreshold (float): The slow-start threshold
        unreceived_packets (list): List of ids of packets that haven't been
            received yet

    """
    def __init__(self, ns, flow_id, src, dest, data_amount, start_time):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount
        self.start_time = start_time
        self.unacknowledged_packets = set()
        self.first_unacknowledged = 0
        self.num_packets = int(math.ceil(data_amount/DATA_PACKET_SIZE))
        self.window_size = 1.0
        self.duplicate_counter = 0
        self.canceled_timeouts = []
        self.ssthreshold = sys.maxint
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
        """Checks if all packets have been acknowledged and updates the 
        NetworkSimulator object accordingly.

        """
        if self.is_done():
            self.ns.decrement_active_flows(self.flow_id)

    def slow_start(self):
        """Returns true if the flow is in slow start phase, and
        false if it is not.

        """
        return self.window_size < self.ssthreshold

    def update_ack_window_size(self):
        """Updates window size when a packet is acknowledged.

        If the window size has reached the threshold, congestion avoidance will
        be switched on.

        """
        if self.slow_start():
            self.window_size += 1.0
        else:
            self.window_size += 1.0 / math.floor(self.window_size)

        self.duplicate_counter = 0
        self.record_window_size()

    def update_timeout_window_size(self):
        """After a timeout, sets the ssthreshold to half of the window size, 
        sets window size back to 1, and resets the duplicate counter.

        """
        self.ssthreshold = max(self.window_size / 2.0, 1)
        self.window_size = 1.0
        self.duplicate_counter = 0
        self.record_window_size()

    def update_fast_retransmit_window_size(self):
        """During fast retransmit, sets threshold to half of the window size, 
        and sets window size back to 1.

        """
        assert(self.duplicate_counter == 3)
        self.ssthreshold = max(self.window_size / 2.0, 1)
        self.window_size = 1.0
        self.record_window_size()

    def clean_unacknowledged(self):
        """Cleans up unacknowledged packet array by removing all packets with 
        ids preceding the first unacknowledged packet.

        Returns the number of packets removed.

        """
        prev_length = len(self.unacknowledged_packets)
        self.unacknowledged_packets = \
            {packet_id for packet_id in self.unacknowledged_packets \
            if packet_id >= self.first_unacknowledged}
        return prev_length - len(self.unacknowledged_packets)

    def update_flow(self, a_packet):
        """Upon receiving an acknowledgement packet, checks for flow completion,
        checks for duplicate acknowledgement packets, updates the flow's
        attributes accordingly, and sends more packets (if appropriate).

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """

        rtt = self.ns.cur_time - a_packet.timestamp
        self.ns.record_packet_rtt_time(self.flow_id, rtt)

        if a_packet.packet_id > self.first_unacknowledged:
            self.first_unacknowledged = a_packet.packet_id
            self.update_ack_window_size()
            self.clean_unacknowledged()
            self.check_flow_completion()
            self.send_packets()
        elif a_packet.packet_id == self.first_unacknowledged:
            self.duplicate_counter += 1
            self.send_packets()

            if not self.slow_start() and self.duplicate_counter == 3:
                self.update_fast_retransmit_window_size()
                self.create_packet(self.first_unacknowledged)
                self.canceled_timeouts.append(self.first_unacknowledged)

    def time_out(self, packet_id):
        """If sent packet is still unacknowledged after a period of time, packet
        is considered lost. Packet is then resent and window size is updated.

        Args:
            packet_id (int): packet_id of packet being added to 
                timed_out_packets

        """
        if packet_id in self.canceled_timeouts:
            self.canceled_timeouts.remove(packet_id)
        elif packet_id in self.unacknowledged_packets:
            self.update_timeout_window_size()
            self.unacknowledged_packets.clear()
            self.send_packets()

    def send_packets(self, delay=0.0):
        """Sends as many packets as possible, triggering the create_packet 
        function.

        delay (float): delay until sending packets. Should only be used for
            initial send.
        """
        cur = self.first_unacknowledged
        effective_window_size = self.get_effective_window_size()
        while len(self.unacknowledged_packets) < int(effective_window_size) \
            and  cur < self.num_packets:
            if cur not in self.unacknowledged_packets:
                self.create_packet(cur, delay)
            cur += 1

    def get_effective_window_size(self):
        return self.window_size

    def create_packet(self, packet_id, delay=0.0):
        """Creates packet and then adds it to event queue to be sent to the 
        host, along with a timing event to ensure that they are resent if
        unacknowledged.

        Args:
            packet_id (int): Unique id identifying the packet
            delay (float): delay until sending packet. Should only be used for
                initial send.

        """

        new_packet = DataPacket(packet_id, self.src.node_id,
            self.dest.node_id, self.flow_id, self.ns.cur_time + delay)

        self.unacknowledged_packets.add(new_packet.packet_id)

        event1 = lambda: self.src.send_packet(new_packet)
        event1_message = "flow.create_packet: Flow" + str(self.flow_id) + \
            ": made data packet " + str(new_packet.packet_id)
        self.ns.add_event(event1, event1_message, delay=delay)

        event2 = lambda: self.time_out(new_packet.packet_id)
        event2_message = "flow.create_packet: Adding to time_out_packets, packet " + \
            str(new_packet.packet_id)
        self.ns.add_event(event2, event2_message, delay=TIMEOUT_DELAY + delay)

    def make_acknowledgement_packet(self, timestamp):
        """Method makes the AcknowledgementPacket and triggers the send_packet
        method for the host if applicable.

        Args:
            timestamp (float): time the packet to be acknowledged was sent

        """
        if len(self.unreceived_packets) > 0:
            next_expected = self.unreceived_packets[0]
        else:
            next_expected = self.num_packets

        src = self.dest.node_id
        dest = self.src.node_id
        new_packet = AcknowledgementPacket(next_expected, src, dest, \
            self.flow_id, timestamp)

        event = lambda: self.dest.send_packet(new_packet)
        event_message = "flow.make_acknowledgement_packet(): Flow" + \
            str(self.flow_id) + ": made acknowledgment packet " + str(next_expected)
        self.ns.add_event(event, event_message)

    def receive_packet(self, packet):
        """Receives a given packet. If it's a data packet, sends an 
        acknowledgement packet. If it's an acknowledgement packet, updates the 
        flow.

        Args:
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
        """Triggers the send_packet function for the host if applicable by
        making and sending an acknowledgement packet.

        Args:
            packet (Packet): The packet attempting to be acknowledged

        """

        if packet.packet_id in self.unreceived_packets:
            self.unreceived_packets.remove(packet.packet_id)

        self.make_acknowledgement_packet(packet.timestamp)

    def is_done(self):
        """Checks if a flow is completed. If the first unacknowledged packet is
        after our number of packets sent, the flow is done.

        """
        return self.first_unacknowledged == self.num_packets

    def record_window_size(self):
        """Records the window size of the flow. Calls the network simulator to 
        record the window size (we only care to log the window size if the flow
        is not done yet).

        """
        if not self.is_done():
            self.ns.record_window_size(self.flow_id, self.window_size)
