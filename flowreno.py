import sys
from packet import Packet, DataPacket, RoutingPacket, AcknowledgementPacket
from constants import *
from flow import Flow
import math

class FlowReno(Flow):
    """A subclass of Flow that represents active connections between
    hosts and routers, and implements TCP Reno congestion control.

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
        fast_recovery (bool): Indicates whether or not the flow has entered
            fast recovery mode
        first_partial_ack (int): Packet id of the unacknowledged packet with the
            smallest id
        last_partial_ack (int): Packet id of the unacknowledged packet with the
            largest id

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time):
        self.fast_recovery = False
        Flow.__init__(self, ns, flow_id, src, dest, data_amount, start_time)

        self.first_partial_ack = -1
        self.last_partial_ack = -1

    def update_ack_window_size(self):
        """Updates window size when a packet is acknowledged.

        If the window size has reached the threshold, congestion avoidance will
        be switched on.

        """
        if self.fast_recovery:
            self.fast_recovery = False
            self.window_size = math.ceil(self.ssthreshold)
            self.duplicate_counter = 0
            self.record_window_size()
        else:
            Flow.update_ack_window_size(self)

    def update_timeout_window_size(self):
        """Updates window size, and recorded partial acknowledgement packet ids
        after a timeout.

        """
        Flow.update_timeout_window_size(self)
        self.fast_recovery = False
        self.first_partial_ack = -1
        self.last_partial_ack = -1

    def update_fast_retransmit_window_size(self):
        """Updates window size during fast retransmit. Sets threshold to half of
        current window size, turns on fast recovery, and records partial
        acknowledgement packets

        """
        assert(self.duplicate_counter == 3)

        self.ssthreshold = max(self.window_size / 2.0, 1)
        self.window_size = self.ssthreshold
        self.record_window_size()

        self.fast_recovery = True
        self.last_partial_ack = max(self.unacknowledged_packets)
        self.first_partial_ack = min(self.unacknowledged_packets)

    def update_flow(self, a_packet):
        """Upon receiving an acknowledgement packet, updates the flow's
        attributes. Also checks for duplicate acknowledgement packets, and flow
        completion.

        Args:
            a_packet (AcknowledgementPacket): Packet being sent back from host

        """
        rtt = self.ns.cur_time - a_packet.timestamp
        self.ns.record_packet_rtt_time(self.flow_id, rtt)

        if a_packet.packet_id > self.first_unacknowledged:
            self.first_unacknowledged = a_packet.packet_id
            if self.fast_recovery and \
                self.first_unacknowledged <= self.last_partial_ack:
                self.create_packet(self.first_unacknowledged)
                self.canceled_timeouts.append(self.first_unacknowledged)
                num_cleaned = self.clean_unacknowledged()
                self.duplicate_counter -= num_cleaned

            else:
                self.update_ack_window_size()
                self.clean_unacknowledged()

            self.check_flow_completion()
            self.send_packets()
        elif a_packet.packet_id == self.first_unacknowledged:
            self.duplicate_counter += 1
            self.send_packets()

            if not self.slow_start() and not self.fast_recovery and \
                self.duplicate_counter == 3:
                self.update_fast_retransmit_window_size()
                self.create_packet(self.first_unacknowledged)
                self.canceled_timeouts.append(self.first_unacknowledged)

    def get_effective_window_size(self):
        """Returns the current window size. If fast recovery is on, includes the
        addition of the current duplicate count.
        """
        effective_window_size = self.window_size
        if self.fast_recovery:
            effective_window_size += self.duplicate_counter
        return effective_window_size
