import socket
import sys

# create a socket
def create_socket():
	try:	
		global host
		global port
		global sock

		host = ""
		port = 9999

		sock = socket.socket()
	except socket.error as msg:
		print('Socket creation error: ', msg)

# binding the socket and listening to connections
def bind_socket():
	try:
		global host
		global port
		global sock

		print("Binding the port: ", port)

		sock.bind((host, port))
		sock.listen(5)

	except socket.error as msg:
		print('Socket finding error: ', msg, ' | Retrying...')
		bind_socket()

# Establish connection with a client and the socket is listening
def socket_accept():
	conn, addr = sock.accept()
	print('Connection estalished: ', addr)
	send_command(conn)
	conn.close()

# send commands to client
def send_command(conn):
	while True:
		cmd = input()
		if cmd == 'quit':
			conn.close()
			sock.close()
			sys.exit()
		if len(str.encode(cmd)) > 0:
			conn.send(str.encode(cmd))
			client_response = str(conn.recv(1024), 'utf-8')
			print(client_response, end = "")

def main():
	create_socket()
	bind_socket()
	socket_accept()

if __name__ == "__main__":
	main()