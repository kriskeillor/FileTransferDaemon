# Kris Keillor
# Demonstration Script - Server Daemon
# Multi User Data Daemon (MUDD) library
# v1.0.0
# Prof. Junaid Khan
# EECE 397A Wireless Networking


#   *   *   *   *   *   *
# INCLUDES
#   *   *   *   *   *   *
# System module
import sys
# Local Library Files
try:
    from ERROR_CODES import PICO_ERROR_NONE as ERR_NONE
    from ERROR_CODES import PICO_ERROR_TIMEOUT as ERR_TIMEOUT
    from ERROR_CODES import PICO_ERROR_GENERIC as ERR_GENERIC
    from ERROR_CODES import PICO_ERROR_NO_DATA as ERR_NO_DATA
except ImportError:
    print("Error loading MUDD library file 'ERROR_CODES.py.'")
    sys.exit(-1)
try:
    from MuddTable import append_values_bulk, append_entry, print_stream
except ImportError:
    print("Error loading MUDD library file MuddTable.py")
    sys.exit(ERR_GENERIC)
try:
    import MuddSocket
except ImportError:
    print("Error loading MUDD library file MuddSocket.py")
    sys.exit(ERR_GENERIC)
# Modules
import os
try:
    import random
except ImportError:
    print("Random module import failed")
    sys.exit(ERR_GENERIC)
try:
    import time
except ImportError:
    print("Time module import failed")
    sys.exit(ERR_GENERIC)
try:
    import _thread
except ImportError:
    print("_Thread module import failed")
    sys.exit(ERR_GENERIC)
try:
    from pathlib import Path
except ImportError:
    print("Pathlib.Path module import failed")
    sys.exit(ERR_GENERIC)


#   *   *   *   *   *   *
# VARIABLES
#   *   *   *   *   *   *
# File objects
fin_dir = "DataStreams/"
fout_dir = "DataStreamsFiltered/"
fname_test1 = "SampleDertData01"
fname_test2 = "SampleDertData02"
fname_test3 = "SampleDertData03"
dat_ext = ".csv"
# Socket settings
maxUsers = 3
localIP = "192.168.137.53"
tcpPort = 6545
ThreadCount = 0


#   *   *   *   *   *   *
# PROGRAM
#   *   *   *   *   *   *
daemon = MuddSocket.init_socket(localIP, tcpPort)
daemon.listen(maxUsers)
print("Listening on port {0} for up to {1} users.".format(localIP, maxUsers))

while True:
    (imp, addr) = daemon.accept()
    print("Connected to: {0}/{1}".format(addr[0], addr[1]))
    _thread.start_new_thread(MuddSocket.watch_socket_threaded, (imp, ))
    ThreadCount += 1
    print("Thread count: {0}".format(ThreadCount))