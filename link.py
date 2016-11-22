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
        cur_packets (arr[Packet]): stores the packet being sent on the link
        cur_destination (Node): stores where to send this packet
        is_transmitting (Bool): we can only transmit one packet at a time
        
    """

    def __init__ (self, ns, link_id, max_buffer_size, prop_delay, capacity, 
                  nodes):
        self.ns = ns
        self._link_id = link_id
        self._max_buffer_size = max_buffer_size
        self._cur_buffer_size = 0.0
        self._num_packets = 0

        self._prop_delay = prop_delay
        self._capacity = capacity
        self._is_transmitting = False
        
        if len(nodes) != 2:
            raise AttributeError("Node array should contain two nodes")
        self.nodes = nodes
        
        self.link_buffer = deque()
        self._cur_packets = deque()
        self._cur_destination = None
        self.num_packets_transmitting = 0
        
        
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
    def num_packets(self):
        return self._num_packets
        
    @num_packets.setter
    def num_packets(self, value):
        raise AttributeError("Number of packets in buffer should not be" 
        "changed externally")    
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
    def cur_packets(self):
        return self._cur_packets
    
    @cur_packets.setter
    def cur_packet(self, value):
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
        other id. If no packet is being sent, calls start_packet_transfer.
        If the buffer is full, the packet is dropped.
        
        Args:
            packet (Packet): the packet being sent
            node_id (string): the id of the node sending the packet 
            
        """  
        if self.cur_buffer_size + packet.packet_size <= self.max_buffer_size:
            
            destination = self._get_other_node(node_id)
            self.link_buffer.append((packet, destination))
            self._cur_buffer_size += packet.packet_size
            self._num_packets += 1
            self.ns.record_buffer_occupancy(self.link_id, self.num_packets)
            

            if not self.is_transmitting:
                if len(self.cur_packets) == 0:
                    event = lambda: self.start_packet_transmission()
                    self.ns.add_event(event, "Link.start_packet_transmission with"
                              " link_id = %s" % (self.link_id))
                    self._is_transmitting = True
                elif destination == self.cur_destination:
                    event = lambda: self.start_packet_transmission()
                    self.ns.add_event(event, "Link.start_packet_transmission() with"
                              " link_id = %s" % (self.link_id))
                    self._is_transmitting = True
        else:
            print "Link %s is full; packet %s is dropped." \
                % (self.link_id, packet.packet_id)
            self.ns.record_packet_loss(self.link_id)
    
    def start_packet_transmission(self):
        if self.num_packets_transmitting != 0:
            print self.link_id
            temp = self.link_buffer.popleft()
            print temp[0].packet_id
            print self.num_packets_transmitting
            print self.ns.cur_time
            assert self.num_packets_transmitting == 0
        
        self.num_packets_transmitting += 1
        temp = self.link_buffer.popleft()

        self._cur_packets.append(temp[0])
        packet_size = temp[0].packet_size
        self._cur_buffer_size -= packet_size

        self._num_packets -= 1
        self.ns.record_buffer_occupancy(self.link_id, self.num_packets)

        event = lambda: self.start_packet_transfer()
        trans_delay = packet_size / self.capacity
        if self.cur_destination == None:
            self._cur_destination = temp[1]
            self.ns.add_event(event, "Link.start_packet_transfer() with"
                              " link_id = %s" % (self.link_id), trans_delay)

            if len(self.link_buffer) > 0:
                event = lambda: self.start_packet_transmission()
                self.ns.add_event(event, "Link.start_packet_transmission() with link_id = %s" \
                              % (self.link_id), trans_delay)

        elif temp[1] == self.cur_destination:
            self.ns.add_event(event, "Link.start_packet_transfer() with"
                              " link_id = %s" % (self.link_id), trans_delay)

            if len(self.link_buffer) > 0:
                event = lambda: self.start_packet_transmission()
                self.ns.add_event(event, "Link.start_packet_transmission() with link_id = %s" \
                              % (self.link_id), trans_delay)
        else:
            # if the direction isn't the same, we have to wait for the previous packet to propagte
            # and for this packet to transmit before we start transfering it.
            self.ns.add_event(event, "Link.start_packet_transfer() with"
                              " link_id = %s" % (self.link_id), trans_delay + self.prop_delay)


    def start_packet_transfer(self):
        """Send a packet
        
        Takes a packet out of the buffer and begins sending it to the correct
        node. Sets the current packet and current destination of the link. 
        
        """
        self._is_transmitting = False
        self.num_packets_transmitting -= 1
        event = lambda: self.finish_packet_transfer()
        self.ns.add_event(event, "Link.finish_packet_transfer() with"
                          " link_id = %s" % self.link_id, self.prop_delay)
   
    def finish_packet_transfer(self):
        """Hand off the packet it to the node it was going to. 
        
        When this method is called, the packet will be transfered to the 
        correct node. If there is another packet in the buffer that needs to be
        sent, the start_packet_transfer function will be called and another
        packet will be sent.
        
        """
        assert len(self.cur_packets) > 0
        assert self.cur_destination != None
        cur_destination = self.cur_destination
        cur_packet = self.cur_packet.popleft()
        event = lambda: cur_destination.receive_packet(cur_packet, self.link_id)
        self.ns.add_event(event, "Host.receive_packet() with node_id = %s, "
                          "cur_packet = %s, link_id = %s" \
                          % (cur_destination.node_id, cur_packet.packet_id, 
                             self.link_id))
        
        self.ns.record_link_rate(self.link_id, cur_packet.packet_size)
        
        if len(self.cur_packets) == 0:
            self._cur_destination = None
        
        if len(self.link_buffer) > 0 and not self.is_transmitting:
            event = lambda: self.start_packet_transmission()
            self.ns.add_event(event, "Link.start_packet_transmission() with link_id = %s" \
                          % (self.link_id))