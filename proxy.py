import socket, sys
import threading
import time
allowedDomains = ["iitkgp.ac.in","iitk.ac.in"]

def httpUrlParser(url):
	"Parses the given URL to get URI and Port"

	portocolIndicator = url.find("://")
	portIndicator = url.find(":", portocolIndicator + 3)
	if portIndicator == -1:
		port = 80
		if portocolIndicator == -1:
			return url, port
		else:
			return url[(portocolIndicator + 3): ], port
	else:
		port = int(url[(portIndicator+1):])
		if portocolIndicator == -1:
			return url[:portIndicator], port
		else:
			return url[(portocolIndicator + 3):portIndicator], port


def resourselocator(uri):
	"Parses the given URI to get domain and resource path"

	rootIndicator = uri.find("/")
	if rootIndicator == -1:
		domain = uri
		path = "/"
	else:
		domain = uri[:rootIndicator]
		path = uri[rootIndicator:]
	return domain, path


def incorrect(sockfdinc,desturl):
	"returns the proxy reply if accessing NOT allowed \"http\" domains"

	replyHTML = "<html><head><title>Access Blocked</title></head><body><h1>The access to the given URL is NOT ALLOWED</h1><p>-Reply from proxy server at 127.0.0.1:45678</p></body></html>"
	response_headers = { 'Content-Type': 'text/html; encoding=utf8', 'Content-Length': len(replyHTML), 'Connection': 'close',}
	response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
	response_proto = 'HTTP/1.1'
	response_status = '200'
	response_status_text = 'OK'
	header = '%s %s %s\r\n' % (response_proto, response_status, response_status_text)
	responsePass = header + response_headers_raw + "\r\n" + replyHTML
	try:
		sockfdinc.send(responsePass.encode("utf-8"))
	except:
		pass
	sockfdinc.close()
	print("[One Connection Closed] To ", desturl)

def notResponsive(sockfdres,destdomain):
	"returns the proxy reply if accessing NOT allowed \"http\" domains"

	replyHTML = "<html><head><title>Not Responsive</title></head><body><h1>The given URL is not responsive</h1><p>-Reply from proxy server at 127.0.0.1:45678</p></body></html>"
	response_headers = { 'Content-Type': 'text/html; encoding=utf8', 'Content-Length': len(replyHTML), 'Connection': 'close',}
	response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
	response_proto = 'HTTP/1.1'
	response_status = '200'
	response_status_text = 'OK'
	header = '%s %s %s\r\n' % (response_proto, response_status, response_status_text)
	responsePass = header + response_headers_raw + "\r\n" + replyHTML
	try:
		sockfdres.send(responsePass.encode("utf-8"))
	except:
		pass
	sockfdres.close()
	print("[One Connection Closed] To ", destdomain)

def HTTPrequest(destDomain, destPort, socketfd, toSendData):
	"Sends the HTTP response(from destination) to the requester"

	destsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	host = socket.gethostbyname(destDomain)
	try:
		destsock.connect((host,  destPort))
		destsock.send(toSendData.encode("utf-8"))
	except:
		destsock.close()
		notResponsive(socketfd, destDomain)
		return

	while True:
		try:
			replyFromdest = destsock.recv(BUFFER)
		except:
			destsock.close()
			notResponsive(socketfd, destDomain)
			return
		if len(replyFromdest) > 0:
			try:
				socketfd.send(replyFromdest)
			except:
				destsock.close()
				socketfd.close()
				return
		else:
			break
	destsock.close()
	socketfd.close()
	print("[One Connection Closed] To ", destDomain)


def datamanipulator(sessionfd, data, destURL, method, address):
	"Manipulates the received HTTP request"

	newlinedata = data.split("\n")			# Spliting the lines of HTTP request

	"""URL parsing"""
	addr, port = httpUrlParser(destURL)
	domain, path = resourselocator(addr)

	"""Data Manipulating"""
	modData = method
	modData += " " + path +  " "
	for head in newlinedata[0].split(" ")[2:]:
		modData += head
	modData += "\n"
	for eachdata in newlinedata[1:]:
		if eachdata.split(": ")[0] == "Request URI":
			modData += eachdata.split(": ")[0] + ": " + path + "\r\n"
		else:
			modData += eachdata + "\n"

	HTTPrequest(domain, port, sessionfd, modData)




"""MAIN FUNCTION"""

print("[Initiated]: Server Started ", time.asctime())

PORT = 45678
BACKLOG = 5
BUFFER = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

server.bind(("127.0.0.1", PORT))
server.listen(BACKLOG)

def sessionConv(session, address):
	"Checks for allowance and checks for data"
	try:
		data = session.recv(BUFFER)
	except:
		session.close()
		return
	if type(data) == bytes:
		data = data.decode("utf-8")
	if len(data) < 1:
		session.close()
		return
	"""Deals with first line of HTTP request"""
	newlinedata = data.split("\n")			# Spliting the lines of HTTP request
	requestline = newlinedata[0]			# Getting the first line
	requestparse = requestline.split(" ")	# Spliting the first line as [Method, URL, version]
	HTTPmethod = requestparse[0].lstrip()

	if HTTPmethod == "CONNECT":				# Session is HTTPS and so closing the session
		session.close()
	else:
		desturl = requestparse[1]			# Getting the URL
		print(f"[Connection To]: {desturl} ", time.asctime())
		allowance = False
		for domains in allowedDomains:
			if desturl.find(domains) != -1:
				allowance = True
				break
		if allowance:
			result = threading.Thread(target=datamanipulator, args=(session, data, desturl, HTTPmethod, address))
			result.start()
		else:
			incorrect(session, desturl)

while True:
	session, address = server.accept()
	connected = threading.Thread(target=sessionConv, args=(session, address))
	connected.start()