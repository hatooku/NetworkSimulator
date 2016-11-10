from packet import Packet
from constants import *

class AcknowledgementPacket(Packet):
    """A class that will represent acknowledgement packets.

    Attributes:
        packet_id (int): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        flow_id (string): Unique id indicating flow
    """

    def __init__(self, packet_id, src, dest, flow_id):
        Packet.__init__(self, packet_id, src, dest, ACK_PACKET_SIZE, flow_id)
