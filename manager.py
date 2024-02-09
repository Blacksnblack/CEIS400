from GUI import GUI
from hashlib import sha256
from dataStructures import Employee, Equipment, Skill, Log, LOG_CODES
from datetime import datetime
from csv_database import (
    read_employees_from_csv,
    write_employees_to_csv,
    read_equipment_from_csv,
    write_equipment_to_csv,
    read_skills_from_csv,
    write_skills_to_csv
)

DEBUG = True  # obviously for debugging...

class Manager:
    def __init__(self, checkoutLimit=1, lostLimit=3, equipment=None, employees=None, termEmployees=None, skills=None, logs=None) -> None:
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

        if logs is None:
            logs: list[Log] = []
        self.logs = logs

        self.current_user = None

        def load_data_from_csv(self):
            self.employees = read_employees_from_csv("employees.csv")
            self.equipment = read_equipment_from_csv("equipment.csv")
            self.skills = read_skills_from_csv("skills.csv")
            # Load other data from CSV files if and as needed

        def save_data_to_csv(self):
            write_employees_to_csv(self.employees, "employees.csv")
            write_equipment_to_csv(self.equipment, "equipment.csv")
            write_skills_to_csv(self.skills, "skills.csv")
            # Save other data to CSV files if and as needed

        self.load_data_from_csv()  # Load data from CSV files when the Manager instance is created/called

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
            return
        self.window.popup(text="Invalid Username or Password")



        return False # placeholder return value

    def getSkillByID(self, skill_id: str) -> Skill|None:
        for skill in self.skills:
            if skill.skillId == skill_id:
                return skill
        return None

    def getEmployeeByID(self, emp_id: str) -> Employee|None:
        for emp in self.employees:
            if emp.emp_id == emp_id:
                return emp
        return None

    def getEquipmentByID(self, equip_id: str) -> Equipment|None:
        for equip in self.equipment:
            if equip.equipId == equip_id:
                return equip
        return None

    def checkIn(self, equip: Equipment, emp:Employee|None=None, notes: list[str]=[]) -> None:
        if emp is None:
            emp = self.current_user

        # handle errors
        error_msg = ""
        if equip.borrower_id is None:
            error_msg += "Equipment is already checked out.\n"
        if equip.equipId not in emp.borrowedEquipIds:
            error_msg += "Employee doesn't have equipment checked out."

        if error_msg != "":
            self.window.popup(error_msg)
            return

        # logs
        self.logs.append(Log(date=datetime.now(), logCode=LOG_CODES.CHECKIN, empId=emp.emp_id, equipId=equip.equipId, notes=notes))

        # finish
        equip.borrower_id = None
        emp.borrowedEquipIds.remove(equip.equipId)

        self.window.checkIn()
        self.window.popup(text="Check In Successful", isError=False)

    def checkout(self, equip: Equipment, emp: Employee|None=None, notes: list[str]=[]) -> None:
        """
        Returns a bool if successful and a string of the error, if error else blank str
        """
        if emp is None:
            emp = self.current_user

        # handle errors
        error_msg = ""
        if equip.borrower_id is not None:
            error_msg += "Equipment is not available.\n"
        if emp.numLostEquips > self.lostLimit:
            error_msg += "Employee cannot checkout due to lost limitations.\n"
        if len(emp.borrowedEquipIds) > self.checkoutLimit:
           error_msg += "Employee cannot checkout due to checkout limitations.\n"
        missing_skills = equip.getMissingSkills(emp=emp)
        if len(missing_skills) != 0:
            error_msg += f"Missing skills for Equipment: \n {'\n'.join(['   ' + self.getSkillByID(skillID).name for skillID in missing_skills])}"

        if error_msg != "":
            self.window.popup(text=error_msg)
            return

        #logs
        self.logs.append(Log(date=datetime.now(), logCode=LOG_CODES.CHECKOUT, empId=emp.emp_id, equipId=equip.equipId, notes=notes))

        # finish
        equip.borrower_id = emp.emp_id
        emp.borrowedEquipIds.append(equip.equipId)

        self.window.checkOut()
        self.window.popup(text="Check Out Successful", isError=False)

    def logLost(self, equip: Equipment, emp:Employee|None, notes: list[str]=[]):
        self.logs.append(Log(date=datetime.now(), logCode=LOG_CODES.LOST, empId=emp.emp_id, equipId=equip.equipId, notes=notes))


