from node import Node

class Router(Node):
    """A class that will represent routers.

    Attributes:
        ns (NetworkSimulator): An instance of the NetworkSimulator class.
        node_id (string): The network address of the router.
        links (Link dict): The links that the router is connected to.
        routing_table (dict): The routing table for the router.

    """

    def __init__(self, ns, node_id):
        Node.__init__(self, ns, node_id)
        self.links = {}
        self.routing_table = {}

    def add_link(self, link):
        """Add a link to the router.

        Args:
            link (Link): The link to add.

        """
        self.links[link.link_id] = link

    def send_packet(self, packet):
        """Sends a packet to another node.

        Args:
            packet (Packet): The packet to send.

        """

        # Use the routing table to send a packet to the right node
        pass

    def receive_packet(self, packet):
        """Receives a packet from another node.

        If the packet needs to be sent to another node, this method will call
        send_packet().

        Args:
            packet (Packet): The packet we received.

        """

        # if we get a routing packet:
        #   update_routing_table(packet)
        # else: (we need to send a data packet or ack packet to its dest host)
        #   call send_packet(packet)
        pass

    def update_routing_table(self, routing_packet):
        """Updates the routing table based on the routing packet the router just
        received.

        Args:
            routing_packet (Packet): The routing packet we received.

        """

        # Check if we should update the routing table
        # If we do update the routing table, send out routing packets
        pass