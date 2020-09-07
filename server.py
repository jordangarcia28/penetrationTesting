# Referensi dari https://www.tutorialspoint.com/simple-chat-room-using-python

import time
import socket
import sys

time.sleep(1)

soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 1111
soc.bind(("127.0.0.1", port))

print(host_name, '({})'.format(ip))
name = input("Enter name : ")
soc.listen(1)

print("Waiting for connection...")
connection, addr = soc.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")
print("Connection Established. Connected From : {}, ({})".format(addr[0], addr[0]))

client_name = connection.recv(1024)
client_name = client_name.decode()
print(client_name + " has connected")
print('Type [bye] to leave the chatroom')

connection.send(name.encode())

while True:
	message = input("Me : ")
	if message == "[bye]":
		connection.send(message.encode())
		print("\n")
		break
	connection.send(message.encode())
	message = connection.recv(1024)
	message = message.decode()
	print(client_name, ":", message)