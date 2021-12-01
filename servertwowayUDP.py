import socket
import time
import sys
import threading

localIP = socket.gethostbyname(socket.gethostname())

PORT = 12345
print(f"Server IP: {localIP} , Server Port: {PORT}")
buffer = 2048
inetAddress = (localIP, PORT)


serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

try:
	serversock.bind(inetAddress)
except:
	print("[Binding Error] : Exiting...")
	sys.exit(1)

print("[Initiated]: Server Started ", time.asctime())


mobileIP = input("[Client IP] ?: ")
mobilePort = int(input("[Client Port] ?: "))

def reciving():
	global address
	while True:
		try:
			message, address = serversock.recvfrom(buffer)
			message = message.decode("utf-8")
			print("reply -> ", message)
		except:
			print("[No Client] Waiting...")

def sending():
	while True:
		with open("log.txt","r") as file:
			message = file.read()
		if message.encode("utf-8") == b'':
			continue
		with open("log.txt","w") as file:
			file.write(b''.decode('utf-8'))
		try:
			addr = (mobileIP, mobilePort)
			serversock.sendto(message.encode("utf-8"), addr)
			print("sent-> ", message)
		except:
			print("[No Client] Waiting...")
			time.sleep(1)
			continue

	
try:
	reciver = threading.Thread(target=reciving)
	reciver.start()
	sender = threading.Thread(target=sending)
	sender.start()

except KeyboardInterrupt:
	sys.exit(2)