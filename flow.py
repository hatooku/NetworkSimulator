class Flow(object):
    """ A flow class that represents active connections between
    hosts and routers.

    Args:
        ns: Instance of the NetworkSimulator class
        flow_id: Unique id identifying the flow

    Attributes:
        flow_id: Unique id identifying the flow
        src: The flow's source node
        dest: The flow's destination node
        data_amount: Data capacity of the flow

        window_size: The size of the window
        unacknowledged_packets: The list of packets with no acknowledgement
        current_packet: The current packet in the flow
        num_packets:  The number of packets that have been through the flow
        last_acknowledged: The last acknowledged packet in the flow
    """
    def __init__(self, ns, flow_id):
        self._flow_id = flow_id

    @property
    def flow_id(self):
        return self.flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        raise Exception("Error: Can't change id of a flow.")

    @property
    def src(self):
        return id

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
    def dest(self, unacknowledged_packets):
        pass

    @property
    def current_packet(self):
        pass

    @current_packet.setter
    def current_packet(self, dest):
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
        """Method makes and returns packet

        Args:
            id: The unique id identifying the packet
            src: The packet's source node
            dest: The packet's destination node
            data: The data in the packet

        Returns:
            A packet with the given input arguments.  Triggers the send_packet
            function for the host if applicable
        """
        pass

    def acknowledge(self, packet):
        """Method that acknowledges a packet and sends it if applicable

        Args:
            packet: The packet attempting to be acknowledged

        Returns:
            Triggers the send_packet function for the host if applicable
        """
        pass

p = Flow(13, 12)
