import sys
from packet import Packet
from datapacket import DataPacket
from acknowledgementpacket import AcknowledgementPacket
from routingpacket import RoutingPacket
from constants import *
import math

class Flow(object):
    """A flow class that represents active connections between
    hosts and routers.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (string): Unique id identifying the flow
        src (Node): The flow's source node id
        dest (Node): The flow's destination node id
        data_amount (float): Data capacity of the flow (bits)

        start_time (float): Start time in seconds
        unacknowledged_packets (set): The list of packets with no acknowledgement
        timed_out_packets (set): The list of packets timed out before acknowledgement
        num_packets_sent(float): Number of packets that have been sent through
            the flow
        num_packets (float):  Number of packets to be sent through the flow
        window_size (float): The size of the window

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time,
        window_size=1):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount
        self.start_time = start_time
        self.num_packets_sent = 0
        self.unacknowledged_packets = set()
        self.timed_out_packets = set()
        self.num_packets = math.ceil(data_amount/DATA_PACKET_SIZE)
        self.window_size = window_size

        self.send_packets()

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
        if len(self.unacknowledged) == 0:
            self.ns.decrement_active_flows()

    def update_flow(a_packet):
        """Upon receiving an acknowledgement packet, updates the flow's
        attributes

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """
        print("Acknowledgement packet", packet_id, "in flow", self.flow_id)
        self.check_flow_completion()
        self.unacknowledged_packets.remove(a_packet.packet_id)

    def time_out(self, packet_id):
        """Method where sent packet is added to timed_out_packets array if
        still unacknowledged after a period of time

        Args:
            packet_id (int): packet_id of Packet being added to timed_out_packets

        """
        if packet_id in unacknowledged:
            timed_out_packets.add(packet_id)
            unacknowledged_packets.remove(packet_id)
            print("Packet", packet_id, "timed out in Flow", self.flow_id)

    def send_packets(self):
        """Method sends as many packets as possible, triggering the
        create_packet function.

        """
        while (len(self.unacknowledged_packets) < self.window_size):
            if (len(timed_out_packets) > 0):
                self.create_packet(min(timed_out_packets))
            else:
                self.create_packet(self.num_packets_sent)
                self.num_packets_sent += 1

    def create_packet(self, packet_id):
        """Method creates packet and then adds them to event queue to be sent
        to the host, and adds a timing event to ensure that they are resent if
        unacknowledged.

        Args:
            packet_id (int): Unique id identifying the packet

        """
        new_packet = DataPacket(packet_id, self.src.node_id,
            self.dest.node_id, self.flow_id)

        print("Flow", self.flow_id, ": made data packet", new_packet.packet_id)

        self.unacknowledged_packets.add(new_packet.packet_id)

        # Adding events to queues
        event1 = lambda: self.src.send_packet(new_packet)
        self.ns.add_event(event1)
        event2 = lambda: self.time_out(new_packet.packet_id)
        self.ns.add_event(event2, delay=ACK_DELAY)

        print("Flow", self.flow_id, ": sent data packet", new_packet.packet_id)

    def make_acknowledgement_packet(self, packet_id, src, dest, packet_size):
        """Method makes the AcknowledgementPacket and triggers the send_packet
        method for the host if applicable

        Args:
            packet_id (int): Unique id identifying the packet
            src (Node): The packet's source node
            dest (Node): The packet's destination node
            packet_size (float): The packet's size in bits
            flow_id (string): Unique id indicating flow

        """
        print("Flow ", self.flow_id, ": made acknowledgement packet", packet_id)
        new_packet = AcknowledgementPacket(packet_id, src, dest
            self.flow_id)

        event = lambda: self.src.send_packet(new_packet)
        self.ns.add_event(event)

    def receive_packet(self, packet):
        """Method receives a given packet.  If it's a data packet, send an
        acknowledgement packet.  If it's an acknowledgement packet, update_flow

        args:
            packet (Packet): packet object being received

        """
        print("Flow", self.flow_id, ": received data packet", packet.packet_id)
        if isinstance(packet, DataPacket):
            self.acknowledge(packet)
        elif isinstance(packet, AcknowledgementPacket):
            self.update_flow(packet)

    def acknowledge(self, packet):
        """Method that triggers the send_packet function for the host if
        applicable by sending the acknowledgement packet

        Args:
            packet (Packet): The packet attempting to be acknowledged

        """
        print("Flow", self.flow_id, ": sending acknowledgement packet",
            packet.packet_id)
        a_packet = make_acknowledgement_packet(packet.packet_id, packet.src,
            packet.dest, packet.packet_size)

        event = lambda: self.src.send_packet(packet)
        self.ns.add_event(event)
