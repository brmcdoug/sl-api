#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs
import ipaddress
import os
import sys
import threading

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_global_pb2_grpc
from genpy import sl_global_pb2
from genpy import sl_common_types_pb2
from genpy import sl_version_pb2
from genpy import sl_route_ipv4_pb2_grpc
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_common_pb2

# Utilities

# gRPC libs
import grpc
#import grpc.beta

#
# Get the GRPC Server IP address and port number
#
def get_server_ip_port():
    # Get GRPC Server's IP from the environment
    if 'SERVER_IP' not in os.environ.keys():
        print("Need to set the SERVER_IP env variable e.g.")
        print("export SERVER_IP='10.30.110.214'")
        os._exit(0)

    # Get GRPC Server's Port from the environment
    if 'SERVER_PORT' not in os.environ.keys():
        print("Need to set the SERVER_PORT env variable e.g.")
        print("export SERVER_PORT='57777'")
        os._exit(0)

    return (os.environ['SERVER_IP'], int(os.environ['SERVER_PORT']))


#
# Client Init: Initialize client session
#    stub: GRPC stub
#
def client_init(stub, event):
    #
    # Create SLInitMsg to handshake the version number with the server.
    # The Server will allow/deny access based on the version number.
    # The same RPC is used to setup a notification channel for global
    # events coming from the server.
    #
    # # Set the client version number based on the current proto files' version
    init_msg = sl_global_pb2.SLInitMsg()
    init_msg.MajorVer = sl_version_pb2.SL_MAJOR_VERSION
    init_msg.MinorVer = sl_version_pb2.SL_MINOR_VERSION
    init_msg.SubVer = sl_version_pb2.SL_SUB_VERSION

    # Set a very large timeout, as we will "for ever" loop listening on
    # notifications from the server
    Timeout = 365*24*60*60 # Seconds

    # This for loop will never end unless the server closes the session
    for response in stub.SLGlobalInitNotif(init_msg, Timeout):
        if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_VERSION:
            if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                    response.ErrStatus.Status) or \
                (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_CLEAR ==
                    response.ErrStatus.Status) or \
                (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_READY ==
                    response.ErrStatus.Status):
                print("Server Returned 0x%x, Version %d.%d.%d" %(
                    response.ErrStatus.Status,
                    response.InitRspMsg.MajorVer,
                    response.InitRspMsg.MinorVer,
                    response.InitRspMsg.SubVer))
                print("Successfully Initialized, connection established!")
                # Any thread waiting on this event can proceed
                event.set()
            else:
                print("client init error code 0x%x", response.ErrStatus.Status)
                os._exit(0)
        elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
            print("Received HeartBeat")
        elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
            if (sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM ==
                    response.ErrStatus.Status):
                print("Received notice to terminate. Client Takeover?")
                os._exit(0)
            else:
                print("Error not handled:", response)
        else:
            print("client init unrecognized response %d", response.EventType)
            os._exit(0)

#
# Thread starting point
#
def global_thread(stub, event):
    print("Global thread spawned")

    # Initialize the GRPC session. This function should never return
    client_init(stub, event)

    print("global_thread: exiting unexpectedly")
    # If this session is lost, then most likely the server restarted
    # Typically this is handled by reconnecting to the server. For now, exit()
    os._exit(0)

#
# Spawn a thread for global events
#
def global_init(channel):
    # Create the gRPC stub.
    stub = sl_global_pb2_grpc.SLGlobalStub(channel)

    # Create a thread sync event. This will be used to order thread execution
    event = threading.Event()

    # The main reason we spawn a thread here, is that we dedicate a GRPC
    # channel to listen on Global asynchronous events/notifications.
    # This thread will be handling these event notifications.
    t = threading.Thread(target = global_thread, args=(stub, event))
    t.start()

    # Wait for the spawned thread before proceeding
    event.wait()

    # Get the globals. Create a SLGlobalsGetMsg
    global_get = sl_global_pb2.SLGlobalsGetMsg()

    #
    # Make an RPC call to get global attributes
    #
    Timeout = 10 # Seconds
    response = stub.SLGlobalsGet(global_get, Timeout)

    # Check the received result from the Server
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("Max VRF Name Len     : %d" %(response.MaxVrfNameLength))
        print("Max Iface Name Len   : %d" %(response.MaxInterfaceNameLength))
        print("Max Paths per Entry  : %d" %(response.MaxPathsPerEntry))
        print("Max Prim per Entry   : %d" %(response.MaxPrimaryPathPerEntry))
        print("Max Bckup per Entry  : %d" %(response.MaxBackupPathPerEntry))
        print("Max Labels per Entry : %d" %(response.MaxMplsLabelsPerPath))
        print("Min Prim Path-id     : %d" %(response.MinPrimaryPathIdNum))
        print("Max Prim Path-id     : %d" %(response.MaxPrimaryPathIdNum))
        print("Min Bckup Path-id    : %d" %(response.MinBackupPathIdNum))
        print("Max Bckup Path-id    : %d" %(response.MaxBackupPathIdNum))
        print("Max Remote Bckup Addr: %d" %(response.MaxRemoteAddressNum))
    else:
        print("Globals response Error 0x%x" %(response.ErrStatus.Status))
        os._exit(0)


# Route get
#    channel: GRPC channel
#    entries_count: Number of entries requested
#
# A SLRoutev4GetMsg contains information to GET the first 'EntriesCount'
# entries.
# If the prefix and prefix length are not specified, get up to first 
# 'EntriesCount' entries
#
def route_get(channel, EntriesCount):
    # Create the gRPC stub.
    #stub = sl_route_ipv4_pb2.beta_create_SLRoutev4Oper_stub(channel)
    stub = sl_route_ipv4_pb2_grpc.SLRoutev4OperStub(channel)
    #
    # Create SL Get Message object
    #
    rt_msg = sl_route_ipv4_pb2.SLRoutev4GetMsg()
    
    #
    # VRF name 
    #
    rt_msg.VrfName = "default"
    
    #
    # Number of entries requested
    #
    rt_msg.EntriesCount = EntriesCount
    
    #
    # If FALSE: request up to 'EntriesCount' entries starting from prefix/prefix len key
    # If TRUE: or if key exact match is not found, request up to 'EntriesCount' entries
    #          starting from key's next
    #
    rt_msg.GetNext = False
    
    #
    # Make an RPC call
    #
    Timeout = 10 # Seconds
    response = stub.SLRoutev4Get(rt_msg, Timeout)
    
    #
    # Check the received result from the Server
    # 
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.ErrStatus.Status):
        print("Route Get Success!")
        print("Getting %d route entries Prefix and Prefix Length:" %(EntriesCount))
        for routes in response.Entries: 
            print (str(ipaddress.IPv4Address(routes.Prefix)) + "/" + str(routes.PrefixLen))
    else:
        print("Error code for route is 0x%x" % (
            response.ErrStatus.Status))
        os._exit(0)

#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':
    server_ip, server_port = get_server_ip_port()

    print("Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port))

    # Create the channel for gRPC.
    channel = grpc.insecure_channel(str(server_ip) + ":" + str(server_port))

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    global_init(channel)

    # RPC EOF to cleanup any previous stale routes
    #vrf_operation(channel, sl_common_types_pb2.SL_REGOP_EOF)

    # RPC route operations
    #    for add: sl_common_types_pb2.SL_OBJOP_ADD
    #    for update: sl_common_types_pb2.SL_OBJOP_UPDATE
    #    for delete: sl_common_types_pb2.SL_OBJOP_DELETE
    #route_operation(channel, sl_common_types_pb2.SL_OBJOP_ADD)

    #route_operation(channel, sl_common_types_pb2.SL_OBJOP_DELETE)
    # while ... add/update/delete routes

    # RPC route get
    # Takes in the channel and number of routes to get 
    route_get(channel, 20000)
    # Exit and Kill any running GRPC threads.
    os._exit(0)
