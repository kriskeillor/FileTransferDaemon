# Kris Keillor
# Socket (TCP/IP) Script
# Multi User Data Daemon (MUDD) library
# v0.5.1
# Prof. Junaid Khan
# EECE 397A Wireless Networking
#   *   *   *   *   *   *


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
    print("Error loading MUDD library file ERROR_CODES.py.")
    sys.exit(-1)
try:
    from MuddTable import *
except ImportError:
    print("Error loading MUDD library file MuddTable.py.")
# Modules
try:
    from socket import *
except ImportError:
    print("Socket module import failed")
    sys.exit(ERR_GENERIC)
try:
    import time
except ImportError:
    print("Time module import failed")
    sys.exit(ERR_GENERIC)
try:
    import os
except ImportError:
    print("OS module import failed")
    sys.exit(ERR_GENERIC)
try:
    from select import *
except ImportError:
    print("Select module import failed")
    sys.exit(ERR_GENERIC)
try:
    import _thread
except ImportError:
    print("_Thread module import failed")
    sys.exit(ERR_GENERIC)


#   *   *   *   *   *   *   *
# VARIABLES
#   *   *   *   *   *   *   *
invalid_req_msg = "Please enter a valid code (AIR, LUX, or SOIL)".encode("ascii")
sample_data = "./DataStreams/SampleDertData03.csv"
air_path = os.path.expanduser("~/iotshare/AirData.csv")
lux_path = os.path.expanduser("~/iotshare/LuxData.csv")
soil_path = os.path.expanduser("~/iotshare/SoilData.csv")


#   *   *   *   *   *   *
# FUNCTIONS
#   *   *   *   *   *   *
# Initalize the socket with the assigned IP addr and provided port
def init_socket(addr, port):
    servSocket = socket(AF_INET, SOCK_STREAM)
    servSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    servSocket.bind((addr, port))
    return servSocket

# Create a threaded socket monitor for an individual user.
def watch_socket_threaded(connSocket):
    while True:
        msg = connSocket.recv(1024).decode()
        if msg == "AIR":
            get_rows_by_code(sample_data, ["ARH", "ATF"], air_path)
            connSocket.send("Data sent to iotshare/".encode())
        elif msg == "LUX":
            get_rows_by_code(sample_data, ["LUX"], lux_path)
            connSocket.send("Data sent to iotshare/".encode())
        elif msg == "SOIL":
            get_rows_by_code(sample_data, ["STC", "SWC"], soil_path)
            connSocket.send("Data sent to iotshare/".encode())
        else:
            connSocket.send(invalid_req_msg)
    return ERR_NONE
