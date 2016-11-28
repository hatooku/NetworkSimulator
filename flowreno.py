import sys
from packet import Packet, DataPacket, RoutingPacket, AcknowledgementPacket
from constants import *
from flow import Flow
import math

class FlowReno(Flow):

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time):
        self.fast_recovery = False
        Flow.__init__(self, ns, flow_id, src, dest, data_amount, start_time)

    def update_ack_window_size(self):
        """Method that updates window size when a packet is acknowledged.
        If the window size has reached the threshold, congestion avoidance will
        be switched on.

        """
        if self.fast_recovery:
            self.window_size = self.ssthreshold
            self.fast_recovery = False
        elif self.slow_start():
            self.window_size += 1.0
        else:
            self.window_size += 1.0 / math.floor(self.window_size)

    def update_loss_window_size(self):
        """Method that updates window size, and is called after a packet loss
        occurs.  Sets threshold to half of current window size, retransmits
        lost packet, and removes that packet from the unacknowledged packets.
        """
        self.fast_recovery = True
        self.ssthreshold = self.window_size / 2.0

    def send_packets(self, delay=0.0):
        """Method sends as many packets as possible, triggering the
        create_packet function.

        delay (float): delay until sending packets. Should only be used for
            initial send.
        """
        cur = self.first_unacknowledged

        effective_window_size = self.window_size
        if self.fast_recovery:
            effective_window_size = self.window_size + self.duplicate_counter

        while len(self.unacknowledged_packets) < int(effective_window_size) and cur < self.num_packets:
            if cur not in self.unacknowledged_packets:
                self.create_packet(cur, delay)
            cur += 1
