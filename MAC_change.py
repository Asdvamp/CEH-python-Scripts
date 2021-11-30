import subprocess
import sys

try:
	interface = sys.argv[1]
except:
	print("inteface was not specified, provide interface below.")
	interface = input("interface: ")

try:
	newMAC = sys.argv[2]
except:
	print("MAC address was not specified, provide MAC address below.")
	newMAC = input("new MAC: ")


print(f"[.] Running {sys.platform} Operating System.")
print(f"[.] Interface {interface} to be Modified.")
print(f"[.] The new MAC address is {newMAC}.")

if sys.platform == "linux":
	subprocess.call(f"ifconfig {interface} down", shell=True)
	subprocess.call(f"ifconfig {interface} hw ether {newMAC}", shell=True)
	subprocess.call(f"ifconfig {interface} up", shell=True)
elif "win" in sys.platform:
	subprocess.call(f"ipconfig /all", shell=True)
else:
	print("Not identifiable Operating System.")