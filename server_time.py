import socket
import time
import sys
import datetime
import threading
from clock import clock

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.100.38', 8000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)

#Reloj del servidor
dt = datetime.datetime.now()
c = clock.Clock("Server time", [dt.hour, dt.minute, dt.second])
c.time()

def listening():
	global c
	while True:
		print('waiting for a connections')
		connection, client_address = sock.accept()
		try:
			print('connection from', client_address)
			print('sending time to the client')
			tm = bytes("{}:{}:{}".format(c.current_time[0], c.current_time[1], c.current_time[2]), 'utf-8')
			connection.sendall(tm)
			print("sending ", tm)
			data = connection.recv(1024).decode() #guardar esto en la base de datos reloj
			print("recieved", data)

		finally:
			connection.close()

listen = threading.Thread(target = listening)
listen.start()

c.root.mainloop()