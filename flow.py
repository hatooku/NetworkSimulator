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
        last_acknowledged (float): The last acknowledged packet in the flow
        start_time (float): Start time in seconds

    """

    def __init__(self, ns, flow_id, src, dest, data_amount, start_time):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount
        self.start_time = start_time

        self.window_size = 1
        self.unacknowledged_packets = -1
        self.current_packet  = -1
        self.num_packets = 0
        self.last_acknowledged = -1

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
            self.ns.num_active_flows -= 1

    def update_flow(a_packet):
        """Upon receiving an acknowledgement packet, updating the flow's
        attributes

        Args:
            a_packet (AcknowledgementPacket): Packet being sent
                back from host
        """
        print("Flow: updated with acknowledgement packet")
        self.last_acknowledged += 1
        self.check_last()
        self.unacknowledged_packets.remove(a_packet)


    def make_data_packet(self, packet_id, src, dest, packet_size, data):
        """Method makes the packet and triggers the send_packet method for the
        host if applicable

        Args:
            packet_id (string): Unique id identifying the packet
            src (Node): The packet's source node
            dest (Node): The packet's destination node
            packet_size (float): The packet's size in bits
            flow_id (string): Unique id indicating packet
            data (any datatype): The data in the packet
        """
        print("Flow: made data packet")
        new_packet = DataPacket(ns, packet_id, src, dest, self.flow_id,
            packet_size, data)
        ns.flows[new_packet.dest].send_packet(new_packet)

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
        print("Flow: made acknowledgement packet")
        new_packet = AcknowledgementPacket(ns, packet_id, src, dest,
            packet_size, self.flow_id, acknowledge_id)
        ns.flows[new_packet.dest].send_packet(new_packet)

    def receive_packet(self, packet):
        """Method receives a given packet: acknowledges packet if it's a
        data packet, updates the flow if it's an acknowledgement packet
        """
        print("Flow: received packet")
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
        print("Flow: acknowledged packet")
        ns.flows[packet.dest].send_packet(packet)
