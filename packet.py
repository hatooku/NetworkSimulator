class Packet(object):
    """ A packet class that represents a data packet being sent from
        a source to a destination

    Args:
        ns: Instance of the NetworkSimulator class
        packet_id: Unique id identifying the packet
        src: The packet's source node
        dest: The packet's destination node
        data: Data string being stored in the packet

    Attributes:
        packet_id: Unique id identifying the packet
        src: The packet's source node
        dest: The packet's destination node
        data: Data string being stored in the packet

    """
    def __init__(self, ns, packet_id, src=0, dest=0, data=""):
        self._packet_id = packet_id
        self._src = src
        self._dest = dest
        self._data = data

    @property
    def packet_id(self):
        return id

    @packet_id.setter
    def packet_id(self, packet_id):
        raise Exception("Error: Can't change id of a packet.")

    @property
    def src(self):
        pass

    @src.setter
    def src(self, src):
        pass

    @property
    def dest(self):
        pass

    @dest.setter
    def dest(self, dest):
        pass

    @property
    def data(self):
        pass

    @data.setter
    def data(self, data):
        pass
