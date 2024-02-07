from manager import Manager
from dataStructures import Employee, Equipment
from hashlib import sha256


def main():
    pass_hash = sha256("123".encode('utf-8')).hexdigest() # password is 123
    testEmp1 = Employee(name="Test User 0", password_hash=pass_hash, emp_id="0", contactInfo="email@email.com", isAdmin=False)  # temp user 1
    testEmp2 = Employee(name="Test Admin 1", password_hash=pass_hash, emp_id="1", contactInfo="email@email.com", isAdmin=True)  # temp user 2

    emps = [testEmp1, testEmp2]

    for i in range(2, 20): # create a bunch of users for testing manage Employees GUI
        emps.append(Employee(name=f"Test User {i}", password_hash=pass_hash, emp_id=f"{i}", contactInfo="email@gmail.com", isAdmin=False))
    print(emps)
    equips = []
    for i in range(10): # bunch of equipment for debugging manage Equipment GUI
        equips.append(Equipment(name=f"Equipment {i}", equipId=str(i)))

    manager = Manager(employees=emps, equipment=equips)


if __name__ == "__main__":
    main()