import socket
import gopigo as go

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

go.set_speed(50)

try:
    # <-- 66xx = Port number. Change it to 60xx where xx is the number of your SD card following the 'R' (use 0x for 1-digit numbers (use 04 for R4))
    PORT_NR = 6666  # You should change it

    server_socket.bind(('', PORT_NR))

    if PORT_NR == 6666:
        raise ValueError("You did not change the port number to 60xx")

    while 1:
        dataFromClient, address = server_socket.recvfrom(256)  # Receive data from client

        # Data is received as a bit stream, so it needs to be decoded first
        dataFromClient = dataFromClient.decode("utf-8").strip()  # To avoid any errors in comparison when a line ending is appended

        print(dataFromClient)  # To see what is received

        if dataFromClient == 'F':
            print("fwd")
            go.fwd()

        elif dataFromClient == 'B':
            print("bwd")
            go.bwd()

        elif dataFromClient == 'S':
            print("stop")
            go.stop()
        # <-- You should implement the rest of the necessary commands!


finally:
    # Close the socket if any error occurs
    go.stop()  # Make sure to always stop the robot if the server stops for any reason
    print("exiting")
    server_socket.close()

