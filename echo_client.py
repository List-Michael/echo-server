'''
UW Python Certificate - py230
Lesson 02 - TCP/IP Sockets
Student: Michael List
Echo Client
'''

import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    '''Echo Client'''
    server_address = ('localhost', 10000)
    # instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    # connect your socket to the server
    sock.connect((server_address))
    # variable for accumulating the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        # send your message to the server here.
        sock.sendall(msg.encode('utf-8'))
        chunk = ''
        while True:
            # reading 16-byte chunks sent by server
            chunk = sock.recv(16)
            # Log each chunk with the print statement below
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            decoded_chunk = chunk.decode('utf-8')
            #Building up entire reply from the server
            received_message += decoded_chunk
            #break loop once entire message has been received
            if len(chunk) < 16:
                break
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # close client socket
        print('closing socket', file=log_buffer)
        sock.close()
        # return the entire reply from the server as return value
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
