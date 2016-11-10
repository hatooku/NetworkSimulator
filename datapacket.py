from packet import Packet
from constants import *

class DataPacket(Packet):
    """A class that will represent data packets.

    Attributes:
        packet_id (string): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        flow_id (string): Unique id indicating flow
        data (string): Data string being stored in the packet in bits
    """

    def __init__(self, packet_id, src, dest, flow_id, data=""):
        Packet.__init__(self, ns, packet_id, src, dest, DATA_PACKET_SIZE, flow_id)
        self.data = data
