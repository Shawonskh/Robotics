from Commander import *

# <-- IP_ADRESS: Your raspberry IP address (You can check it by using 'ifconfig' command on raspberry)
# <-- PORT_NR: Port number. Change it to 60xx where xx is the number of your SD card following the 'R' (use 0x for 1-digit numbers (use 04 for R4))
IP_ADDRESS = "your.pi.ip.addr"  # for example "192.168.15.23"
PORT_NR = 6666


if __name__ == "__main__":

	commander = Commander(IP_ADDRESS, PORT_NR)

	try:
		while True:
			command = input("Enter command (F - forward, B - backward, S - stop, Q - quit) :")
			if command.strip() == 'Q':
				break

			commander.sendCommand(command)

	finally:
		commander.closeSocket()




