from GUI import GUI
from hashlib import sha256
from dataStructures import Employee, Equipment, Skill

U, P = "test", sha256("123".encode('utf-8')).hexdigest()  # placeholder user and password
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

        self.window.mainloop()


        

    def login(self, user: str, pwd: str) -> bool:
        if len(user) == 0 or len(pwd) == 0:
            return False
        
        if DEBUG:
            print(f"Login Attempt:: User: {user}, Pass: {pwd}") 

        # TODO: pull credentials from a Database and check? maybe have creds stored locally? (obviously hashed...)
        if user == U and pwd == P:
            # TODO: logged In! so give the GUI the info for the user...
            self.window.main_menu_frame()


        return False # placeholder return value