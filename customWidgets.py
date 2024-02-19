# SOURCE: https://github.com/clear-code-projects/tkinter-complete/blob/main/2%20layout/2_13_scrollable_widgets.py

import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Button

# exercise
# create a scrollbar

class ListFrame(ttk.Frame):
	def __init__(self, parent, buttons_data, item_height, isLost=False):
		self.isLost= isLost
		super().__init__(master = parent)
		self.pack(expand = True, fill = 'both')

		# widget data
		self.buttons_data = buttons_data
		self.item_number = len(buttons_data)
		self.list_height = self.item_number * item_height

		# canvas 
		self.canvas = tk.Canvas(self, background = 'red', scrollregion = (0,0,self.winfo_width(),self.list_height))
		self.canvas.pack(expand = True, fill = 'both')

		# display frame
		self.frame = ttk.Frame(self)

		self.addButtons()

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

	def addButtons(self):
		for button in self.buttons_data:
			frame = ttk.Frame(self.frame)
			# grid layout
			frame.rowconfigure(0, weight = 1)
			frame.columnconfigure((0,), weight = 1)
			if self.isLost:
				lostEquipmentButtonVar(frame=frame, **button).grid(row = 0, column = 0, sticky = 'nsew')
			else:
				ButtonVar(frame=frame, **button).grid(row = 0, column = 0, sticky = 'nsew')
			
			frame.pack(expand = True, fill = 'both', pady =  4, padx = 10)


class ButtonVar(Button):
	def __init__(self, frame, item, i, gui, items, t, *args, **kwargs):
		super().__init__(master=frame, text=f'{item}', command=lambda: gui.ManageItems(t=t, items=items, selection_index=i) , style="a20.TButton", *args, **kwargs)


class lostEquipmentButtonVar(Button):
	def __init__(self, frame, item, i, gui, items, *args, **kwargs):
		super().__init__(master=frame, text=f'{item}', command=lambda: gui.lostEquipment_selection(items=items, selection_index=i) , style="a20.TButton", *args, **kwargs)