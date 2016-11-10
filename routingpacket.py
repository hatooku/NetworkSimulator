from packet import Packet

class RoutingPacket(Packet):
    """A class that will represent routing table packets.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        packet_id (string): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        packet_size (float): The packet's size in bits
        flow_id (string): Unique id indicating flow
        routing_table (dict): Routing table
    """

    def __init__(self, ns, packet_id, src, dest, packet_size, flow_id, routing_table):
        Packet.__init__(self, ns, packet_id, src, dest, packet_size, flow_id)
        self.routing_table = routing_table
