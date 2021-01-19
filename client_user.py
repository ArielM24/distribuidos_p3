import socket
import sys
import time
import datetime
import threading
from tkinter import *

root = Tk()
root.geometry("600x300")
root.title("Get books")
lblData = Label(root, text = "Book info", font = ("Arial", 12, "italic"))
lblData.grid(row = 0, column = 0)

btnGet = Button(root, text = "Get a book", command = lambda: get_random_book())
btnGet.grid(row = 1, column = 0)

btnReset = Button(root, text = "Reset session", command = lambda: reset_session(), state = DISABLED)
btnReset.grid(row = 2, column = 0)

btnExit = Button(root, text = "Exit session", command = lambda: exit_session())
btnExit.grid(row = 3, column = 0)


def get_random_book():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('192.168.100.38', 9000)
		print('connecting to {} port {}'.format(*server_address))
		sock.connect(server_address)
		data = sock.recv(1024).decode()
		print(data)
		lblData.config(text = data, font = "Arial 12 bold")
		if "last" in data:
			lblData.config(text = data.replace("last_book", " No more books"), font = "Arial 12 bold")
			btnReset.config(state = "normal")
			btnGet.config(state = "disabled")
	finally:
		print("closing socket")
		sock.close()

def reset_session():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('192.168.100.38', 9000)
		print('connecting to {} port {}'.format(*server_address))
		sock.connect(server_address)
		sock.sendall("reset".encode())
		btnGet.config(state = "normal")
		btnReset.config(state = "disabled")
	finally:
		print("closing socket")
		sock.close()

def exit_session():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('192.168.100.38', 9000)
		print('connecting to {} port {}'.format(*server_address))
		sock.connect(server_address)
		sock.sendall("exit".encode())
		sys.exit()
	finally:
		print("closing socket")
		sock.close()

root.mainloop()