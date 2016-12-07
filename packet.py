from constants import *

class Packet(object):
    """A packet class that represents a packet being sent from a source to a 
    destination.

    Attributes:
        packet_id (int): An id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node id
        packet_size (float): The packet's size in bits
        flow_id (string): Unique id indicating flow
        timestamp (float): Time the packet was sent
    """

    def __init__(self, packet_id, src, dest, packet_size, flow_id, timestamp):
        self._packet_id = packet_id
        self._src = src
        self._dest = dest
        self._packet_size = packet_size
        self._flow_id = flow_id
        self._timestamp = timestamp

    @property
    def packet_id(self):
        return self._packet_id

    @packet_id.setter
    def packet_id(self, packet_id):
        raise AttributeError("Cannot modify id of a packet.")

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        raise AttributeError("Cannot modify a packet's source node.")

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, dest):
        raise AttributeError("Cannot modify a packet's destination node.")

    @property
    def packet_size(self):
        return self._packet_size

    @packet_size.setter
    def packet_size(self, packet_size):
        raise AttributeError("Cannot modify a packet's size.")

    @property
    def flow_id(self):
        return self._flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        raise AttributeError("Cannot modify a packet's flow id.")

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        raise AttributeError("Cannot modify timestamp of a packet.")


class DataPacket(Packet):
    """A class that will represent data packets.

    Attributes:
        packet_id (string): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node id
        flow_id (string): Unique id indicating flow
        data (string): Data string being stored in the packet
    """

    def __init__(self, packet_id, src, dest, flow_id, timestamp, data=""):
        Packet.__init__(self, packet_id, src, dest, DATA_PACKET_SIZE, flow_id, \
            timestamp)
        self.data = data

class RoutingPacket(Packet):
    """A class that will represent routing table packets.

    Attributes:
        packet_id (string): An id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node id
        flow_id (string): Unique id indicating flow
        routing_table (dict): Routing table
    """

    def __init__(self, packet_id, src, dest, flow_id, routing_table, timestamp):
        Packet.__init__(self, packet_id, src, dest, ROUT_PACKET_SIZE, flow_id, \
            timestamp)
        self.routing_table = routing_table

class AcknowledgementPacket(Packet):
    """A class that will represent acknowledgement packets.

    Attributes:
        packet_id (int): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node id
        flow_id (string): Unique id indicating flow
    """

    def __init__(self, packet_id, src, dest, flow_id, timestamp):
        Packet.__init__(self, packet_id, src, dest, ACK_PACKET_SIZE, flow_id, \
            timestamp)



    
