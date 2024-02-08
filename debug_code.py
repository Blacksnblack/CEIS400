from manager import Manager
from dataStructures import Employee, Equipment, Skill
from hashlib import sha256
from random import choice, randint # remove later

DEBUG = True

def get_debug_values():
    skills: list[Skill] = []
    for i in range(10): # create a bunch of skills for testing GUI
        skills.append(Skill(name=f"Skill {i}", skillId=str(i)))

    pass_hash = sha256("123".encode('utf-8')).hexdigest() # password is 123
    testEmp1 = Employee(name="Test User 0", password_hash=pass_hash, emp_id="0", contactInfo="email@email.com", isAdmin=False)  # temp user 1
    testEmp2 = Employee(name="Test Admin 1", password_hash=pass_hash, emp_id="1", contactInfo="email@email.com", isAdmin=True)  # temp user 2

    emps = [testEmp1, testEmp2]

    equips: list[Equipment] = []
    for i in range(30): # bunch of equipment for debugging manage Equipment GUI
        equips.append(Equipment(name=f"Equipment {i}", equipId=str(i)))

    # TODO: something not right here? equipment.borrower_id not matching employee.borrowedEquipIds 
    equip_used = []
    for i in range(2, 20): # create a bunch of users for testing manage Employees GUI with randomly chosen equipment that's borrowed
        b_equips = []
        if i != 2: # emp id = 2 will not have any equipment
            while True: # everyone else will have 1 equipment borrowed
                b_equip = choice(equips)
                if b_equip not in equip_used:
                    equip_used.append(b_equip)
                    break
                b_equip.borrower_id = str(i)
            b_equips.append(b_equip.equipId)
        if i == 3: # emp id = 3 will have 2 borrowed equipment
            b_equips.append(equips[-1].equipId)
            equip_used.append(equips[-1])

        emp_skills = list(set([choice(skills).skillId for _ in range(randint(0, int(len(skills)/2)))])) # get a random number of random skills (converted from list to set to list to remove doubles)
        emps.append(Employee(name=f"Test User {i}", password_hash=pass_hash, emp_id=f"{i}", contactInfo="email@gmail.com", isAdmin=False, skillIds=emp_skills, borrowedEquipIds=b_equips))
        
        
    
    if DEBUG:
        print(emps)

    return emps, skills, equips