import tkinter as tk
import os, sys


"""if os.environ.get('DISPLAY','') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')
"""
class GUI(tk.Tk):
    WIDTH, HEIGHT = 300, 300

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Test")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        


class Manager:
    window = GUI()

