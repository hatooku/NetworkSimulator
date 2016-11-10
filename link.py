from collections import deque

class Link(object):
    """A link which connects new nodes in the graph.
       
    Attributes:
        ns (NetworkSimulator): stores the simulator class running the simulation
        link_id (string): a unique identifier for each link
        max_buffer_size (int): how many bits can be stored in the link buffer
        cur_buffer_size (int): how many bits are in the link buffer
        prop_delay (float): propogation delay of the link in s
        capacity (float): the maximum link rate in bits / s
        nodes (array): an array of the 2 nodes connected with this link
        link_buffer (Deque): stores packets waiting to be sent on this link
        cur_packet (Packet): stores the packet being sent on the link
        cur_destination (Node): stores where to send this packet
        
    """

    def __init__ (self, ns, link_id, max_buffer_size, prop_delay, capacity, nodes):
        self._ns = ns
        self._link_id = link_id
        self._max_buffer_size = max_buffer_size

        self._prop_delay = prop_delay
        self._capacity = capacity
        
        if len(nodes) != 2:
            raise AttributeError("Node array should contain two nodes")
        self.nodes = nodes
        
        self.link_buffer = deque()
        self._cur_packet = None
        self._cur_direction = None
        
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
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = value
    
    @property
    def cur_packet(self):
        return self._cur_packet
    
    @cur_packet.setter
    def cur_packet(self, value):
        raise AttributeError("Current packet should not be changed externally")
    
    @property
    def cur_destination(self):
        return self._cur_destination
    
    @cur_packet.setter
    def cur_destination(self, value):
        raise AttributeError("Current destination cannot be changed externally")    
    
    
    def add_packet(self, packet, node_id):
        """Add a packet to be sent
        
        Puts the packet in the packet buffer to be sent to to the node with the
        other id. If no packet is being sent, calls start_packet_transfer.
        If the buffer is full, the packet is dropped.
        
        Args:
            packet (Packet): the packet being sent
            node_id (string): the id of the node sending the packet 
            
        """  
        
        if self.cur_buffer_size + packet.packet_size <= self.max_buffer_size:
            
            if node_id == self.nodes[0].node_id:
                destination = nodes[1]
            elif node_id == self.nodes[1].node_id:
                destination = nodes[0]
            else:
                raise Exception("This link is not connected to node with \
                node_id %s" % node_id)
            
            self.link_buffer.append((packet, destination))
            self.cur_buffer_size += packet.packet_size
            
            if self.cur_packet == None:
                event = lambda: self.start_packet_transfer()
                self.ns.add_event(event)
        else:
            print "Link with id %s is full so packet with \
            id %s is dropped" % (self.link_id, packet.packet_id)
    
    def start_packet_transfer(self):
        """Send a packet
        
        Takes a packet out of the buffer and begins sending it to the correct
        node. Sets the current packet and current destination of the link. 
        
        """
        assert self.cur_destination == None
        assert self.cur_packet == None 
        assert len(self.link_buffer) > 0   
        
        packet_info = self.link_buffer.popleft()
        self.cur_packet = packet_info[0]
        self.cur_destination = packet_info[1]
        
        time_to_pass = self.cur_packet.packet_size / self.capacity
        time_to_pass += self.prop_delay
        
        event = lambda: self.finish_packet_transfer()
        print "Link %s beginning to transfer packet %s" \
              %(self.link_id, self.cur_packet.packet_id)
        self.ns.add_event(event, time_to_pass)
   
    def finish_packet_transfer(self):
        """Hand off the packet it to the node it was going to. 
        
        When this method is called, the packet will be transfered to the 
        correct node. If there is another packet in the buffer that needs to be
        sent, the start_packet_transfer function will be called and another
        packet will be sent.
        
        """ 
        event = lambda: self.cur_destination.recieve_packet(self.cur_packet)
        self.ns.add_event(event)
        
        print "Link %s finishing transfering packet %s. Handing to node %s" \
        %(self.link_id, self.cur_packet.packet_id, self.cur_direction.node_id)        
        
        self.cur_packet = None
        self.cur_destination = None
        
        if len(self.link_buffer) > 0:
            event = lambda: self.start_packet_transfer()
            self.ns.add_event(event)
  