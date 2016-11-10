from packet import Packet
from constants import *

class RoutingPacket(Packet):
    """A class that will represent routing table packets.

    Attributes:
        packet_id (string): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        flow_id (string): Unique id indicating flow
        routing_table (dict): Routing table
    """

    def __init__(self, packet_id, src, dest, flow_id, routing_table):
        Packet.__init__(self, packet_id, src, dest, ROUT_PACKET_SIZE, flow_id)
        self.routing_table = routing_table
