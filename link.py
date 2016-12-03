from collections import deque
from packet import *

class Link(object):
    """A link which connects new nodes in the graph.
       
    Attributes:
        ns (NetworkSimulator): stores the simulator class running the simulation
        link_id (string): a unique identifier for each link
        max_buffer_size (float): how many bits can be stored in the link buffer
        cur_buffer_size (float): how many bits are in the link buffer
        num_packets (int): stores how many packets are in the buffer
        prop_delay (float): propagation delay of the link in s
        capacity (float): the maximum link rate in bits / s
        nodes (array): an array of the 2 nodes connected with this link
        link_buffer (Deque): stores packets waiting to be sent on this link
        packets_in_route (arr[Packet]): stores all packets being sent on the
                                    link either in transmission or propagation
        cur_destination (Node): stores the direction of all packets being
                                sent on the link
        is_transmitting (Bool): Keeps track of if a packet is being transmitted
        
    """

    def __init__ (self, ns, link_id, max_buffer_size, prop_delay, capacity, 
                  nodes):
        self.ns = ns
        self._link_id = link_id
        self._max_buffer_size = max_buffer_size
        self._cur_buffer_size = 0.0
  
        self._prop_delay = prop_delay
        self._capacity = capacity
        
        if len(nodes) != 2:
            raise AttributeError("Node array should contain two nodes")
        self.nodes = nodes
        
        self.link_buffer = deque()
        self._packets_in_route = deque()
        self.counter = 0
        
        
    @property
    def link_id(self):
        return self._link_id
    
    @link_id.setter
    def link_id(self, value):
        raise AttributeError("Cannot modify link id")
    
    @property
    def max_buffer_size(self):
        return self._max_buffer_size
    
    @max_buffer_size.setter
    def max_buffer_size(self, value):
        raise AttributeError("Cannot modify link's maximum buffer size")
    
    @property
    def cur_buffer_size(self):
        return self._cur_buffer_size

    @cur_buffer_size.setter
    def cur_buffer_size(self, new_buffer_size):
        raise AttributeError("Cannot modify current buffer size")
      
    @property
    def prop_delay(self):
        return self._prop_delay
    
    @prop_delay.setter
    def prop_delay(self, value):
        raise AttributeError("Cannot modify link's prop_delay")
        
    @property
    def capacity(self):
        return self._capacity  
    
    @capacity.setter
    def capacity(self, value):
        raise AttributeError("Cannot modify link's capacity")
    
    @property
    def packets_in_route(self):
        return self._packets_in_route
    
    @packets_in_route.setter
    def packets_in_route(self, value):
        raise AttributeError("Current packet should not be changed externally")

    def _get_cur_destination(self):
        if len(self._packets_in_route) == 0:
            return None

        first_packet_info = self._packets_in_route[0]
        dest = first_packet_info[1]

        for packet_info in self._packets_in_route:
            assert dest.node_id == packet_info[1].node_id

        return dest

    def _get_other_node(self, node_id):
        """Finds the node that node with id node_id is linked to.
        
        Checks which node of the links has the node_id that was passed in and 
        returns the other node. If neither node has that node_id, an error is
        thrown.
        
        Args:
            node_id (string): the id of the node whose opposite we wish to find.
        
        """
        destination = None
        if node_id == self.nodes[0].node_id:
            destination = self.nodes[1]
        elif node_id == self.nodes[1].node_id:
            destination = self.nodes[0]   
        else:
            raise Exception("This link is not connected to node with"
                            "node_id %s" % node_id)
        return destination        
        
    def get_other_node_id(self, node_id):
        """Finds the id of the node that node with id node_id is linked to.
        
        Gets the opposite node of the node with id node_id and returns the id.
        Allowed to be called publicly
          
        Args:
            node_id (string): the id of the node whose opposite we wish to find.
          
          """        
        other_node = self._get_other_node(node_id)
        return other_node.node_id 
    
    def add_packet(self, packet, node_id):
        """Add a packet to be sent
        
        Puts the packet in the packet buffer to be sent to to the node with the
        other id. If no other packets are in the buffer and not transmitting,
        checks if the packet added is eligible to be sent. If it is, calls
        start_packet_transmission. If the buffer is full, the packet is dropped.
        
        Args:
            packet (Packet): the packet being sent
            node_id (string): the id of the node sending the packet 
            
        """

        if self.cur_buffer_size + packet.packet_size <= self.max_buffer_size:
            
            destination = self._get_other_node(node_id)
            self.counter +=1
            self.link_buffer.append((packet, destination))
            self._cur_buffer_size += packet.packet_size

            # Assert _cur_buffer_size is correct
            assert self._cur_buffer_size == sum([packet_info[0].packet_size for packet_info in self.link_buffer])
            
            self.ns.record_buffer_occupancy(self.link_id, len(self.link_buffer))

            if len(self.link_buffer) == 1:
                cur_destination = self._get_cur_destination()
                if cur_destination is None or destination == cur_destination or len(self.packets_in_route) == 0:
                    self.start_packet_transmission()
        else:
            print "Link %s is full; packet %s is dropped @ t=%f" \
                % (self.link_id, packet.packet_id, self.ns.cur_time)
            self.ns.record_packet_loss(self.link_id)
    
    def start_packet_transmission(self):
        """Transmit a packet into the link
        
        Takes a packet out of the link buffer to be sent. Starts transmitting
        the packet. Calls the start_packet_propagation function to start 
        propagating the packet after the transmission delay. 
            
        """

        assert len(self.link_buffer) > 0

        packet, destination = self.link_buffer[0]
        cur_destination = self._get_cur_destination()
        assert cur_destination is None or cur_destination == destination

        event = lambda: self.start_packet_propagation()
        trans_delay = 1.0 * packet.packet_size / self.capacity
        
        self.ns.add_event(event, "Link.start_packet_propagation() with"
                              " link_id = %s" % (self.link_id), trans_delay)


    def start_packet_propagation(self):
        """Begin propagating a packet on the wire
        
        Starts propagating the packet. If the first packet in the buffer is
        going in the same direction, call start_packet_transmission.
        Calls finish_packet_transfer after the propagation delay.
        
        """
        packet, destination = self.link_buffer.popleft()
        self._cur_buffer_size -= packet.packet_size
        self.ns.record_buffer_occupancy(self.link_id, len(self.link_buffer))

        self._packets_in_route.append((packet, destination))
        assert self._get_cur_destination() == destination
       
        event = lambda: self.finish_packet_transfer()
        self.ns.add_event(event, "Link.finish_packet_transfer() with"
                          " link_id = %s" % self.link_id, self.prop_delay)

        if len(self.link_buffer) > 0:
            next_destination = self.link_buffer[0][1]
            if next_destination == self._get_cur_destination():
                self.start_packet_transmission()
   
    def finish_packet_transfer(self):
        """Hand off the packet to the node it was going to. 
        
        When this method is called, the packet will be transferred to the 
        correct node. If there is another packet in the buffer that needs to be
        sent, the start_packet_transmission function will be called and another
        packet will be sent.
        
        """
        assert len(self.packets_in_route) > 0
        cur_destination = self._get_cur_destination()
        packet, destination = self._packets_in_route.popleft()
        assert destination == cur_destination

        event = lambda: destination.receive_packet(packet, self.link_id)
        self.ns.add_event(event, "Node.receive_packet() with node_id = %s, "
                          "cur_packet = %s, link_id = %s" \
                          % (cur_destination.node_id, packet.packet_id, 
                             self.link_id))
        
        self.ns.record_link_rate(self.link_id, packet.packet_size)

        # Start transmitting next packet buffer if applicable.
        if len(self.link_buffer) > 0 and len(self._packets_in_route) == 0:
            next_packet, next_destination = self.link_buffer[0]
            # If destination == next_destination, it is already transmitting
            if destination != next_destination:
                assert self._get_other_node(destination.node_id) == next_destination
                self.start_packet_transmission()
    