# SOURCE: https://github.com/clear-code-projects/tkinter-complete/blob/main/2%20layout/2_13_scrollable_widgets.py

import tkinter as tk
from tkinter import ttk

# exercise
# create a scrollbar

class ListFrame(ttk.Frame):
	def __init__(self, parent, text_data, item_height):
		super().__init__(master = parent)
		self.pack(expand = True, fill = 'both')

		# widget data
		self.text_data = text_data
		self.item_number = len(text_data)
		self.list_height = self.item_number * item_height

		# canvas 
		self.canvas = tk.Canvas(self, background = 'red', scrollregion = (0,0,self.winfo_width(),self.list_height))
		self.canvas.pack(expand = True, fill = 'both')

		# display frame
		self.frame = ttk.Frame(self)
		
		for item in self.text_data:
			self.create_item(item=item["text"], command=item["command"]).pack(expand = True, fill = 'both', pady =  4, padx = 10)

		# scrollbar 
		self.scrollbar = ttk.Scrollbar(self, orient = 'vertical', command = self.canvas.yview)
		self.canvas.configure(yscrollcommand = self.scrollbar.set)
		self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')

		# events
		self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
		self.bind('<Configure>', self.update_size)

	def update_size(self, event):
		if self.list_height >= self.winfo_height():
			height = self.list_height
			self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
			self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')
		else:
			height = self.winfo_height()
			self.canvas.unbind_all('<MouseWheel>')
			self.scrollbar.place_forget()
		
		self.canvas.create_window(
			(0,0), 
			window = self.frame, 
			anchor = 'nw', 
			width = self.winfo_width(), 
			height = height)

	def create_item(self, item, command):
		frame = ttk.Frame(self.frame)
		# grid layout
		frame.rowconfigure(0, weight = 1)
		frame.columnconfigure((0,), weight = 1, uniform = 'a')

		# widgets 
		# ttk.Label(frame, text = f'#{index}').grid(row = 0, column = 0)
		# ttk.Label(frame, text = f'{item[0]}').grid(row = 0, column = 1)
		ttk.Button(frame, text = f'{item}', command=command).grid(row = 0, column = 0, sticky = 'nsew')
		
		return frame