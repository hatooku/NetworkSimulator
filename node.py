import abc

class Node(object):
    """A node class that will be the parent of the hosts and routers.

    Attributes:
        ns (NetworkSimulator): An instance of the NetworkSimulator class.
        node_id (string): The network address of the host or router.

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, ns, node_id):
        self.ns = ns
        self._node_id = node_id

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, value):
        raise AttributeError("Cannot modify node id")

    @abc.abstractmethod
    def add_link(self, link):
        """Add a link to the node.

        Args:
            link (Link): The link to add.

        """
        return

    @abc.abstractmethod
    def send_packet(self, packet):
        """Sends a packet to another node. Must be implemented by host or
        router.

        Args:
            packet (Packet): The packet to send.

        """
        return

    @abc.abstractmethod
    def receive_packet(self, packet):
        """Receives a packet from another node. Must be implemented by host or
        router.

        Args:
            packet (Packet): The packet we received.
            
        """
        return