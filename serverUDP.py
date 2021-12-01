import socket
import time
import sys

localIP = "127.0.0.1"
PORT = 12345
buffer = 1024
inetAddress = (localIP, PORT)


serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
try:
	serversock.bind(inetAddress)
except:
	print("[Binding Error] : Exiting...")
	sys.exit(1)

print("[Initiated]: Server is Listening! ", time.asctime())

count = 1
try:
	while True:
		print("[Waiting]: Request Count -> ", count)
		try:
			message, address = serversock.recvfrom(buffer)
		except:
			print("[Error]: Probable Client Errror")
			continue
		message = message.decode("utf-8")
		count += 1
		print("[Received]: Message -> ", message)
		reply = message.upper()
		print("[Sending]: Reply -> ", reply)
		try:
			serversock.sendto(reply.encode("utf-8"), address)
			print("[Sent] : Request No. ", count - 1, " Fulfilled. ", time.asctime())
		except:
			print("[Error] Probable Client Error, Request ", count -1, " Failed.")
except KeyboardInterrupt:
	sys.exit(2)