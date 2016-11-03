from collections import deque
'''
   Class for a link.
   
   Attributes:
   link_id is a unique identifier for each link
   max_buffer_size is how much data can be stored in the link buffer
   delay is propogation delay of the link
   capacity is the maximum link rate
   nodes is an array of the 2 nodes connected with this link
   
   link_buffer stores packets that are waiting to be sent on this link
   
   current_packet stores the packet being sent on the link.
   current_destination stores which host this packet is being sent to.
   '''   

class Link(object):
    '''
    Constructor for Link class takes the aformentioned 
    link_id,
    max_buffer_size,
    delay,
    capacity,
    nodes'''    
    def __init__ (self, link_id, max_buffer_size, delay, capacity, nodes):
        self._link_id = link_id
        self._max_buffer_size = max_buffer_size

        self._delay = delay
        self._capacity = capacity
        
        if(len(nodes) != 2):
            raise AttributeError("Node array should contain two nodes")
        self.nodes = nodes
        
        self.link_buffer = deque()
        self._current_packet = None
        self._current_direction = None
        
        
    @property
    def link_id(self):
        return self._link_id
    
    @link_id.setter
    def link_id(self, value):
        raise AttributeError("Can not modify link id")
    
    @property
    def max_buffer_size(self):
        return self._max_buffer_size
    
    @max_buffer_size.setter
    def max_buffer_size(self, value):
        raise AttributeError("Can not modify link's maximum buffer size")
    
    @property
    def delay(self):
        return self._delay
    
    @delay.setter
    def delay(self, value):
        raise AttributeError("Can not modify link's delay")
        
    @property
    def capacity(self):
        return self._delay    
    
    @capacity.setter
    def capacity(self, value):
        raise AttributeError("Can not modify link's capacity")
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = direction
    
    @property
    def current_packet(self):
        return self._current_packet
    
    @current_packet.setter
    def current_packet(self, value):
        raise AttributeError("Current packet should not be changed externally")
    
    @property
    def current_destination(self):
        return self._current_destination
    
    @current_packet.setter
    def current_destination(self, value):
        raise AttributeError("Current destination can not be changed externally")    
 
 
    
    
    ''' Puts the packet in the packet buffer to be sent to to the host with the
    opposite id. If no packet is being sent, calls the send_packet function'''
    def add_packet(self, packet, host_id):
        pass
    
    ''' Begins transfering the packet. '''
    def start_packet_trasfer(self):
        
        pass
    
    ''' When this event is called, the packet will be transfered to the host of 
        its destination. If there is another packet to be sent in the queue,
        send that packet '''
    def finish_packet_transfer(self):
        pass