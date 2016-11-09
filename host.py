from node import Node

class Host(Node):
    """A class that will represent hosts.

    Attributes:
        ns (NetworkSimulator): An instance of the NetworkSimulator class.
        node_id (string): The network address of the host.
        link (Link): The link that the host is connected to.
        flows (Flow dict): All the flows that are going into or out of the host.

    """

    def __init__(self, ns, node_id):
        Node.__init__(self, ns, node_id)
        self._link = None
        self.flows = {}

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        raise AttributeError("Cannot modify the host's link")

    def add_link(self, link):
        """Add a link to the host.

        Args:
            link (Link): The link to add.

        """
        self._link = link

    def add_flow(self, flow):
        """Add a flow to the host.

        Args:
            flow (Flow): The flow to add.

        """
        self.flows[flow.flow_id] = flow

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