import socket
import sys
import time
import datetime
import threading
from clock import clock
from timeit import default_timer as timer 

clock_time = [11, 33, 22]
update_delay = 2
c = clock.BookClock("Book server", clock_time)
c.time()

def synchronize_time():
	while True:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = ('192.168.100.38', 8000)
			print('connecting to {} port {}'.format(*server_address))
			sock.connect(server_address)
			ct = datetime.datetime.now()
			t0 = timer()
			data = sock.recv(1024).decode().split(":")
			st = datetime.datetime.now()
			st = st.replace(hour = int(data[0]))
			st = st.replace(minute = int(data[1]))
			st = st.replace(second = int(data[2]))
			t1 = timer()
			latency = t1 - t0
			nt = st + datetime.timedelta(seconds = (latency / 2))
			print("data", data)
			print("last time", ct)
			print("latency", latency)
			print("server time", st)
			print("new time", nt)
			global clock_time
			clock_time[0] = nt.hour
			clock_time[1] = nt.minute
			clock_time[2] = nt.second
			global c
			c.current_time = clock_time
			data = "{}:{}|{}|{}|{}|{}".format(*server_address, ct, latency, st, nt)
			sock.sendall(data.encode())

		finally:
		    print('closing socket')
		    sock.close()
		    time.sleep(update_delay)

update_time = threading.Thread(target = synchronize_time)
update_time.start()
c.root.mainloop()