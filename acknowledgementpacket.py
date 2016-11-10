from packet import Packet

class AcknowledgementPacket(Packet):
    """A class that will represent acknowledgement packets.

    Attributes:
        packet_id (int): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        packet_size (float): The packet's size in bits
        flow_id (string): Unique id indicating flow
    """

    def __init__(self, packet_id, src, dest, packet_size, flow_id, acknowledge_id):
        Packet.__init__(self, packet_id, src, dest, packet_size, flow_id)
