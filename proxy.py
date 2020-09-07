# berdasarkan belajar dari vincent 

from socket import socket
from threading import Thread

def client_process(client_conn, server_conn):
	while True:
		message = client_conn.recv(1024)
		message = message.decode()
		server_conn.send(message.encode())
	return



ip = "127.0.0.1"
ports = 1111
serversoc = socket()
serversoc.connect(("127.0.0.1", 1111))


portc = 1112
clientsoc = socket()
clientsoc.bind(("localhost",portc))
clientsoc.listen(5)

conn,_ = clientsoc.accept()

client_process_thread= Thread(target=client_process, args=(conn,serversoc,))

client_process_thread.start()

while True:
	message = serversoc.recv(1024)
	message = message.decode()
	conn.send(message.encode())