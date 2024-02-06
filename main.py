from manager import Manager
from dataStructures import Employee
from hashlib import sha256


def main():
    pass_hash = sha256("123".encode('utf-8')).hexdigest() # password is 123
    testEmp1 = Employee(name="Test User 1", password_hash=pass_hash, emp_id="0", contactInfo="email@email.com", isAdmin=False)  # temp user 1
    testEmp2 = Employee(name="Test User 2", password_hash=pass_hash, emp_id="1", contactInfo="email@email.com", isAdmin=True)  # temp user 2

    emps = [testEmp1, testEmp2]

    for i in range(20): # create a bunch of users for testing manage Employees GUI
        emps.append(Employee(name=f"Test User {i+2}", password_hash=pass_hash, emp_id=f"{i+2}", contactInfo="email@gmail.com", isAdmin=False))
    manager = Manager(employees=emps)


if __name__ == "__main__":
    main()