import tkinter as tk
from tkinter.ttk import Frame, Label, Button, Style, Combobox
from tkinter import StringVar, Entry, Listbox, Scrollbar
from typing import Protocol
from hashlib import sha256
from dataStructures import Employee, Equipment, Skill, Log
from customWidgets import ListFrame
from Pipeline import AllFilters, Pipeline
from collections.abc import Callable 


DEBUG = False  # for debugging...

class Manager(Protocol):  # for accessing Manager class without circular importing error
    loggedIn: bool
    current_user: Employee
    equipment: list[Equipment] | None
    employees: list[Employee] | None
    skills: list[Skill] | None

    def login(self, user: str, pwd: str) -> bool:
        ...

    def getSkillByID(self, skill_id: str) -> Skill|None:
        ...
    
    def getEmployeeByID(self, emp_id: str) -> Employee|None:
        ...
    
    def getEquipmentByID(self, equip_id: str) -> Equipment|None:
        ...
    
    def checkIn(self, equip: Equipment, emp:Employee|None=None, notes: list[str]=[]):
        ...

    def checkout(self, equip: Equipment, emp: Employee|None, notes: list[str]=[]):
        ...

    def logLost(self, equip: Equipment, emp:Employee|None):
        ...
    
    def save_data_to_csv(self):
        ...

    def getLogs(self) -> list[Log]:
        ...
    
    def getNumEquipment(self) -> int:
        ...
    
    def getNumEmployees(self) -> int:
        ...
    
    def getNumSkills(self) -> int:
        ...
    
    def removeEquipment(self, equip, items):
        ...

    def removeSkill(self, skill, skills: list[Skill], items, selection_index, t):
        ...

def do_grid(root: Frame, cols: int, rows: int) -> None:  # creates a grid in root
        for i in range(cols):
            root.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            root.grid_rowconfigure(i, weight=1)

def new_label(root: Frame, text: str, textSize=20) -> Label:
    return Label(root, text=text, anchor="center", font=("Arial", textSize))

def new_button(root: Frame, text: str, command: callable, style: str = "a20.TButton", *args, **kwargs):
    return Button(root, text=text, command=command, style=style, *args, **kwargs)

class GUI(tk.Tk):
    WIDTH, HEIGHT = 1000, 800

    def __init__(self, manager: Manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.title("Equipment Checkout System")
        
        # window setup
        x = int(self.winfo_screenwidth()/2 - self.WIDTH/2)  
        y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        # self.resizable(False, False)  # not resizable ? 
        self.username, self.password = StringVar(self), StringVar(self)
        self.reusableStringVars = [StringVar(self) for _ in range(10)]
        self.current_frame: None|Frame = None

        s = Style()
        s.configure('a20.TButton', font=('Arial', 20))

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.login_frame()  # open login screen

    def on_close(self):
        self.manager.save_data_to_csv()
        self.destroy()

    def clear_current_frame(self) -> None:
        if self.current_frame is not None:
            for child in self.current_frame.winfo_children(): 
                child.destroy()
            col, row = self.current_frame.grid_size()
            for i in range(col):
                self.current_frame.grid_columnconfigure(i, weight=0)
            for i in range(row):
                self.current_frame.grid_rowconfigure(i, weight=0)
            # need to do this beacuse of ListFrame from customWidgets.py
            self.unbind_all('<MouseWheel>')  
            self.unbind_all('<Configure>')

            for var in self.reusableStringVars:
                var.set("")

        else:
            self.current_frame = Frame(self)
            self.current_frame.pack(fill="both", expand=True, padx=30, pady=30)

    def try_login(self):
        self.manager.login(self.username.get(), sha256(self.password.get().encode('utf-8')).hexdigest())
        self.username.set("")
        self.password.set("")
    
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

        login_button = new_button(root=self.current_frame, text="Login", command=self.try_login)
        login_button.grid(row=3, column=0, columnspan=6, sticky="nesw" , padx=40, pady=40)

    def main_menu_frame(self) -> None:
        self.clear_current_frame()

        btn_dicts = [
            {"text": "Check In Equipment",  "command": lambda : self.checkIn()},
            {"text": "Check Out Equipment", "command": lambda : self.checkOut()},
            {"text": "Reports",             "command": lambda : self.Reports()},
            {"text": "View User Details",   "command": lambda : self.UserDetails()},
            {"text": "Report Lost Equipment", "command": lambda: self.lostEquipment_selection()}
        ]

        if DEBUG:
            print(self.current_frame.grid_size())

        rows = len(btn_dicts) + 4
        if self.manager.current_user.isAdmin:
            rows += 1
        cols = 10
        do_grid(self.current_frame, cols=3, rows=rows)
    
        new_label(root=self.current_frame, text=f"Welcome, {self.manager.current_user.name}").grid(row=0, column=0, sticky="nesw", columnspan=int(2*cols/3))
        new_button(root=self.current_frame, text="Logout", command=self._logout).grid(row=0, column=int(2*cols/3), columnspan=int(cols/3), sticky="news")


        
        buttons = []
        for i, btn_dict in enumerate(btn_dicts):
            btn = new_button(root=self.current_frame, **btn_dict)
            btn.grid(row=i+2, column=0, sticky="nesw", columnspan=cols)
            buttons.append(btn)

        if self.manager.current_user.isAdmin:
            btn = new_button(root=self.current_frame, text="Manage Employees", command=lambda : self.ManageItems(t=Employee, items=self.manager.employees))
            btn.grid(row=i+3, column=0, sticky="nesw", columnspan=cols)

            btn = new_button(root=self.current_frame, text="Manage Equipment", command=lambda: self.ManageItems(t=Equipment, items=self.manager.equipment))
            btn.grid(row=i+4, column=0, sticky="nesw", columnspan=cols)

            btn = new_button(root=self.current_frame, text="Manage Skills", command=lambda: self.manageSkills(self.manager.skills, None, None, None))
            btn.grid(row=i+5, column=0, sticky="news", columnspan=cols)


    def _set_lost(self, equip: Equipment):
        # originally was gonna popup an error if I couldn't find the employee
        # but thought about situations where it was lost but never checked out, but still be marked as lost
        if equip.borrower_id is not None and (emp:=self.manager.getEmployeeByID(equip.borrower_id)) is not None:
            emp.numLostEquips += 1
        equip.isLost = True
        self.manager.logLost(equip=equip, emp=emp)

    def lostEquipment_selection(self, items: list[Equipment]=None, selection_index: int|None=None):
        if items is None:
            items = [self.manager.getEquipmentByID(x) for x in self.manager.current_user.borrowedEquipIds]
        do_success_popup = False
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=(cols:=2), rows=(rows:=4))
        if selection_index is not None: # selection is made
            self._set_lost(items[selection_index])
            do_success_popup=True
        new_label(root=self.current_frame, text="Select Equipment To Report As Lost").grid(row=0, column=0, columnspan=cols, sticky="nesw")
        subFrame = Frame(self.current_frame)
        subFrame.grid(row=1, column=0, columnspan=cols, sticky="nesw", rowspan=rows-2)
        buttons_data = [{"gui":self, "i":i, "items":items, "item":x} for i, x in enumerate(items)]
        ListFrame(parent=subFrame, buttons_data=buttons_data, item_height=100, isLost=True)
        new_button(root=self.current_frame, text="Back", command=self.main_menu_frame).grid(row=rows-1, column=0, columnspan=cols, sticky="nesw")
        if do_success_popup: # need to do popup last so it shows up
            self.popup("Successfully reported equipment as lost", isError=False)
        
        
        
    def _logout(self):
        self.manager.current_user = None
        self.login_frame()

    def popup(self, text: str, isError: bool=True) -> None:
        if self.current_frame is None:
            return
        s = Style()
        s.configure((style:='PopupError.TFrame'), background='#bf1143')
        s.configure('PopupMsg.TFrame', background='#16db20')
        if not isError:
            style = 'PopupMsg.TFrame'
        subFrame = Frame(master=self.current_frame, padding=20, borderwidth=2, style=style)
        subFrame.place(relheight=.8, relwidth=.8, relx=.1, rely=.1)

        do_grid(root=subFrame, cols=3, rows=3)

        new_label(root=subFrame, text=text).grid(row=0, column=0, columnspan=3, sticky="news")
        new_button(root=subFrame, text="Close", command=lambda: subFrame.destroy()).grid(row=2, column=0, columnspan=3)

    def checkIn(self) -> None:
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=(cols:=6), rows=(rows:=5))

        new_label(root=self.current_frame, text="Check-In").grid(row=0, column=0, columnspan=cols, sticky="nesw")

        new_label(root=self.current_frame, text="Select Equipment").grid(row=rows//2, column=0, columnspan=2)
        equips = [equip for equipID in self.manager.current_user.borrowedEquipIds if (equip:=self.manager.getEquipmentByID(equip_id=equipID)) is not None]
        values=[equip.name for equipID in self.manager.current_user.borrowedEquipIds if (equip:=self.manager.getEquipmentByID(equip_id=equipID)) is not None]
        combo = Combobox(master=self.current_frame, state="readonly", values=values, font=("Arial", 20), justify="center")
        combo.grid(row=rows//2, column=2, columnspan=cols-1, sticky="nesw")


        new_button(root=self.current_frame, text="Back", command=lambda : self.main_menu_frame()).grid(row=rows-1, column=0, columnspan=cols//2, sticky="nesw")
        new_button(root=self.current_frame, text="Check-In", command= lambda: self.manager.checkIn(equips[combo.current()])).grid(row=rows-1, column=cols//2, columnspan=cols//2, sticky="nesw")


    def checkOut(self) -> None:
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=(cols:=6), rows=(rows:=5))

        new_label(root=self.current_frame, text="Check-Out").grid(row=0, column=0, columnspan=cols, sticky="nesw")

        new_label(root=self.current_frame, text="Select Equipment").grid(row=rows//2, column=0, columnspan=2)
        equips = [equip for equip in self.manager.equipment if equip.borrower_id in [None, '']]
        values=[equip.name for equip in equips]
        combo = Combobox(master=self.current_frame, state="readonly", values=values, font=("Arial", 20), justify="center")
        combo.grid(row=rows//2, column=2, columnspan=cols-1, sticky="nesw")


        new_button(root=self.current_frame, text="Back", command=lambda : self.main_menu_frame()).grid(row=rows-1, column=0, columnspan=cols//2, sticky="nesw")
        new_button(root=self.current_frame, text="Check-Out", command= lambda: self.manager.checkout(equips[combo.current()])).grid(row=rows-1, column=cols//2, columnspan=cols//2, sticky="nesw")


    def Reports(self, UnselectedFilters:list[dict]=AllFilters, SelectedFilters:list[dict]=[]) -> None:
        def addFunc():
            SelectedFilters.append(UnselectedFilters.pop(comboUnselected.current()))
            self.Reports(UnselectedFilters=UnselectedFilters, SelectedFilters=SelectedFilters)
        def removeFunc():
            UnselectedFilters.append(SelectedFilters.pop(comboSelected.current()))
            self.Reports(UnselectedFilters=UnselectedFilters, SelectedFilters=SelectedFilters)

        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=(cols:=6), rows=(rows:=4))

        comboUnselected = Combobox(master=self.current_frame, state="readonly", values=[x['name'] for x in UnselectedFilters], font=("Arial", 20), justify="center")
        comboUnselected.grid(row=1, column=0, columnspan=2*cols//3, sticky="nesw")

        new_button(root=self.current_frame, text="Add", command=addFunc).grid(row=1, column=2*cols//3, columnspan=cols//3, sticky="news")

        comboSelected = Combobox(master=self.current_frame, state="readonly", values=[x['name'] for x in SelectedFilters], font=("Arial", 20), justify="center")
        comboSelected.grid(row=2, column=0, columnspan=2*cols//3, sticky="nesw")
        
        new_button(root=self.current_frame, text="Remove", command=removeFunc).grid(row=2, column=2*cols//3, columnspan=cols//3, sticky="news")

        new_button(root=self.current_frame, text="Back", command=self.main_menu_frame).grid(row=3, column=0, columnspan=cols//2, sticky="news")
        new_button(root=self.current_frame, text="Run Report", command=lambda: self.reportPage(UnselectedFilters=UnselectedFilters, SelectedFilters=SelectedFilters)).grid(row=3, column=cols//2, columnspan=cols//2, sticky="news")


    def reportPage(self, UnselectedFilters:list[dict], SelectedFilters:list[dict]):
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=(cols:=20), rows=(rows:=10))

        if len(SelectedFilters) == 0:
            self.popup(text="Report is blank.")
            self.Reports(UnselectedFilters=UnselectedFilters, SelectedFilters=SelectedFilters)
            return
        p = Pipeline(filters=[x['func'] for x in SelectedFilters], data=[self.manager.getLogs(), self.manager.getNumEmployees(), self.manager.getNumEquipment(), self.manager.getNumSkills()])
        report: dict = p.executeFilters()
        report['data'].pop('logs')
        vals = [f"{report['header']}"]
        for k,v in report['data'].items():
            if isinstance(v, list):
                vals.append(f"{k}")
                for item in v:
                    vals.append(f"     {item}")
            else:
                vals.append(f"{k} : {v}")
        lbox = Listbox(master=self.current_frame)
        lbox.grid(column=0, row=0, rowspan=rows-1, columnspan=cols-1, sticky="news")

        scrollbar = Scrollbar(self.current_frame)
        scrollbar.grid(column=cols-1, row=0, rowspan=rows-1, sticky="news")

        lbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=lbox.yview)

        for v in vals:
            lbox.insert('end', v)
        new_button(root=self.current_frame, text="Back", command=lambda: self.Reports(UnselectedFilters=UnselectedFilters, SelectedFilters=SelectedFilters)).grid(column=0, row=rows-1, columnspan=cols, sticky="news")
        


    def UserDetails(self) -> None:
        user = self.manager.current_user
        self.clear_current_frame()
        cols, rows = 6, 10
        do_grid(self.current_frame, cols=cols, rows=rows)
        new_label(self.current_frame, text=user.name).grid(column=0, row=0, columnspan=cols)

        new_label(self.current_frame, text="Name").grid(row=1, column=0, columnspan=int(cols/3), sticky="nesw")
        self.reusableStringVars[0].set(user.name)
        Entry(master=self.current_frame, textvariable=self.reusableStringVars[0], justify="center", font=("Arial", 20)).grid(row=1, column=int(cols/3), columnspan=int(2*cols/3), sticky="nesw")
        
        new_label(self.current_frame, text="Employee ID").grid(row=2, column=0, columnspan=int(cols/3), sticky="nesw")
        self.reusableStringVars[1].set(user.emp_id)
        if user.isAdmin:
            Entry(master=self.current_frame, textvariable=self.reusableStringVars[1], justify="center", font=("Arial", 20)).grid(row=2, column=int(cols/3), columnspan=int(2*cols/3), sticky="nesw")
        else:
            new_label(root=self.current_frame, text=user.emp_id).grid(row=2, column=int(cols/3), columnspan=int(2*cols/3), sticky="nesw")

        new_label(self.current_frame, text="Contact Info").grid(row=3, column=0, columnspan=int(cols/3), sticky="nesw")
        self.reusableStringVars[2].set(user.contactInfo)
        Entry(master=self.current_frame, textvariable=self.reusableStringVars[2], justify="center", font=("Arial", 20)).grid(row=3, column=int(cols/3), columnspan=int(2*cols/3), sticky="nesw")

        new_label(self.current_frame, text="Borrowed Equipment").grid(row=4, column=0, columnspan=int(cols/3), sticky="nesw")
        values=[equip.name for equipID in user.borrowedEquipIds if (equip:=self.manager.getEquipmentByID(equip_id=equipID)) is not None]
        if len(values) == 0:
            values = ["None"]
        combo = Combobox(master=self.current_frame, state="readonly", values=values, font=("Arial", 20), justify="center")
        combo.current(0 if len(values) > 0 else None)
        combo.grid(row=4, column=cols//3, columnspan=2*cols//3, sticky="nesw")

        new_label(self.current_frame, text=f"Number of Lost Equipment: {user.numLostEquips}").grid(row=5, column=0, columnspan=cols, sticky="news")

        new_button(self.current_frame, text="Change Password", command=lambda: self._change_password(items=[user], selection_index=0, isUserDetails=True)).grid(row=6, column=0, columnspan=cols, sticky="news")

        new_button(root=self.current_frame, text="Back", command=lambda: self.main_menu_frame()).grid(column=0, row=rows-1, columnspan=cols//2, sticky="nesw") # back button
        new_button(root=self.current_frame, text="Save", command=lambda: self._save_changes(savingObj=user)).grid(column=cols//2, row=rows-1, columnspan=cols//2, sticky="nesw") # save button
        

    
    def ManageItems(self, t, items: list[Equipment|Employee]=None, selection_index: None|int=None) -> None:  # this function handles Equipment and Employee obj Handling
        if selection_index is None:
            self._getSelection(items=items, t=t)
            return
        if DEBUG:
            print(f"Selection Index: {selection_index}")
        
        self.clear_current_frame()
        cols, rows = 6, 10
        do_grid(self.current_frame, cols=cols, rows=rows)
        new_label(self.current_frame, text=items[selection_index].name).grid(column=0, row=0, columnspan=cols)
        new_button(root=self.current_frame, text="Back", command=lambda: self.ManageItems(t=t, items=items, selection_index=None)).grid(column=0, row=rows-1, columnspan=cols//2, sticky="nesw") # back button
        new_button(root=self.current_frame, text="Save", command=lambda: self._save_changes(savingObj=items[selection_index])).grid(column=cols//2, row=rows-1, columnspan=cols//2, sticky="nesw") # save button
        if isinstance(items[0], Employee): # Selection is Employee
            new_label(self.current_frame, text="Name").grid(row=1, column=0, columnspan=cols//3, sticky="nesw")
            self.reusableStringVars[0].set(items[selection_index].name)
            Entry(master=self.current_frame, textvariable=self.reusableStringVars[0], justify="center", font=("Arial", 20)).grid(row=1, column=cols//3, columnspan=2*cols//3, sticky="nesw")
            
            new_label(self.current_frame, text="Employee ID").grid(row=2, column=0, columnspan=cols//3, sticky="nesw")
            self.reusableStringVars[1].set(items[selection_index].emp_id)
            Entry(master=self.current_frame, textvariable=self.reusableStringVars[1], justify="center", font=("Arial", 20)).grid(row=2, column=cols//3, columnspan=2*cols//3, sticky="nesw")

            new_label(self.current_frame, text="Contact Info").grid(row=3, column=0, columnspan=cols//3, sticky="nesw")
            self.reusableStringVars[2].set(items[selection_index].contactInfo)
            Entry(master=self.current_frame, textvariable=self.reusableStringVars[2], justify="center", font=("Arial", 20)).grid(row=3, column=cols//3, columnspan=2*cols//3, sticky="nesw")

            new_label(self.current_frame, text="Borrowed Equipment").grid(row=4, column=0, columnspan=cols//3, sticky="nesw")
            values=[equip.name for equipID in items[selection_index].borrowedEquipIds if (equip:=self.manager.getEquipmentByID(equip_id=equipID)) is not None]
            if len(values) == 0:
                values = ["None"]
            combo = Combobox(master=self.current_frame, state="readonly", values=values, font=("Arial", 20), justify="center")
            combo.current(0 if len(values) > 0 else None)
            combo.grid(row=4, column=cols//3, columnspan=2*cols//3, sticky="nesw")

            new_label(self.current_frame, text=f"Number of Lost Equipment: {items[selection_index].numLostEquips}").grid(row=5, column=0, columnspan=cols, sticky="news")

            new_button(self.current_frame, text="Edit Skills", command=lambda: self.editSkills(currentObj=items[selection_index], items=items, selection_index=selection_index, t=t)).grid(row=6, column=0, columnspan=cols//2, sticky="nesw")

            new_button(self.current_frame, text="Change Password", command=lambda: self._change_password(items=items, selection_index=selection_index)).grid(row=6, column=cols//2, columnspan=cols//2, sticky="nesw")

            toggle_admin = lambda: (v:=self.reusableStringVars[3]).set("True" if v.get() == "False" else "False")

            new_label(root=self.current_frame, text="Admin Privildges").grid(row=7, column=0, columnspan=cols//2, sticky="news")
            self.reusableStringVars[3].set(f"{items[selection_index].isAdmin}")
            new_button(self.current_frame, text="", command=toggle_admin, textvariable=self.reusableStringVars[3]).grid(row=7, column=cols//2, columnspan=cols//2, sticky="news")

            new_button(root=self.current_frame, text="DELETE USER", command=lambda: self.manager.removeEmp(items[selection_index], items)).grid(row=8, column=0, columnspan=cols, sticky="news")

        elif isinstance(items[0], Equipment): # Selection is Equipment
            new_label(self.current_frame, text="Name").grid(row=1, column=0, columnspan=cols//3, sticky="nesw")
            self.reusableStringVars[0].set(items[selection_index].name)
            Entry(master=self.current_frame, textvariable=self.reusableStringVars[0], justify="center", font=("Arial", 20)).grid(row=1, column=cols//3, columnspan=2*cols//3, sticky="nesw")
            
            new_label(self.current_frame, text="Equipment ID").grid(row=2, column=0, columnspan=cols//3, sticky="nesw")
            self.reusableStringVars[1].set(items[selection_index].equipId)
            Entry(master=self.current_frame, textvariable=self.reusableStringVars[1], justify="center", font=("Arial", 20)).grid(row=2, column=cols//3, columnspan=2*cols//3, sticky="nesw")
            text = f"Borrowed By: {emp.name if (emp := self.manager.getEmployeeByID(b_id:=items[selection_index].borrower_id)) is not None and b_id is not None else "Vacant"}"
            b_lab = new_label(self.current_frame, text=text)
            b_lab.grid(row=3, column=0, columnspan=cols, sticky="nesw")

            # TODO: add way to edit requirement skills for equipment

            new_label(self.current_frame, text="Queue").grid(row=4, column=0, columnspan=int(cols/3), sticky="nesw")
            values=[emp.name for empID in items[selection_index].queue if (emp:=self.manager.getEmployeeByID(emp_id=empID)) is not None]
            if len(values) == 0:
                values = ["None"]
            combo = Combobox(master=self.current_frame, state="readonly", values=values, font=("Arial", 20), justify="center")
            combo.current(0 if len(values) > 0 else None)
            combo.grid(row=4, column=cols//3, columnspan=2*cols//3, sticky="nesw")

            new_button(root=self.current_frame, text="DELETE EQUIPMENT", command=lambda: self.manager.removeEquipment(equip=items[selection_index], items=items)).grid(row=6, column=0, columnspan=cols, sticky="news")
        else:
            self.popup("Error : Selected Item isn't Equipment or Employee class for some reason...")  # this should never happen

    def editSkills(self, currentObj: Employee|Equipment, items, selection_index, t=None):
        if t == Employee:
            skills = currentObj.skillIds
        else:
            skills = currentObj.skillRequirementsIDs
        self.manageSkills(skills, items, selection_index, t)
        
    def editSkill(self, skill: Skill, skills: list[Skill], items, selection_index, t=None):
        self.clear_current_frame()
        do_grid(self.current_frame, cols=(cols:=3), rows=5)
        self.reusableStringVars[0].set(skill.name)
        self.reusableStringVars[1].set(skill.skillId)

        new_label(root=self.current_frame, text="Edit Skill").grid(row=0, column=0, columnspan=cols, sticky="news")

        new_label(root=self.current_frame, text="Name").grid(row=1, column=0, columnspan=1, sticky="news")
        Entry(master=self.current_frame, textvariable=self.reusableStringVars[0], justify="center", font=("Arial", 20)).grid(row=1, column=1, columnspan=cols-1, sticky="news")

        new_label(root=self.current_frame, text="Skill ID").grid(row=2, column=0, columnspan=1, sticky="news")
        Entry(master=self.current_frame, textvariable=self.reusableStringVars[1], justify="center", font=("Arial", 20)).grid(row=2, column=1, columnspan=cols-1, sticky="news")
        
        back_func = lambda: self.manageSkills(skills, items, selection_index, t)
        def saveSkill():
            # TODO: if skill id changes, need to find all references and change the references
            # TODO: need to check for clashes with skillIDs here
            skill.name = self.reusableStringVars[0].get()
            skill.skillId =  self.reusableStringVars[1].get()
            self.popup("Skill Saved Successfully", isError=False)

        new_button(root=self.current_frame, text="Save", command=saveSkill).grid(row=3, column=0, columnspan=cols, sticky="news")
        new_button(root=self.current_frame, text="Back", command=back_func).grid(row=4, column=0, columnspan=cols, sticky="news")

    def manageSkills(self, skills:list[Skill], items, selection_index, t=None):
        self.clear_current_frame()
        do_grid(self.current_frame, cols=(cols:=6), rows=(rows:=10))
        new_label(self.current_frame, text="Select Skill").grid(row=0, column=0, columnspan=cols, sticky="news")

        combo = Combobox(master=self.current_frame, state="readonly", values=[x.name for x in skills], font=("Arial", 20), justify="center")
        combo.current(0 if len(skills) > 0 else None)
        combo.grid(row=1, column=0, columnspan=cols, sticky="nesw")

        new_button(root=self.current_frame, text="Select", command=lambda: self.editSkill(skills[combo.current()], skills, items, selection_index, t) if len(skills)>0 else "").grid(row=3, column=0, columnspan=cols//2, sticky="news")
        
        new_button(root=self.current_frame, text="DELETE SKILL", command=lambda: self.manager.removeSkill(skills[combo.current()], skills, items, selection_index, t) if len(skills) > 0 else "").grid(row=3, column=cols//2, columnspan=cols//2, sticky="news")

        def newSkill():
            self.manager.skills.append((newSkill:=Skill(name="", skillId="")))
            self.editSkill(newSkill, skills=skills + [newSkill], items=items, selection_index=selection_index, t=t)
        new_button(root=self.current_frame, text="New Skill", command=newSkill).grid(row=8, column=0, columnspan=cols, sticky="news")
        new_button(root=self.current_frame, text="Back", command=lambda: self.ManageItems(t=t, items=items, selection_index=selection_index) if items is not None else self.main_menu_frame()).grid(row=9, column=0, columnspan=cols, sticky="news")
    
    def _getSelection(self, items: list[Equipment | Employee], t):
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=2, rows=6)
        new_label(root=self.current_frame, text="Make a Selection").grid(row=0, column=0, columnspan=2, sticky="nesw")
        subFrame = Frame(self.current_frame)
        subFrame.grid(row=1, column=0, columnspan=2, sticky="nesw", rowspan=4)
        buttons_data = [{"gui":self, "i":i, "items":items, "item":x, "t": t} for i, x in enumerate(items)]
        ListFrame(parent=subFrame, buttons_data=buttons_data, item_height=100)
        new_button(root=self.current_frame, text="Back", command=lambda: self.main_menu_frame()).grid(row=5, column=0, sticky="nesw")
        if t == Equipment:
            func = lambda: self.addNewEquipment(items=items)
        elif t == Employee: # instance of Employee
            func = lambda: self.addNewEmployee(items=items)
        else:
            self.popup("Something Went wrong...")
        
        new_button(root=self.current_frame, text="Add New", command=func).grid(row=5, column=1, sticky="nesw")
    
    def addNewEquipment(self, items: list[Equipment]):
        if not self.manager.current_user.isAdmin:
            self.popup("Admin Priviliges Needed")
            return
        equip = Equipment(equipId="", name="")
        self.manager.equipment.append(equip)
        self.ManageItems(t=Equipment, items=self.manager.equipment, selection_index=len(self.manager.equipment)-1)

    def addNewEmployee(self, items: list[Employee]):
        if not self.manager.current_user.isAdmin:
            self.popup("Admin Priviliges Needed")
            return
        emp = Employee(emp_id="", name="", password_hash=sha256("".encode('utf-8')).hexdigest(), contactInfo="")
        self.manager.employees.append(emp)
        self.ManageItems(t=Employee, items=self.manager.employees, selection_index=len(self.manager.employees)-1)
    
    def _save_changes(self, savingObj: Employee|Equipment):
        if isinstance(savingObj, Employee):
            vals = [var.get() for var in self.reusableStringVars[:4]]
            if vals[3]=="False" and savingObj.isAdmin and len([emp for emp in self.manager.employees if emp.isAdmin]) <= 1: # prevent zero admin accounts
                self.popup("Cannot remove admin priviledges of last admin")
                return

            savingObj.name = vals[0] # name
            # TODO: if ID changes need to look through and change references & check for clashes
            savingObj.emp_id = vals[1] # Emp ID 
            savingObj.contactInfo = vals[2] # contact Info
            
            savingObj.isAdmin = True if vals[3]=="True" else False # admin
        elif isinstance(savingObj, Equipment):
            vars = self.reusableStringVars[:2]
            vals = [var.get() for var in vars]
            savingObj.name = vals[0] # name
            # TODO: if ID changes need to look through and change references & check for clashes
            savingObj.equipId = vals[1] # equipment Id  
        else:
            self.popup("Error: Object typing isn't as expected") # This should never happen
            return
        self.popup("Successfully Saved", isError=False)

    def _not_implemented(self) -> None: # TODO: Delete me later | Temporary function
        self.clear_current_frame()
        do_grid(root=self.current_frame, cols=1, rows=4)

        lab = new_label(root=self.current_frame, text="Not Implemented yet...")
        lab.grid(row=1, column=0, sticky="nesw")

        but = new_button(root=self.current_frame, text="Main Menu", command=lambda: self.main_menu_frame())
        but.grid(row=2, column=0, sticky="nesw")
    
    def _change_password(self, items: list[Employee], selection_index: int, isUserDetails=False):
        self.clear_current_frame()
        do_grid(self.current_frame, cols=4, rows=4)

        new_label(root=self.current_frame, text="Change Password").grid(row=0, column=0, columnspan=3, sticky="news")

        new_label(root=self.current_frame, text="New Password").grid(row=1, column=0, sticky="news")
        p1 = Entry(master=self.current_frame, textvariable=self.reusableStringVars[0], justify="center", font=("Arial", 20), show="*")
        p1.grid(row=1, column=1, columnspan=2, sticky="nesw")
        p1_tog = lambda: p1.configure(show=("" if p1.cget("show")=="*" else "*")) # functionality to toggle showing password
        new_button(root=self.current_frame, text="Show", command=p1_tog).grid(row=1, column=4, sticky="news")

        new_label(root=self.current_frame, text="Confirm Password").grid(row=2, column=0, sticky="news")
        p2 = Entry(master=self.current_frame, textvariable=self.reusableStringVars[1], justify="center", font=("Arial", 20), show="*")
        p2.grid(row=2, column=1, columnspan=2, sticky="nesw")
        p2_tog = lambda: p2.configure(show=("" if p2.cget("show")=="*" else "*")) # functionality to toggle showing password
        new_button(root=self.current_frame, text="Show", command=p2_tog).grid(row=2, column=4, sticky="news")

        def func():
            if (txt:=self.reusableStringVars[0].get()) == self.reusableStringVars[1].get():
                (emp:=items[selection_index]).password_hash = sha256(txt.encode("utf-8")).hexdigest()
                if not isUserDetails:
                    self.ManageItems(t=Employee, items=items, selection_index=selection_index)
                else:
                    self.UserDetails()
                self.popup("Password Change Successful", isError=False)
            else:
                self.popup("Passwords do not match.")
        new_button(root=self.current_frame, text="Confirm", command=func).grid(row=3, column=0, columnspan=4, sticky="news")

    