import sys
from packet import Packet, DataPacket, RoutingPacket, AcknowledgementPacket
from constants import *
from flow import Flow
import math

class FlowReno(Flow):
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
        self.fast_recovery = False
        Flow.__init__(self, ns, flow_id, src, dest, data_amount, start_time)

        self.first_partial_ack = -1
        self.last_partial_ack = -1

    def update_ack_window_size(self):
        """Method that updates window size when a packet is acknowledged.
        If the window size has reached the threshold, congestion avoidance will
        be switched on.

        """
        if self.fast_recovery:
            self.fast_recovery = False
            self.window_size = math.ceil(self.ssthreshold)
            self.duplicate_counter = 0
        elif self.slow_start():
            self.window_size += 1.0
        else:
            self.window_size += 1.0 / math.floor(self.window_size)
        self.ns.record_window_size(self.flow_id, self.window_size)

    def update_timeout_window_size(self):
        """Method that updates window size after a timeout.

        Sets threshold to half of current window size and retransmits lost packet.

        """

        Flow.update_timeout_window_size(self)
        self.fast_recovery = False
        self.first_partial_ack = -1
        self.last_partial_ack = -1

    def update_flow(self, a_packet):
        """Upon receiving an acknowledgement packet, updates the flow's
        attributes

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """

        rtt = self.ns.cur_time - a_packet.timestamp
        self.ns.record_packet_rtt_time(self.flow_id, rtt)

        if a_packet.packet_id > self.first_unacknowledged:
            self.first_unacknowledged = a_packet.packet_id

            if self.fast_recovery and self.first_unacknowledged <= self.last_partial_ack:
                self.create_packet(self.first_unacknowledged)
                num_cleaned = self.clean_unacknowledged()
                self.duplicate_counter -= num_cleaned
            else:
                self.update_ack_window_size()
                self.clean_unacknowledged()
            
            self.check_flow_completion()
            self.send_packets()
        elif a_packet.packet_id == self.first_unacknowledged:
            if not self.fast_recovery or self.first_unacknowledged == self.first_partial_ack:
                self.duplicate_counter += 1
            self.send_packets()

            if self.duplicate_counter == 3:
                self.update_fast_retransmit_window_size()
                self.create_packet(self.first_unacknowledged)
                self.canceled_timeouts.append(self.first_unacknowledged)

    def update_fast_retransmit_window_size(self):
        """Method that updates window size during fast retransmit.

        Sets threshold to half of current window size and retransmits lost packet.

        """
        self.fast_recovery = True
        self.last_partial_ack = max(self.unacknowledged_packets)
        self.first_partial_ack = min(self.unacknowledged_packets)
        self.ssthreshold = max(self.window_size / 2.0, 1)
        assert(self.duplicate_counter == 3)
        self.window_size = self.ssthreshold
        self.ns.record_window_size(self.flow_id, self.window_size)

    def send_packets(self, delay=0.0):
        """Method sends as many packets as possible, triggering the
        create_packet function.

        delay (float): delay until sending packets. Should only be used for
            initial send.
        """
        cur = self.first_unacknowledged

        effective_window_size = self.window_size
        if self.fast_recovery:
            effective_window_size += self.duplicate_counter

        while len(self.unacknowledged_packets) < int(effective_window_size) and cur < self.num_packets:
            if cur not in self.unacknowledged_packets:
                self.create_packet(cur, delay)
            cur += 1
