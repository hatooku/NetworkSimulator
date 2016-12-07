"""Constants that can be globally accessed."""

# Unit conversion constants
BYTE_TO_BIT = 8.0
BIT_TO_BYTE = 0.125

MEGABIT_TO_BIT = 1000000.0
BIT_TO_MEGABIT = 0.000001

KILOBYTE_TO_BIT = 8000.0
BIT_TO_KILOBYTE = 0.000125

S_TO_MS = 1000.0
MS_TO_S = 0.001

# packet sizes
DATA_PACKET_SIZE = 1024.0 * BYTE_TO_BIT
ACK_PACKET_SIZE = 64.0 * BYTE_TO_BIT
ROUT_PACKET_SIZE = 128.0 * BYTE_TO_BIT

# How many seconds a flow waits before resending unacknowledged packets.
TIMEOUT_DELAY = 1000.0 * MS_TO_S

# How often a router dynamically routes in ms.
REROUTE_PERIOD = 5.0

# The length of time between each FAST TCP window size update in seconds.
FAST_WINDOW_UPDATE_PERIOD = 20 * MS_TO_S

# parameters for FAST TCP window size calculation
FAST_GAMMA = 0.5
FAST_ALPHA = 15
