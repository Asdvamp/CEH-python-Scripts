import socket
import sys
import time

server = ("127.0.0.1", 12345)
PORT = 0
BUFFER = 1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

try:
	clientsocket.bind((socket.gethostbyname(""), PORT))
except:
	print("[Binding Error] : Exiting...")
	sys.exit(1)

while True:
	try:
		print("\n\"exit\" for exiting the program")
		message = input("Message -> ")
		if message.encode("utf-8") == b'':
			print("[Invalid Input] : Enter something!!")
			continue
		if message == "exit":
			print("[Exit Received] Exiting...")
			time.sleep(2)
			break

		print("[Sending]: ", message)
		message = message.encode("utf-8")

		try:
			clientsocket.sendto(message, server)
		except:
			print("[Server Not Running] : Waiting")
			time.sleep(2)
			continue
		try:
			msgFromServer, serverAddress = clientsocket.recvfrom(BUFFER)
			print("[Reply From Server] :", msgFromServer.decode("utf-8"))
		except:
			print("[Error] : Probable Server Error, Retry")
	except KeyboardInterrupt:
		sys.exit(2)
clientsocket.close()