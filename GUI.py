import tkinter as tk
from tkinter.ttk import Frame, Label, Button, Style
from tkinter import StringVar, Entry, Scrollbar
from typing import Protocol
from hashlib import sha256
from dataStructures import Employee, Equipment, Skill
from customWidgets import ListFrame


DEBUG = True  # for debugging...

class Manager(Protocol):  # for accessing Manager class without circular importing error
    loggedIn: bool
    current_user: Employee
    equipment: list[Equipment] | None
    employees: list[Employee] | None

    def login(self, user: str, pwd: str) -> bool:
        ...


    
def do_grid(root: Frame, cols: int, rows: int) -> None:  # creates a grid in root
        for i in range(cols):
            root.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            root.grid_rowconfigure(i, weight=1)

def new_label(root: Frame, text: str, textSize=20) -> Label:
    return Label(root, text=text, anchor="center", font=("Arial", textSize))

def new_button(root: Frame, text: str, command: callable, style: str = "a20.TButton"):
    return Button(root, text=text, command=command, style=style)

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
        self.username, self.password = StringVar(self), StringVar(self)
        self.current_frame: None|Frame = None

        s = Style()
        s.configure('a20.TButton', font=('Arial', 20))

        self.login_frame()  # open login screen

    
    def clear_current_frame(self) -> None:
        if self.current_frame is not None:
            for child in self.current_frame.winfo_children(): 
                child.destroy()
            col, row = self.current_frame.grid_size()
            for i in range(col):
                self.current_frame.grid_columnconfigure(i, weight=0)
            for i in range(row):
                self.current_frame.grid_rowconfigure(i, weight=0)

        else:
            self.current_frame = Frame(self)
            self.current_frame.pack(fill="both", expand=True, padx=30, pady=30)

    
    def login_frame(self) -> None:
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=6, rows=4)

        login_text = new_label(self.current_frame, text="Login", textSize=30)
        login_text.grid(row=0, column=0, columnspan=6, sticky="nesw")
        
        user_text = new_label(self.current_frame, text="User ID")
        user_text.grid(row=1, column=0, columnspan=2, sticky="nesw")

        user_entry = Entry(self.current_frame, textvariable=self.username, justify="center", font=("Arial", 30))
        user_entry.grid(row=1, column=2, columnspan=3, sticky="nesw")

        pass_text = new_label(self.current_frame, text="Password")
        pass_text.grid(row=2, column=0, columnspan=2, sticky="nesw")

        pass_entry = Entry(self.current_frame, textvariable=self.password, justify="center", font=("Arial", 30), show="*")
        pass_entry.grid(row=2, column=2, columnspan=3, sticky="nesw")

        show_toggle = lambda: pass_entry.configure(show=("" if pass_entry.cget("show")=="*" else "*")) # functionality to toggle showing password
        show_password_btn = new_button(root=self.current_frame, text="Show", command=show_toggle)
        show_password_btn.grid(row=2, column=5, columnspan=1, sticky="nesw", padx=10, pady=10)

        try_login = lambda : self.manager.login(self.username.get(), sha256(self.password.get().encode('utf-8')).hexdigest())
        login_button = new_button(root=self.current_frame, text="Login", command=try_login)
        login_button.grid(row=3, column=0, columnspan=6, sticky="nesw" , padx=40, pady=40)

    def main_menu_frame(self) -> None:
        """
        * After the user has logged in, we don't need to ask who is doing the action *
        

        Main Menu functionality needed:
        - checking an equipment in and out
        - a way for the user to get a notification that the equipment they have queued for is available
        - check user auth level
            - if supervisor or higher (ex: HR)
                - ability to terminate an employee
                - search for equipment details and current ownership and vise - versa for ALL employees
                    - including employees with excess equipment losses
                - update employee's skills
        - way to generate reports and decide on what filters to use or what to search for
        - ability to see user's currently checked-out equipment
        """
        self.clear_current_frame()

        btn_dicts = [
            {"text": "Check In Equipment",  "command": lambda : self.checkIn()},
            {"text": "Check Out Equipment", "command": lambda : self.checkOut()},
            {"text": "Reports",             "command": lambda : self.Reports()},
            {"text": "View User Details",   "command": lambda : self.UserDetails()}
        ]

        if DEBUG:
            print(self.current_frame.grid_size())

        rows = len(btn_dicts) + 3
        if self.manager.current_user.isAdmin:
            rows += 1
        do_grid(self.current_frame, cols=2, rows=rows)
    
        welcome_label = new_label(root=self.current_frame, text=f"Welcome, {self.manager.current_user.name}")
        welcome_label.grid(row=0, column=0, sticky="nesw", columnspan=2)

        
        buttons = []
        for i, btn_dict in enumerate(btn_dicts):
            btn = new_button(root=self.current_frame, **btn_dict)
            btn.grid(row=i+2, column=0, sticky="nesw", columnspan=2)
            buttons.append(btn)

        if self.manager.current_user.isAdmin:
            btn = new_button(root=self.current_frame, text="Manage Employees", command=lambda : self.ManageItems(items=self.manager.employees))
            btn.grid(row=i+3, column=0, sticky="nesw", columnspan=2)

            btn = new_button(root=self.current_frame, text="Manage Equipment", command=lambda: self.ManageItems(items=self.manager.equipment))
            btn.grid(row=i+4, column=0, sticky="nesw", columnspan=2)


    # TODO: replace self._not_implemented() with actualy functionality...
    def checkIn(self) -> None:
        self.clear_current_frame()
        self._not_implemented()

    def checkOut(self) -> None:
        self.clear_current_frame()
        self._not_implemented()

    def Reports(self) -> None:
        self.clear_current_frame()
        self._not_implemented()

    def UserDetails(self) -> None:
        self.clear_current_frame()
        self._not_implemented()
    
    def ManageItems(self, items: list[Equipment|Employee]=None, selection: None|Equipment|Employee=None) -> None:
        if selection is None:
            self._getSelection(items=items)
            return
        
        # TODO: create entry's depending on if it's an Employee or an Equipment
        # there is a selection but is it employee or equipment
        self.clear_current_frame()
        if isinstance(selection, Employee):
            lab = new_label(self.current_frame, text=selection.name)
            lab.pack()
            pass
        elif isinstance(selection, Equipment):
            pass
        else:
            print("Error : Selected Item isn't Equipment or Employee class for some reason...")  # this should never happen

    
    def _getSelection(self, items: list[Equipment | Employee]):
        self.clear_current_frame()

        do_grid(root=self.current_frame, cols=1, rows=5)

        lab = new_label(root=self.current_frame, text="Selection")
        lab.grid(row=0, column=0, sticky="nesw")

        subFrame = Frame(self.current_frame)  
        data=[{"text": x.name, "command": lambda: self.ManageItems(selection=x)} for x in items]  #TODO: passing command is broken; only remembers last one for some reason?
        print(data)
        lf = ListFrame(parent=subFrame, text_data=data, item_height=100)


        subFrame.grid(row=1, column=0, sticky="nesw", rowspan=4)
            # TODO create list of buttons with the command being lambda: self.ManageItems(selection=item)
        
        # self._not_implemented()


    def _not_implemented(self) -> None:
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=1, rows=4)

        lab = new_label(root=self.current_frame, text="Not Implemented yet...")
        lab.grid(row=1, column=0, sticky="nesw")

        but = new_button(root=self.current_frame, text="Main Menu", command=lambda: self.main_menu_frame())
        but.grid(row=2, column=0, sticky="nesw")

    