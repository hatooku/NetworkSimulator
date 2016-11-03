class Flow(object):
    """A flow class that represents active connections between
    hosts and routers.

    Attributes:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (int): Unique id identifying the flow
        src (Node): The flow's source node
        dest (Node): The flow's destination node
        data_amount (int): Data capacity of the flow

        window_size (int): The size of the window
        unacknowledged_packets (dict): The list of packets with no acknowledgement
        current_packet (Packet): The current packet in the flow
        num_packets (int):  The number of packets that has been sent so far
        last_acknowledged (Packet): The last acknowledged packet in the flow

    """

    def __init__(self, ns, flow_id, src, dest, data_amount):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount

        self.window_size = 1
        self.unacknowledged_packets = -1
        self.current_packet  = -1
        self.num_packets = 0
        self.last_acknowledged = -1


    @property
    def flow_id(self):
        return self.flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        raise AttributeError("Cannot modify id of a flow.")

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        raise AttributeError("Cannot modify a flow's source node.")

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, dest):
        raise AttributError("Cannot modify a flow's destination node.")

    def make_packet(self, id, src, dest, data):
        """Method makes the packet and triggers the send_packet method for the
        host if applicable

        Args:
            id (int): The unique id identifying the packet
            src (Node): The packet's source node
            dest (Node): The packet's destination node
            data (any datatype): The data in the packet
        """
        pass

    def acknowledge(self, packet):
        """Method that triggers the send_packet function for the host if
        applicable by sending the acknowledgement packet

        Args:
            packet (Packet): The packet attempting to be acknowledged
        """
        pass
