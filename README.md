# NetworkSimulator
CS 143 Project

To quickly run a simulation, use one of the testscripts provided using the command:
python testscript_name.py

i.e. python test0_fast.py, python test0_reno.py, ....

test scripts are provided for all 3 test cases using both types of flows.

To run with a custom JSON, the following commands can be used:
``` python 
>>> from src import *

>>> ns = NetworkSimulator()
>>> ns.populate("test0_fast.json") # other json files can be substituted here
>>> ns.run()

>>> ns.data_metrics.plot_link_rate()
>>> ns.data_metrics.plot_buffer_occupancy()
>>> ns.data_metrics.plot_packet_loss()
>>> ns.data_metrics.plot_flow_rate()
>>> ns.data_metrics.plot_flow_window_size()
>>> ns.data_metrics.plot_flow_packet_delay()
```

These plot methods can each given optional parameters that are specified in the report.
The JSON file should contain a network object with attributes "hosts", "links", and "flows".
The network object may or may not also include a "routers" attribute.
The details for these objects are further specified in the report.



