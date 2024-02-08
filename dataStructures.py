from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class Employee:
    def __init__(self, name: str, password_hash: str, emp_id: str, contactInfo: str, borrowedEquipIds:list[str]|None=None, skillIds:list[str]|None=None, numLostEquips=0, isAdmin=False) -> None:
        self.name = name
        self.password_hash =password_hash
        self.emp_id: str = emp_id
        self.contactInfo: str = contactInfo
        if borrowedEquipIds is None:
            borrowedEquipIds = []
        if skillIds is None:
            skillIds = []
        self.borrowedEquipIds: list[str] = borrowedEquipIds
        self.skillIds: list[str] = skillIds
        self.numLostEquips = numLostEquips
        self.isAdmin = isAdmin
    
    def __repr__(self) -> str:
        return self.name

class Equipment:
    def __init__(self, equipId: str, name: str, borrower_id: None|str = None, skillRequirementsIDs: list[str]|None = None, queue: list[str]|None = None) -> None:
        self.equipId: str = equipId
        self.name: str = name
        self.borrower_id: str|None = borrower_id
        if skillRequirementsIDs is None:
            skillRequirementsIDs = []
        self.skillRequirementsIDs: list[str] = skillRequirementsIDs
        if queue is None:
            queue = []
        self.queue: list[str] = queue
    
    def __repr__(self) -> str:
        return self.name
    
    def getMissingSkills(self, emp: Employee) -> list[str]:
        missing = []
        for skill_id in self.skillRequirementsIDs:
            if skill_id not in emp.skillIds:
                missing.append(skill_id)
        return missing
    

@dataclass
class Skill:
    name: str
    skillId: str


class LOG_CODES(Enum):
    LOST = 0
    CHECKOUT = 1
    CHECKIN = 2

@dataclass
class Log:
    date: datetime
    logCode: int
    empId: str
    equipId: str
    notes: list[str]
