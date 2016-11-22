from collections import deque

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
        is_transmitting (Bool): Keeps track on if a packet is being transmitted
        
    """

    def __init__ (self, ns, link_id, max_buffer_size, prop_delay, capacity, 
                  nodes):
        self.ns = ns
        self._link_id = link_id
        self._max_buffer_size = max_buffer_size
        self._cur_buffer_size = 0.0
  

        self._prop_delay = prop_delay
        self._capacity = capacity
        self._is_transmitting = False
        
        if len(nodes) != 2:
            raise AttributeError("Node array should contain two nodes")
        self.nodes = nodes
        
        self.link_buffer = deque()
        self._packets_in_route = deque()
        self._cur_destination = None
        
        
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
    
    @property
    def cur_destination(self):
        return self._cur_destination
    
    @cur_destination.setter
    def cur_destination(self, value):
        raise AttributeError("Current destination cannot be changed externally") 

    @property
    def is_transmitting(self):
        return self._is_transmitting
    
    @is_transmitting.setter
    def is_transmiting(self, value):
        raise AttributeError("Transmitting status cannot be changed externally")    
   

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
        other id. If no other packets are in the buffer and not transmiting,
        checks if the packet added is eligable to be sent. If it is, calls
        start_packet_transmission. If the buffer is full, the packet is dropped.
        
        Args:
            packet (Packet): the packet being sent
            node_id (string): the id of the node sending the packet 
            
        """  
        if self.cur_buffer_size + packet.packet_size <= self.max_buffer_size:
            
            destination = self._get_other_node(node_id)
            self.link_buffer.append((packet, destination))
            self._cur_buffer_size += packet.packet_size
            
            self.ns.record_buffer_occupancy(self.link_id, len(self.link_buffer))

            if len(self.link_buffer) == 1 and not self.is_transmitting:
                    if len(self.packets_in_route) == 0 or \
                        destination == self.cur_destination:
                       
                        event = lambda: self.start_packet_transmission()
                        self.ns.add_event(event, "Link.start_packet_transmission"
                                  " with link_id = %s" % (self.link_id))
                        self._is_transmitting = True
        else:
            print "Link %s is full; packet %s is dropped." \
                % (self.link_id, packet.packet_id)
            self.ns.record_packet_loss(self.link_id)
    
    def start_packet_transmission(self):
        """Transmit a packet into the link
        
        Takes a packet out of the link buffer to be sent. Starts transmitting
        the packet. Calls the start_packet_propagation function to start 
        propogating the packet after the transmission delay. 
            
        """
        packet_info = self.link_buffer.popleft()

        self._packets_in_route.append(packet_info[0])
        packet_size = packet_info[0].packet_size
        self._cur_buffer_size -= packet_size

       
        self.ns.record_buffer_occupancy(self.link_id, len(self.link_buffer))

        event = lambda: self.start_packet_propagation()
        trans_delay = packet_size / self.capacity
        total_delay = trans_delay
        
        if self.cur_destination is not None \
            and packet_info[1] != self.cur_destination:

            total_delay += self.prop_delay
        self.ns.add_event(event, "Link.start_packet_propagation() with"
                              " link_id = %s" % (self.link_id), total_delay)

        assert self._cur_destination is None \
                or self._cur_destination == packet_info[1]
        self._cur_destination = packet_info[1]


    def start_packet_propagation(self):
        """Begin propogating a packet on the wire
        
        Starts propogating the packet. If the first packet in the buffer is
        going in the same direction, call start_packet_transmission.
        Calls finish_packet_transfer after the propogation delay.
        
        """
       
        self._is_transmitting = False
       
        event = lambda: self.finish_packet_transfer()
        self.ns.add_event(event, "Link.finish_packet_transfer() with"
                          " link_id = %s" % self.link_id, self.prop_delay)

        assert self.cur_destination is not None

        if len(self.link_buffer) > 0:
            next_packet = self.link_buffer[0]
            if next_packet[1] == self.cur_destination:
               
                event = lambda: self.start_packet_transmission()
                self.ns.add_event(event, "Link.start_packet_transmission()"
                 " with link_id = %s" % (self.link_id))
                self._is_transmitting = True
            else:
                # if the direction isn't the same, we have to wait for the 
                # previous packet to propagte before we transmit the next packet.
                event = lambda: self.start_packet_transmission()
                self.ns.add_event(event, "Link.start_packet_transmission()"
                 "with link_id = %s" % (self.link_id), self.prop_delay)
                self._is_transmitting = True
   
    def finish_packet_transfer(self):
        """Hand off the packet it to the node it was going to. 
        
        When this method is called, the packet will be transfered to the 
        correct node. If there is another packet in the buffer that needs to be
        sent, the start_packet_transmission function will be called and another
        packet will be sent.
        
        """
        assert len(self.packets_in_route) > 0
        assert self.cur_destination != None
        cur_destination = self.cur_destination
        cur_packet = self.packets_in_route.popleft()
        event = lambda: cur_destination.receive_packet(cur_packet, self.link_id)
        self.ns.add_event(event, "Host.receive_packet() with node_id = %s, "
                          "cur_packet = %s, link_id = %s" \
                          % (cur_destination.node_id, cur_packet.packet_id, 
                             self.link_id))
        
        self.ns.record_link_rate(self.link_id, cur_packet.packet_size)
        
        if len(self.packets_in_route) == 0:
            self._cur_destination = None
        
        if len(self.link_buffer) > 0 and not self.is_transmitting:
            self._is_transmitting = True
            event = lambda: self.start_packet_transmission()
            self.ns.add_event(event, "Link.start_packet_transmission() with" 
                "link_id = %s" % (self.link_id))
    