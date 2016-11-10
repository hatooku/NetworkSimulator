import sys
from packet import Packet
from datapacket import DataPacket
from acknowledgementpacket import AcknowledgementPacket
from routingpacket import RoutingPacket

class Flow(object):
    """A flow class that represents active connections between
    hosts and routers.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (string): Unique id identifying the flow
        src (string): The flow's source node id
        dest (string): The flow's destination node
        data_amount (float): Data capacity of the flow (bits)

        window_size (float): The size of the window
        unacknowledged_packets (dict): The list of packets with no acknowledgement
        current_packet (Packet): The current packet in the flow
        num_packets (float):  Number of packets to be sent through the flow
        num_packets_sent(float): Number of packets that have been sent through
            the flow
        last_acknowledged (float): The last acknowledged packet in the flow
        start_time (float): Start time in seconds

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time,
        unacknowledged_packets):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount
        self.start_time = start_time
        self.num_packets_sent = 0
        self.unacknowledged_packets = {}
        self.last_acknowledged = 0

        self.window_size = 1
        self.current_packet  = 0
        self.num_packets = 0


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
        raise AttributeError("Cannot modify a flow's source node.")

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, dest):
        raise AttributError("Cannot modify a flow's destination node.")

    def check_last(self):
        """Method that checks if all packets have been acknowledged and
        updating the NetworkSimulator object accordingly
        """
        if self.last_acknowledged == self.num_packets:
            self.ns.decrement_active_flows()

    def update_flow(a_packet):
        """Upon receiving an acknowledgement packet, updating the flow's
        attributes

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """
        print("Flow: updated with acknowledgement packet: ", a_packet.id,
            "And flow", self.flow_id)
        self.check_last()
        self.last_acknowledged = a_packet.packet_id
        self.unacknowledged_packets.remove(a_packet.packet_id)


    def make_data_packet(self, src, dest, packet_size, data):
        """Method makes the packet and triggers the send_packet method for the
        host if applicable

        Args:
            packet_id (string): Unique id identifying the packet
            src (Node): The packet's source node
            dest (Node): The packet's destination node
            packet_size (float): The packet's size in bits
            flow_id (string): Unique id indicating packet
            data (string): The data in the packet
        """
        new_packet = DataPacket(ns, self.num_packets_sent + 1, src, dest,
            self.flow_id, packet_size, data)
        print("Flow ", self.flow_id, ": made data packet", new_packet.packet_id)

        event = lambda: self.ns.hosts[new_packet.src].send_packet(new_packet)
        self.ns.add_event(event)

        self.num_packets_sent += 1

    def make_acknowledgment_packet(self, packet_id, src, dest, packet_size, acknowledge_id):
        """Method makes the packet and triggers the send_packet method for the
        host if applicable

        Args:
            packet_id (string): Unique id identifying the packet
            src (Node): The packet's source node
            dest (Node): The packet's destination node
            packet_size (float): The packet's size in bits
            flow_id (string): Unique id indicating packet
            acknowledge_id (string): Unique id identifying packet being acknowledged
        """
        print("Flow ", self.flow_id, ": made data packet", packet_id)
        new_packet = AcknowledgementPacket(ns, packet_id, src, dest,
            packet_size, self.flow_id, acknowledge_id)

        event = lambda: self.ns.hosts[new_packet.src].send_packet(new_packet)
        self.ns.add_event(event)

    def receive_packet(self, packet):
        """Method receives a given packet.  If it's a data packet, send an
        acknowledgement packet.  If it's an acknowledgement packet, update_flow
        """
        print("Flow ", self.flow_id, ": made data packet", new_packet.packet_id)
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
        print("Flow ", self.flow_id, ": made data packet", new_packet.packet_id)
        new_id = packet.packet_id + 1
        a_packet = make_acknowledgment_packet(packet.packet_id, packet.src,
            packet.dest, packet.packet_size, acknowledge_id, new_id)

        event = lambda: self.ns.hosts[packet.src].send_packet(packet)
        self.ns.add_event(event)

        num_packets_sent += 1
