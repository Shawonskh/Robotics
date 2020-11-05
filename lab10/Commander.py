import socket

class Commander:
    # The Commander needs to know the IP address and the port to send data to
    def __init__(self, ip, port):
        if ip == "your.pi.ip.addr" or ip == "192.168.15.23":
            raise ValueError("You did not change the IP address to your raspberry pi IP")
        if port == 6666:
            raise ValueError("You did not change the port number to 60xx, where xx is the number part of your SD card number")

        self.ip = ip
        self.port = port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Open a client socket

    # Send a command to the robot
    def sendCommand(self, command):

        try:
            # Send data out. Communication happens using bit streams, so we need to encode the string first.
            self.client_socket.sendto(command.encode('utf-8'), (self.ip, self.port))

        except e:
            print(str(e))
            # Close the socket if any error occurs
            self.closeSocket()

    # Be sure to call closeSocket() when the program ends
    def closeSocket(self):
        self.client_socket.close()
