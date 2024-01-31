import tkinter as tk


class GUI(tk.Tk):
    SIZE = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Test")
        
        # Set size and center app on screen on startup
        x = int(self.winfo_screenwidth()/2 - self.SIZE/2)  
        y = int(self.winfo_screenheight()/2 - self.SIZE/2)
        self.geometry(f"{self.SIZE}x{self.SIZE}+{x}+{y}")
        

        


class Manager:
    window = GUI()
    window.mainloop()

