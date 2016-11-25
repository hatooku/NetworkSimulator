from node import Node
from host import Host
from packet import RoutingPacket

class Router(Node):
    """A class that will represent routers.

    Class variables:
        REROUTE_PERIOD (float): The length of time between each reroute cycle
            in seconds.

    Attributes:
        ns (NetworkSimulator): An instance of the NetworkSimulator class.
        node_id (string): The network address of the router.
        links (Link dict): The links that the router is connected to.
        routing_table (dict): The routing table for the router.
            { node_id : (link, cost) }
        cost_table (dict): The table detailing the cost of taking a specific
            link to a specific destination.
            { node_id : {link_id : cost}}
        adj_link_costs (dict): The table of adjacent link costs.
            { link_id : cost }

    """

    REROUTE_PERIOD = 5.0

    def __init__(self, ns, node_id):
        Node.__init__(self, ns, node_id)
        self.links = {}
        self.routing_table = {}
        self.cost_table = {}
        self.adj_link_costs = {}

    def add_links(self, links):
        """Add a dictionary of links to the router.

        Args:
            links (Link []): An array of links to add to the router.

        """

        for link in links:
            # Add the link to the link dictionary.
            self.links[link.link_id] = link

        # Start routing cycle
        event = lambda: self.start_routing_cycle()
        description = "Router.start_routing_cycle on router %s" % self.node_id
        self.ns.add_event(event, description)

    def send_packet(self, packet):
        """Sends a packet to another node.

        Args:
            packet (Packet): The packet to send.

        """

        # Use the routing table to send a packet to the right node

        link = self.routing_table[packet.dest][0]

        event = lambda: link.add_packet(packet, self.node_id)
        description = "Link.add_packet() with packet %d" % packet.packet_id
        self.ns.add_event(event, description)

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
            self.receive_routing_packet(packet, link_id)
        else: # We need to send the packet to its dest host
            self.send_packet(packet)

    def start_routing_cycle(self):
        """Begins a routing cycle."""

        self.update_adj_link_costs()
        self.update_routing_table()

        event = lambda: self.send_routing_packets()
        description = "Router.send_routing_packets on router %s" % self.node_id
        self.ns.add_event(event, description)

        next_cycle_event = lambda: self.start_routing_cycle()
        next_description = \
            "Router.start_routing_cycle on router %s" % self.node_id
        self.ns.add_event(next_cycle_event,
            next_description,
            delay=self.REROUTE_PERIOD)

    def send_routing_packets(self):
        """Sends out the routing table to all of the router's links."""

        for link in self.links.itervalues():
            src = self.node_id
            dest = link.get_other_node_id(self.node_id)
            if dest[0] == "H":
                continue
            packet = RoutingPacket(-1, src, dest, None, self.routing_table)
            event = lambda link=link, packet=packet: \
                link.add_packet(packet, self.node_id)
            description = "Link.add_packet() with routing packet from %s to %s"\
                % (src, dest)
            self.ns.add_event(event, description)

    def receive_routing_packet(self, routing_packet, adj_link_id):
        """Receives a routing packet and updates the routing table.

        Args:
            routing_packet (Packet): The routing packet we received.
            adj_link_id (string): The link id of the adjacent link the packet
                is on.

        """

        adj_cost = self.adj_link_costs[adj_link_id]
        
        for node_id, (link, cost) in routing_packet.routing_table.iteritems():
            # No need to put self in routing table
            if node_id == self.node_id:
                continue

            # Poison reverse - To improve convergence rates
            # If the path used by the adjacent node to get to destination
            # includes current node (self), then we set cost to infinity
            # to avoid cycles.
            if link.link_id == adj_link_id:
                cost = float('inf')

            if node_id not in self.cost_table:
                self.cost_table[node_id] = {}

            new_cost = cost + adj_cost
            self.cost_table[node_id][adj_link_id] = new_cost

        changed = self.update_routing_table()

        # If we do update the routing table, send out routing packets
        if changed:
            event = lambda: self.send_routing_packets()
            description = "Router.send_routing_packets on router %s" % self.node_id
            self.ns.add_event(event, description)

    def update_routing_table(self):
        """Updates the routing table, if necessary, according to the
        cost table.

        Returns:
            changed (bool): true if the routing table changed, false otherwise.

        """
        changed = False

        for node_id in self.cost_table:
            # Find the minimum cost and corresponding link in the cost table.
            # The lambda function means that the link_cost_pairs are minimized
            # first with respect to the cost (x[1]), and then link_id (x[0]).
            # The link_id is used for consistent tie-breaking.
            link_cost_pairs = self.cost_table[node_id].iteritems()
            min_link_id, min_cost = min(link_cost_pairs, key=lambda x:(x[1], x[0]))
            min_link = self.links[min_link_id]

            # Compare best link in the cost table with routing table entry
            if node_id not in self.routing_table or \
               self.routing_table[node_id] != (min_link, min_cost):
                #print "Changed, t =", self.ns.cur_time
                changed = True
                self.routing_table[node_id] = (min_link, min_cost)

        return changed

    def get_link_cost(self, link):
        """Returns the cost of a link.

        Args:
            link (Link): The link we want to find the cost of.

        """

        static_cost = link.prop_delay
        
        # how long for all packets in the buffer to complete action on the link
        prop_cost = link.prop_delay * len(link.link_buffer)
        trans_cost = link.cur_buffer_size / link.capacity
        dynamic_cost = prop_cost + trans_cost

        cost = static_cost + dynamic_cost

        return cost

    def update_adj_link_costs(self):
        """Updates the cost table using the dynamic costs of the router's
        links.

        """

        # Calculate new adjacent link costs.
        new_link_costs = {}
        for link_id, link in self.links.iteritems():
            new_link_costs[link_id] = self.get_link_cost(link)

        # If this is the first routing cycle, update the cost table for
        # adjacent nodes only.
        if len(self.adj_link_costs) == 0:
            for link_id, link in self.links.iteritems():
                other_node_id = link.get_other_node_id(self.node_id)
                self.cost_table[other_node_id] = {}
                self.cost_table[other_node_id][link_id] = new_link_costs[link_id]

        # Otherwise, update the entire cost table using the difference between
        # the previous adjcent link cost and the new cost.
        else:
            for node_id in self.cost_table:
                for link_id in self.cost_table[node_id]:
                    diff = new_link_costs[link_id] - self.adj_link_costs[link_id]
                    self.cost_table[node_id][link_id] += diff

        # Overwrite the adjacent link cost table with the new costs.
        self.adj_link_costs = new_link_costs
