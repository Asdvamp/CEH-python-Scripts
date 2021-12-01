import socket
import time
import sys
import threading

localIP = "127.0.0.1"
PORT = 12345
buffer = 1024
inetAddress = (localIP, PORT)
backlog = 5

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

try:
	serversock.bind(inetAddress)
except:
	print("[Binding Error] : Exiting...")
	sys.exit(1)

serversock.listen(backlog)
print("[Initiated]: Server is Listening! ", time.asctime())


def reply(sockfd, threadcount):
	counter = 1
	print(f"[Waiting]: Thread: {threadcount} & Request Count -> ", counter)
	message = "wait"
	while True:
		try:
			message = sockfd.recv(buffer)
		except:
			print("[Error]: Probable Client Errror, Closing Thread ", threadcount)
			break
		message = message.decode("utf-8")
		if message == "exit":
			print("[Closed]: Connection to Thread ", threadcount, " Closed.")
			break
		counter += 1
		print("[Received]: Message -> ", message)

		reply = message.upper()
		print("[Sending]: Reply -> ", reply)

		try:
			sockfd.send(reply.encode("utf-8"))
			print(f"[Sent] : Thread: {threadcount} & Request No. ", counter - 1, " Fulfilled. ", time.asctime())
		except:
			print("[Error]: Probable Client Errror, Closing Thread", threadcount)
			break
	sockfd.close()
count = 1
try:
	while True:
		connectsock, address = serversock.accept()
		status = threading.Thread(target=reply, args=(connectsock, count))
		status.start()
		count += 1
except KeyboardInterrupt:
	sys.exit(2)