from collections import deque

class Link(object):
    """A link which connects new nodes in the graph.
       
    Attributes:
        ns (NetworkSimulator): stores the simulator class running the simulation
        link_id (int): a unique identifier for each link
        max_buffer_size (int): how many bits can be stored in the link buffer
        prop_delay (float): propogation delay of the link in ms
        capacity (float): the maximum link rate in bits / ms
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
    
    
    def add_packet(self, packet, host_id):
        """Add a packet to be sent
        
        Puts the packet in the packet buffer to be sent to to the host with the
        other id. If no packet is being sent, calls the start_packet_transfer
        
        Args:
            packet (Packet): the packet being sent
            host_id (int): the id of the host sending the packet 
            
        """        
        pass
    
    
    def start_packet_trasfer(self):
        """Send a packet
        
        Takes a packet out of the buffer and begins sending it to the correct
        host. Sets the current packet and current destination of the link. 
        
        """
   
    def finish_packet_transfer(self):
        """Hand off the packet it to the Node it was going to. 
        
        When this method is called, the packet will be transfered to the 
        correct node. If there is another packet in the buffer that needs to be
        sent, the start_packet_transfer function will be called and another
        packet will be sent.
        
        """  
        pass