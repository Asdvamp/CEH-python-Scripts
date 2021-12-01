
while True:
	message = input("Send -> ")
	with open("log.txt", "w") as file:
		file.write(message)