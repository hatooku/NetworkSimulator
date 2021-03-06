from node import Node
from packet import DataPacket, RoutingPacket

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
        """Sends a packet to another node by giving the packet to the host's
        link.

        Args:
            packet (Packet): The packet to send.

        """
        # Log send packet
        flow_id = packet.flow_id
        packet_id = packet.packet_id
        packet_size = packet.packet_size
        if isinstance(packet, DataPacket):
            self.ns.record_packet_send(flow_id, packet_id, packet_size)

        event = lambda: self._link.add_packet(packet, self.node_id)
        description = "Link.add_packet() with packet %d from %s" \
            % (packet.packet_id, self.node_id)
        self.ns.add_event(event, description)

    def receive_packet(self, packet, link_id):
        """Receives a packet from another node and then tells the flow that the
        packet came from to receive the packet and respond accordingly.

        Args:
            packet (Packet): The packet we received.
            link_id (string): The link id of the link the packet is on.
            
        """
        assert not isinstance(packet, RoutingPacket)
        assert packet.flow_id in self.flows
        assert packet.dest == self.node_id

        event = lambda: self.flows[packet.flow_id].receive_packet(packet)
        description = "Flow.receive_packet() with packet %d" % packet.packet_id
        self.ns.add_event(event, description)
