from node import Node

class Host(Node):
    """A class that will represent hosts.

    Attributes:
        ns (NetworkSimulator): An instance of the NetworkSimulator class.
        node_id (int): The network address of the host.
        link (Link): The link that the host is connected to.
        flows (Flow dict): All the flows that are going out of the host.

    """

    def __init__(self, ns, node_id, link, flows):
        Node.__init__(self, ns, node_id)
        self._link = link
        self.flows = flows

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        raise AttributeError("Cannot modify the host's link")

    def send_packet(self, packet):
        """Sends a packet to another node.

        Args:
            packet (Packet): The packet to send.

        """
        pass

    def receive_packet(self, packet):
        """Receives a packet from another node.

        Args:
            packet (Packet): The packet we received.
            
        """
        pass