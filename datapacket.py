from packet import Packet

class DataPacket(Packet):
    """A class that will represent data packets.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        packet_id (string): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        packet_size (float): The packet's size in bits
        flow_id (string): Unique id indicating flow
        data (string): Data string being stored in the packet in bits
    """

    def __init__(self, ns, packet_id, src, dest, packet_size, flow_id, data=""):
        Packet.__init__(self, ns, packet_id, src, dest, packet_size, flow_id)
        self.data = data
