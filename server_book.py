import socket
import sys
import time
import datetime
import threading
from clock import clock
from timeit import default_timer as timer 
import random

clock_time = [11, 33, 22]
update_delay = 2
c = clock.BookClock("Book server", clock_time) ##De aqui se saca la hora del reloj
c.time()
sessions = 0

def synchronize_time():
	while True:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = ('192.168.100.38', 8000)
			#print('connecting to {} port {}'.format(*server_address))
			sock.connect(server_address)
			ct = datetime.datetime.now()
			t0 = timer()
			data = sock.recv(1024).decode().split(":")
			st = datetime.datetime.now()
			st = st.replace(hour = int(data[0]), minute = int(data[1]), second = int(data[2]))
			t1 = timer()
			latency = t1 - t0
			nt = st + datetime.timedelta(seconds = (latency / 2))
			#print("data", data)
			#print("last time", ct)
			#print("latency", latency)
			#print("server time", st)
			#print("new time", nt)
			global clock_time
			clock_time[0] = nt.hour
			clock_time[1] = nt.minute
			clock_time[2] = nt.second
			global c
			c.current_time = clock_time
			data = "{}:{}|{}|{}|{}|{}".format(*server_address, ct, latency, st, nt)
			sock.sendall(data.encode())

		finally:
		    #print('closing socket')
		    sock.close()
		    time.sleep(update_delay)

update_time = threading.Thread(target = synchronize_time)
update_time.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.100.38', 9000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)

def listening(n = 5):
	global c
	global sessions
	book_list = list(range(n)) #Llenar la base de datos con 5 libros
	while True:
		connection, client_address = sock.accept()
		sessions = sessions + 1
		print("connection for booksssssssss")
		try:
			print("connection from", client_address)

			if len(book_list) < 1:
				data = "-1".encode()
				connection.sendall(data)
				response = connection.recv(1024).decode()
				print("RESPONSE", response)
				book_list = list(range(n))
				if response != "reset": #reinicio de sesion
					sessions = sessions + 1
				else:
					continue

			print("sending random book to client", end = ":")
			index = random.randint(0, len(book_list) - 1) 
			print("INDEX ", index)
			book_number = book_list.pop(index)
			if len(book_list) == 0:
				data = (get_book_info(book_number) + " last_book").encode()
			else:
				data = get_book_info(book_number).encode() #guardar en base de datos la informacion de peticion
			#libro pedido, hora, direccion del usuario, sesion y no se que mas
			c.change_image(book_number)
			print(data)
			connection.sendall(data)
		finally:
			connection.close()

def get_book_info(id_book):
	#Sacar info de la base de datos o algo xd
	return str(id_book) + " info bien pro"

listen = threading.Thread(target = listening)
listen.start()

c.root.mainloop()