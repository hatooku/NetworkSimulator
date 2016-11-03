class Node(object):
    """A node class that will be the parent of the hosts and routers.

    Args:
        ns: An instance of the NetworkSimulator class.
        node_id: The network address of the host or router.

    Attributes:
        ns: An instance of the NetworkSimulator class.
        node_id: The network address of the host or router.

    """

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, value):
        raise AttributeError("Cannot modify network address")

    def __init__(self, ns, node_id):
        self.ns = ns
        self._node_id = node_id

    def send_packet(self, packet):
        """Sends a packet to another node. Must be implemented by host or
        router.

        Args:
            packet: The packet to send.

        """
        pass

    def receive_packet(self, packet):
        """Receives a packet from another node. Must be implemented by host or
        router.

        Args:
            packet: The packet we received.
            
        """
        pass