'''
UW Python Certificate - py230
Lesson 02 - TCP/IP Sockets
Student: Michael List
Echo Server
'''

import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    '''Echo Server Function '''
    # set an address for our server
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    #SO_REUSEPORT allows to reuse address/port without manually terminating in shell
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    sock.bind(address)
    sock.listen(1)
    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))

                    conn.send(data)
                    print('sent "{0}"'.format(data.decode('utf8')))
                    #if retrieved stream chunk is empty stop reading from stream
                    if not data:
                        break
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                print(
                    'echo complete, client connection closed', file=log_buffer
                )
                conn.close()

    except KeyboardInterrupt:
        # close the server socket in case of Keyboard Interruption
        # and exit from the server function.
        sock.close()
        print('quitting echo server', file=log_buffer)
        #exits server function
        return False


if __name__ == '__main__':
    server()
    sys.exit(0)
