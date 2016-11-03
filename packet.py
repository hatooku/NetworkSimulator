class Packet(object):
    """A packet class that represents a data packet being sent from
        a source to a destination

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        packet_id (int): Unique id identifying the packet
        src (Node): The packet's source node
        dest (Node): The packet's destination node
        data (string): Data string being stored in the packet

    """

    def __init__(self, ns, packet_id, src, dest, data=""):
        self.ns = ns
        self._packet_id = packet_id
        self._src = src
        self._dest = dest
        self.data = data

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