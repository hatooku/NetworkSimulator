class Flow(object):
    """ A flow class that represents active connections between
    hosts and routers.

    Args:
        ns (NetworkSimulator): Instance of the NetworkSimulator class
        flow_id (int): Unique id identifying the flow

    Attributes:
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

    def __init__(self, ns, flow_id, src, dest, data_amount=0, window_size=0, unacknowledged_packets=[],
    current_packet=0, num_packets=0, last_acknowledged=0):
        self.ns = ns
        self._flow_id = flow_id
        self._src = src
        self._dest = dest
        self.data_amount = data_amount
        self.window_size
        self.unacknowledged_packets = unacknowledged_packets
        self.current_packet = current_packet
        self.num_packets = num_packets
        self.last_acknowledged

    @property
    def flow_id(self):
        return self.flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        raise AttributeError("Error: Can't change id of a flow.")

    @property
    def src(self):
        return src

    @src.setter
    def src(self, src):
        raise AttributeError("Error: Can't change a flow's source node.")

    @property
    def dest(self):
        pass

    @dest.setter
    def dest(self, dest):
        raise AttributError("Error: Can't change a flow's destination node.")

    @property
    def data_amount(self):
        pass

    @data_amount.setter
    def data_amount(self, data_amount):
        pass

    @property
    def window_size(self):
        pass

    @window_size.setter
    def window_size(self, window_size):
        pass

    @property
    def unacknowledged_packets(self):
        pass

    @unacknowledged_packets.setter
    def unacknowledged_packets(self, unacknowledged_packets):
        pass

    @property
    def current_packet(self):
        pass

    @current_packet.setter
    def current_packet(self, current_packet):
        pass

    @property
    def num_packets(self):
        pass

    @num_packets.setter
    def num_packets(self, num_packets):
        pass

    @property
    def last_acknowledged(self):
        pass

    @current_packet.setter
    def last_acknowledged(self, last_acknowledged):
        pass

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
