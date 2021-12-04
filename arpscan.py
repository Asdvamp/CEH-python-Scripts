import scapy.all as scapy
import time

def arpscan(iprange, * , castaddress="ff:ff:ff:ff:ff:ff", timeOut=5):
	arpLayer = scapy.ARP(pdst= iprange)
	ethLayer = scapy.Ether(dst= castaddress)
	arpPackets = ethLayer / arpLayer
	answered, unanswered = scapy.srp(arpPackets, timeout= timeOut)
	mapping = list()
	for each in answered:
		addresstuple = (each.query.pdst, each.answer.src)
		mapping.append(addresstuple)
	return mapping

iprange = "192.168.1.1/24"
maps = arpscan(iprange)

start = time.time()

TTL = 100
try:
	while True:
		end = time.time()
		if end - start > TTL:
			print("TableTimeout: Scanning Network Again...")
			maps = arpscan(iprange)
			with open("ARPtable.txt", "w") as table:
				table.writelines("IP address	:	MAC address\n")
				for entry in maps:
					table.writelines(f"{entry[0]}	:	{entry[1]}\n")
			start = end
except KeyboardInterrupt:
	print("KeyboardInterrupt: Exiting...")