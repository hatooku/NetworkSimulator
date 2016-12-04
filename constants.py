"""Unit conversion constants"""
BYTE_TO_BIT = 8.0
BIT_TO_BYTE = 0.125

MEGABIT_TO_BIT = 1000000.0
BIT_TO_MEGABIT = 0.000001

KILOBYTE_TO_BIT = 8000.0
BIT_TO_KILOBYTE = 0.000125

S_TO_MS = 1000.0
MS_TO_S = 0.001

DATA_PACKET_SIZE = 1024.0 * BYTE_TO_BIT
ACK_PACKET_SIZE = 64.0 * BYTE_TO_BIT
ROUT_PACKET_SIZE = 128.0 * BYTE_TO_BIT

TIMEOUT_DELAY = 500.0 * MS_TO_S
# Delay between the time a host receives an ACK and sends packets
SEND_DELAY = 10 * MS_TO_S

DEFAULT_NUM_WINDOWS = 500 # number of time windows

REROUTE_PERIOD = 5.0

# The length of time between each window size update in seconds.
FAST_WINDOW_UPDATE_PERIOD = 20 * MS_TO_S

FAST_GAMMA = 0.5
FAST_ALPHA = 15
