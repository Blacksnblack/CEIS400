from manager import Manager
from dataStructures import Employee
from hashlib import sha256


def main():
    testEmp = Employee(name="Test User", password_hash=sha256("123".encode('utf-8')).hexdigest(), emp_id="0", contactInfo="email@email.com")  # temp user
    manager = Manager(employees=[testEmp])


if __name__ == "__main__":
    main()