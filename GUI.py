import tkinter as tk
from tkinter.ttk import Frame, Label, Button, Style
from tkinter import StringVar, Entry
from typing import Protocol


class Manager(Protocol):
    loggedIn: bool

    def check_password(self, user: str, pwd: str) -> bool:
        ...

    
def do_grid(root: Frame, cols: int, rows: int) -> None:
        for i in range(cols):
            root.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            root.grid_rowconfigure(i, weight=1)

def new_label(root, text, textSize=20):
    return Label(root, text=text, anchor="center", font=("Arial", textSize))

class GUI(tk.Tk):
    WIDTH, HEIGHT = 1000, 800

    def __init__(self, manager: Manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.title("Test")
        
        # window setup
        x = int(self.winfo_screenwidth()/2 - self.WIDTH/2)  
        y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        # self.resizable(False, False)  # not resizable ? 
        self.username = StringVar(self)
        self.password = StringVar(self)
        self.current_frame: None | Frame = None

        s = Style()
        s.configure('a20.TButton', font=('Arial', 20))

        self.login_frame()  # open login screen
    
    def clear_current_frame(self) -> None:
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Frame(self)
        self.current_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    def login_frame(self) -> None:
        self.clear_current_frame()

        do_grid(root=self.current_frame, cols=6, rows=4)

        login_text = new_label(self.current_frame, text="Login", textSize=30)
        login_text.grid(row=0, column=0, columnspan=6, sticky="nesw")
        
        user_text = new_label(self.current_frame, text="Username")
        user_text.grid(row=1, column=0, columnspan=2, sticky="nesw")

        user_entry = Entry(self.current_frame, textvariable=self.username, justify="center", font=("Arial", 30))
        user_entry.grid(row=1, column=2, columnspan=3, sticky="nesw")

        pass_text = new_label(self.current_frame, text="Password")
        pass_text.grid(row=2, column=0, columnspan=2, sticky="nesw")

        pass_entry = Entry(self.current_frame, textvariable=self.password, justify="center", font=("Arial", 30), show="*")
        pass_entry.grid(row=2, column=2, columnspan=3, sticky="nesw")

        def show_toggle():
            if pass_entry.cget("show") == "*":
                pass_entry.configure(show="")
            else:
                pass_entry.configure(show="*")

        show_password_btn = Button(self.current_frame, text="Show", command=show_toggle, style="a20.TButton")
        show_password_btn.grid(row=2, column=5, columnspan=1, sticky="nesw", padx=10, pady=10)

       
        login_button = Button(self.current_frame, text="Login", command=lambda : self.manager.check_password(self.username.get(), self.password.get()), style="a20.TButton")
        login_button.grid(row=3, column=0, columnspan=6, sticky="nesw" , padx=40, pady=40)

    def main_frame(self) -> None:
        self.clear_current_frame()
        
        do_grid(self.current_frame, 1, 3)

        test_label = Label(self.current_frame, text=f"You logged in {self.username.get()}!", font=("Arial", 30), justify="center")
        test_label.grid(row=0, column=0)