import heapq
import json
import sys

from constants import *

from flow import Flow
from host import Host
from link import Link
from router import Router

class NetworkSimulator(object):
    """The main class for the network simulator.

    The NetworkSimulator holds a reference to all elements of the network in
    the form of dictionaries. Also, it has a priority queue of events based
    on execution time. Finally, it holds a reference to a DataMetrics object
    which contains all the data obtained by the simulator.

    Attributes:
        flows (dict): all flows with their ids as the keys
        links (dict): all links with their ids as the keys
        nodes (dict): all nodes (hosts and routers) with their ids as the keys
        pq (arr): a heapq priority queue whose elements are a tuple in the
            form (execution_time, event_id, f) where f is the function to be
            run
        data (DataMetrics): container of all data generated by the simulator
        cur_time (float): a current time counter in seconds
        num_active_flows (int): Number of currently active flows
        event_counter (int): an event counter used to uniquely identify events

    """

    def __init__(self):
        self.flows = {}
        self.links = {}
        self.nodes = {}

        self.pq = []
        # self.data = DataMetrics()

        self._cur_time = 0
        self._num_active_flows = 0
        self._event_counter = 0

    @property
    def cur_time(self):
        return self._cur_time

    @cur_time.setter
    def cur_time(self, time):
        self._cur_time = time

    @property
    def num_active_flows(self):
        return self._num_active_flows
    
    @num_active_flows.setter
    def num_active_flows(self, num):
        raise Exception("Cannot modify num_active_flows in NetworkSimulator")

    @property
    def event_counter(self):
        return self._event_counter

    @event_counter.setter
    def event_counter(self, val):
        raise Exception("Cannot modify event_counter in NetworkSimulator")

    def add_host(self, host_id, link, flows):
        """Adds a new host to the network.

        Args:
            host_id (str): The network address of the host.
            link (Link): The link that the host is connected to.
            flows (dict): All the flows that are going out of the host.

        """
        host = Host(self, host_id, None, {})
        self.nodes[host_id] = host

    def add_router(self, router_id, links):
        """Adds a new router to the network.

        Args:
            router_id (str): id of the router
            links (array): the links that the router is connected to.

        """
        router = Router(self, router_id, [])
        self.nodes[router_id] = router

    def add_link(self, link_id, max_buffer_size, prop_delay, capacity, nodes):
        """Adds a new link to the network.

        Args:
            link_id (str): id of the link
            max_buffer_size (float): link buffer size in KB
            prop_delay (float): propogation delay of the link in ms
            capacity (float): the maximum link rate in Mbps
            nodes (array): an array of the 2 nodes connected with this link

        """
        # convert units into bits and seconds
        size_bits = max_buffer_size * KILOBYTE_TO_BIT
        prop_delay_s = prop_delay * MS_TO_S
        capacity_bps = capacity * MEGABIT_TO_BIT

        link = Link(self, link_id, size_bits, prop_delay_s, capacity_bps, nodes)
        self.links[link_id] = link

    def add_flow(self, flow_id, src, dest, data_amount):
        """Adds a new flow to the network.

        Args:
            flow_id (str): id of the flow
            src (Host): source host
            dest (Host): destination host
            data_amount (float): amount of data to be sent in MB

        """
        # Convert data_amount from megabytes to bits
        num_bits = data_amount * BYTE_TO_BIT * MEGABIT_TO_BIT

        flow = Flow(self, flow_id, src, dest, num_bits)
        self.flows[flow_id] = flow
        self._num_active_flows += 1

    def decrement_active_flows(self):
        self._num_active_flows -= 1

    def populate(self, network_description):
        """Populates a new network given a network description in JSON form.

        num_active_flows is set to the number of flows.

        Args:
            network_description (str): name of the json file containing the
                network description

        """
        self.clear_network()

        with open(network_description) as f:
            network = json.load(f).get("network", None)

        if network is None:
            raise Exception("Failed to load network description")

        for host in network["hosts"]:
            host_id = host["id"]
            self.add_host(host_id, None, None)
            print "Host %s added to network." % host_id

        for router in network.get("routers", []):
            router_id = router["id"]
            self.add_router(router_id, [])
            print "Router %s added to network." % router_id

        for link in network["links"]:
            link_id = link["id"]
            max_buffer_size = link["buffer_size"]
            prop_delay = link["delay"]
            capacity = link["rate"]
            connected_nodes = []
            for node_id in link["nodes"]:
                if node_id not in self.nodes:
                    raise Exception("Invalid network description. "
                                    "%s is not a valid node id." % node_id)
                connected_nodes.append(self.nodes[node_id])

            self.add_link(
                link_id,
                max_buffer_size,
                prop_delay,
                capacity,
                connected_nodes
            )
            print "Link %s added to network." % link_id

        for flow in network["flows"]:
            flow_id = flow["id"]
            data_amt = flow["data_amt"]
            if flow["src"] not in self.nodes:
                raise Exception("Invalid network description")
            if flow["dest"] not in self.nodes:
                raise Exception("Invalid network description")
            src = self.nodes[flow["src"]]
            dest = self.nodes[flow["dest"]]

            # NEED TO ADD STARTING TIME
            self.add_flow(flow_id, src, dest, data_amt)

            print "Flow %s added to network." % flow_id

        print "Network successfully populated."



    def run(self, duration=sys.float_info.max):
        """Runs the simulation for the given duration.
        
        Args:
            duration (float): the duration of the simulation in seconds.
                By default, the simulation runs until termination.

        """
        while self.pq and self.num_active_flows > 0 and self.cur_time < duration:
            event_time, _, f = heappop(self.pq)
            self.cur_time = event_time
            f()

        print "Simulation finished."

    def add_event(self, f, delay=0.0):
        """Adds an event to the priority queue.

        Args:
            f (func): the function to be run during this event.
            delay (float): the delay from the current time at which this event
                should be executed in seconds.

        """
        event = (self.cur_time + delay, self.event_counter, f)
        heapq.heappush(self.pq, event)
        self._event_counter += 1

    def plot_metrics(self):
        """Plots all relevant metrics from DataMetrics."""
        pass

    def clear_network(self):
        """Clears all network data."""
        self.flows = {}
        self.links = {}
        self.routers = {}
        self.hosts = {}

        self.pq = []
        # self.data = DataMetrics()

        self._cur_time = 0
        self._num_active_flows = 0
        self._event_counter = 0
""" 
from networksimulator import NetworkSimulator
n = NetworkSimulator()
n.populate("test1.json")
"""