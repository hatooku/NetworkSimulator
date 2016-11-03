from node import Node

class Host(Node):
    """A class that will represent hosts.

    Args:
        ns: An instance of the NetworkSimulator class.
        node_id: The network address of the host.
        link: The link that the host is connected to.
        flows: All the flows that are going out of the host.

    Attributes:
        ns: An instance of the NetworkSimulator class.
        node_id: The network address of the host.
        link: The link that the host is connected to.
        flows: All the flows that are going out of the host.

    """

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        raise AttributeError("Cannot modify the host's link")

    def __init__(self, ns, node_id, link, flows):
        Node.__init__(self, ns, node_id)
        self._link = link
        self.flows = flows

    def send_packet(self, packet):
        """Sends a packet to another node.

        Args:
            packet: The packet to send.

        """
        pass

    def receive_packet(self, packet):
        """Receives a packet from another node.

        Args:
            packet: The packet we received.
            
        """
        pass