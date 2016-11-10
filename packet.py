class Packet(object):
    """A packet class that represents a data packet being sent from
        a source to a destination

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        packet_id (int): Unique id identifying the packet
        src (string): The flow's source node id
        dest (string): The flow's destination node
        packet_size (float): The packet's size in bits
        flow_id (string): Unique id indicating flow
    """

    def __init__(self, packet_id, src, dest, flow_id, packet_size):
        self._packet_id = packet_id
        self._src = src
        self._dest = dest
        self.packet_size = packet_size
        self.flow_id = flow_id

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
