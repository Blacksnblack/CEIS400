from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class Employee:
    def __init__(self, name: str, emp_id: int, contactInfo: str, borrowedEquipIds=None, skillIds=None, numLostEquips=0) -> None:
        self.name = name
        self.emp_id: int = emp_id
        self.contactInfo: str = contactInfo
        if borrowedEquipIds is None:
            borrowedEquipIds = []
        if skillIds is None:
            skillIds = []
        self.borrowedEquipIds: list[int] = borrowedEquipIds
        self.skillIds: list[int] = skillIds
        self.numLostEquips = numLostEquips
    
    def __repr__(self) -> str:
        return self.name

class Equipment:
    def __init__(self, equipId: int, name: str, borrower: None|int = None, skillRequirements = None, queue = None) -> None:
        self.equipId = equipId
        self.name = name
        self.borrower: int|None = borrower
        if skillRequirements is None:
            skillRequirements = []
        self.skillRequirements = skillRequirements
        if queue is None:
            queue = []
        self.queue = queue
    
    def __repr__(self) -> str:
        return self.name
    
    def getMissingSkills(self, emp: Employee) -> list[int]:
        missing = []
        for skill_id in self.skillRequirements:
            if skill_id not in emp.skillIds:
                missing.append(skill_id)
        return missing
    

@dataclass
class Skill:
    name: str
    skillId: int


class LOG_CODES(Enum):
    LOST = 0
    CHECKOUT = 1
    CHECKIN = 2

@dataclass
class log:
    date: datetime
    logCode: int
    empId: int
    equipId: int
    notes: list[str]
