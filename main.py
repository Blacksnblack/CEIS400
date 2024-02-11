from manager import Manager
from dataStructures import Employee, Equipment, Skill
from hashlib import sha256
from debug_code import get_debug_values

DEBUG = False

def main():
    emps, skills, equips = [], [], [] # Note: without any employee objs, you cannot loggin...
    if DEBUG:
        emps, skills, equips = get_debug_values()
    Manager(employees=emps, equipment=equips, skills=skills)


if __name__ == "__main__":
    main()