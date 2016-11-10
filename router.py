from node import Node
from routingpacket import RoutingPacket

class Router(Node):
    """A class that will represent routers.

    Attributes:
        ns (NetworkSimulator): An instance of the NetworkSimulator class.
        node_id (string): The network address of the router.
        links (Link dict): The links that the router is connected to.
        routing_table (dict): The routing table for the router.
            { node_id : (link, cost) }

    """

    def __init__(self, ns, node_id):
        Node.__init__(self, ns, node_id)
        self.links = {}
        self.routing_table = {}

    def add_links(self, links):
        """Add a dictionary of links to the router.

        Args:
            links (Link []): An array of links to add to the router.

        """
        for link in links:
            # Add the link to the link dictionary.
            self.links[link.link_id] = link

            # Add the link to the routing table.
            node_id = link.get_other_node_id(self.node_id)
            self.routing_table[node_id] = (link, link.prop_delay)

        # Send out routing packets to update all the other router's routing 
        # tables.
        self.send_routing_packets()

    def send_packet(self, packet):
        """Sends a packet to another node.

        Args:
            packet (Packet): The packet to send.

        """

        # Use the routing table to send a packet to the right node
        link = self.routing_table[packet.dest.node_id][0]

        event = lambda: link.add_packet(packet, self.node_id)
        self.ns.add_event(event)

    def receive_packet(self, packet, link_id):
        """Receives a packet from another node.

        If the packet needs to be sent to another node, this method will call
        send_packet().

        Args:
            packet (Packet): The packet we received.
            link_id (string): The link id of the link the packet is on.

        """

        # If we get a routing packet, we need to update the routing table
        if isinstance(packet, RoutingPacket):
            self.update_routing_table(packet, link_id)
        else: # We need to send the packet to its dest host
            self.send_packet(packet)

    def send_routing_packets(self):
        """Sends out the routing table to all of the router's links."""

        for link in self.links.itervalues():
            src = self.node_id
            dest = link.get_other_node_id(self.node_id)
            packet = RoutingPacket(None, src, dest, None, self.routing_table)
            event = lambda: link.add_packet(packet, self.node_id)
            self.ns.add_event(event)

    def update_routing_table(self, routing_packet, link_id):
        """Updates the routing table based on the routing packet the router just
        received.

        Args:
            routing_packet (Packet): The routing packet we received.

        """

        # Check if we should update the routing table
        changed = False
        cost = self.links[link_id].prop_delay

        for node_id, link_info in routing_packet.routing_table.iteritems():
            if node_id not in self.routing_table or
            link_info[1] + cost < self.routing_table[node_id][1]:

                self.routing_table[node_id] = (self.links[link_id],
                    link_info[1] + cost)
                changed = True

        # If we do update the routing table, send out routing packets
        if changed:
            self.send_routing_packets()
