from GUI import GUI
from hashlib import sha256
from dataStructures import Employee, Equipment, Skill

DEBUG = True  # obviously for debugging...

class Manager:
    def __init__(self, checkoutLimit=5, lostLimit=3, equipment=None, employees=None, termEmployees=None, skills=None) -> None:
        self.window = GUI(self)
        
        self.checkoutLimit = checkoutLimit
        self.lostLimit = lostLimit

        if equipment is None:
            equipment = []
        self.equipment: list[Equipment] = equipment
        
        if employees is None:
            employees = []
        self.employees: list[Employee] = employees
        
        if termEmployees is None:
            termEmployees = []
        self.terminatedEmployees: list[Employee] = termEmployees
        
        if skills is None:
            skills: list[Skill] = []
        self.skills = skills

        self.current_user = None

        self.window.mainloop()


    def _set_current_user(self, user_id: str, pwd_hash: str) -> bool:
        if len(self.employees) == 0:
            return False
        for emp in self.employees:
            if emp.emp_id == user_id and emp.password_hash == pwd_hash:
                self.current_user = emp
                return True
        return False

    def login(self, user_id: str, pwd: str) -> bool:
        if len(user_id) == 0 or len(pwd) == 0:
            return False
        
        if DEBUG:
            print(f"Login Attempt:: User: {user_id}, Pass: {pwd}, Success: {self._set_current_user(user_id, pwd)}") 

        # TODO: pull credentials from a Database and check? maybe have creds stored locally? (obviously hashed...)
        if self._set_current_user(user_id, pwd):
            # TODO: logged In! so give the GUI the info for the user...
            self.window.main_menu_frame()


        return False # placeholder return value