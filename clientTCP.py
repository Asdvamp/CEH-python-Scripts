import socket
import sys
import time

PORT = 0
buffer = 1024
server = ("127.0.0.1", 12345)


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

try:
	clientsocket.bind((socket.gethostbyname(""), PORT))
	print(socket.gethostbyname(""))
except:
	print("[Binding Error] : Exiting...")
	sys.exit(1)

while True:
	try:
		clientsocket.connect(server)
		break
	except:
		print("[Server Offline] : Server Not Running, retrying")
		time.sleep(2)


while True:
	try:
		print("\"exit\" for exiting the program")
		message = input("Message -> ")
		if message.encode("utf-8") == b'':
			print("[Invalid Input] : Enter something!!")
			continue
		if message == "exit":
			message = message.encode("utf-8")
			try:
				clientsocket.send(message)
			except:
				break
			print("[Exit Received] Exiting...")
			time.sleep(2)
			break

		print("[Sending]: ", message)
		message = message.encode("utf-8")
		
		try:
			clientsocket.send(message)
		except:
			print("[Error] : Probable Server Error, Try to Reconnect")
			break
		try:
			msgFromServer= clientsocket.recv(buffer)
			print("[Reply From Server] :", msgFromServer.decode("utf-8"))
		except:
			print("[Error] : Probable Server Error, Resend")
	except KeyboardInterrupt:
		sys.exit(2)

clientsocket.close()