from tkinter import *
import threading
from PIL import Image, ImageTk

class Clock():
	def __init__(self, title, current_time):
		self.root = Tk()
		self.root.geometry("350x250")
		self.root.title(title)

		self.clock = Label(self.root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
		self.clock.grid(row = 0, column = 0, pady = 25, padx = 25)
		self.current_time = current_time
		self.delay = 1000
		self.strtime = "{}:{}:{}".format(current_time[0], current_time[1], current_time[2])

		self.lblNew = Label(self.root, text = "New hour for clock (H:M:S)", pady = 10)
		self.lblNew.grid(row = 1, column = 0)
		self.str_hour = StringVar()
		self.entry_hour = Entry(self.root, textvariable = self.str_hour)
		self.entry_hour.grid(row = 2, column = 0)
		self.btnChange = Button(self.root, text = "Change hour", command = lambda: self.getHour())
		self.btnChange.grid(row = 3, column = 0)

	def getHour(self):
		h, m, s = self.str_hour.get().split(":")
		h = int(h)
		m = int(m)
		s = int(s)
		self.current_time = [h,m,s] #guardar en la base de datos reloj el ajuste

	def update_clock(self):
	    self.current_time[2] += 1
	    if self.current_time[2] > 59:
	        self.current_time[2] = 0
	        self.current_time[1] += 1
	        if self.current_time[1] > 59:
	            self.current_time[1] = 0
	            self.current_time[0] += 1
	            if self.current_time[0] > 23:
	                self.current_time[0] = 0
	    strh = str(self.current_time[0]) if self.current_time[0] > 9 else "0" + str(self.current_time[0])
	    strm = str(self.current_time[1]) if self.current_time[1] > 9 else "0" + str(self.current_time[1])
	    strs = str(self.current_time[2]) if self.current_time[2] > 9 else "0" + str(self.current_time[2])
	    self.strtime = strh + ":" + strm + ":" + strs


	def time(self):
	    self.update_clock()
	    self.clock.config(text = self.strtime, bg = "black", fg = "green", font = "Arial 50 bold")
	    self.clock.after(self.delay, self.time)

class BookClock(Clock):
	def __init__(self, title, current_time):
		Clock.__init__(self, title, current_time)
		self.root.geometry("350x500")
		self.canvas = Label(self.root, text = "a")
		self.canvas.grid(row = 4, column = 0)
		img = ImageTk.PhotoImage(Image.open("faro.jpg"))
		self.canvas.image = img

