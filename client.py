# referensi dari https://www.tutorialspoint.com/simple-chat-room-using-python

import time
import socket
import sys

time.sleep(1)

soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)

print(shost, "({})".format(ip))
server_host = input("Enter server\'s IP address : ")
name = input("Enter client\'s' name : ")
port = 1112

print("Trying to connect to server : {}, ({})".format(server_host, port))

soc.connect((server_host, port))
print("Connected...\n")
soc.send(name.encode())
print("test")
server_name = soc.recv(1024)
server_name = server_name.decode()

print("{} has joined...".format(server_name))
print('Type [bye] to leave the chatroom')

while True:
	message = soc.recv(1024)
	message = message.decode()
	print(server_name, ":", message)
	message = input(str("Me : "))
	if message == "[bye]":
		message = "Leaving the chatroom"
		soc.send(message.encode())
		print("\n")
		break
	soc.send(message.encode())