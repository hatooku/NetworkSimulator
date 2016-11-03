from node import Node

class Router(Node):
    """A class that will represent routers.

    Args:
        ns: An instance of the NetworkSimulator class.
        node_id: The network address of the router.
        links: The links that the router is connected to.

    Attributes:
        ns: An instance of the NetworkSimulator class.
        node_id: The network address of the router.
        links: The links that the router is connected to.
        routing_table: The routing table for the router.

    """

    def __init__(self, ns, node_id, links):
        Node.__init__(self, ns, node_id)
        self.links = links
        self.routing_table = {}

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

    def make_routing_table(self):
        """Makes the routing table based on the links."""
        pass