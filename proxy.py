import sys
import socket
import threading

def main():
    # command line args handling
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit()

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    if sys.argv[5] == 'True':
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


# The server_loop accepts incoming connections and spawns a new thread to the new connection
def server_loop(local_host,local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to liston on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit()

    print"[*] Listening on %s:%d" % (local_host, local_port)
    server.listen(5)

    while 1:
        client_socket, addr = server.accept()

        # print out the local connection inform
        print "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])

        # Start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

# 'proxy_handler' creates a TCP socket and connects to the remote host and port
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect (( remote_host, remote_port ))
    
    # Here we check the 'receive_first' parameter
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)

    # If we have data to send to the client, send it..
    if len(remote_buffer):
        print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
        client_socket.send(remote_buffer)

    while 1:

        # Reads from localhost if there's data
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            # Processes data with hexdump function
            hexdump(local_buffer)
            # Sends data to localhost
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print "[==>] Sent to remote."
        
        # Reads from remote host if there's data
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print "[==>] Received %d bytes from remote." % len(remote_buffer)
            # Processes data with hexdump
            hexdump(remote_buffer)
            # Sends data to remote host
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print "[==>] Sent to localhost."

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] No more data. Closing connections"
            break

def receive_from(connection):
#==========START HERE===============================











































