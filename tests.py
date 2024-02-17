from dataStructures import *
from GUI import *
from manager import *
from Pipeline import *
from csv_database import *
from os import remove


def test_getMissingSkills(): # Here's an example to test the "getMissingSkills" function in dataStructures.py in the Equipment class
    """
    The getMissingSkills function is called from an 'Equipment' object and recieves an 'Employee' object as an argument. 
    Also, if we are going to make sure this works, we need to have a skill that the 'Equipment' requires ('skillRequirementsIDs')
    
    We'll create one 'Employee' with the skill and another 'Employee' without the skill to make sure both cases work
    """
    skill = Skill(name="test skill", skillId=0) # create a skill
    emp1 = Employee(name="Test Name", password_hash="123", emp_id="0", contactInfo="", skillIds=["0"]) # this employee has the skill
    emp2 = Employee(name="test Name 2", password_hash="123", emp_id="1", contactInfo="", skillIds=[]) # this employee doesn't have the skill
    equip = Equipment(equipId="0", name="Test Equipment", skillRequirementsIDs=["0"]) # this equipment requires the skill

    assert(equip.getMissingSkills(emp1) == [])  # emp1 isn't missing any skills so it should return an empty list; we assert that what that function returns is an empty list
    assert(equip.getMissingSkills(emp2) == ["0"])  # emp2 is missing the skill with id 0 so it should return a list with that id; we assert that what the function returns is that list
    print("- getMissingSkills() passed tests")  # if no error, it'll print that the test case passed and will return to 'do_tests()' and onto the next test


def persistent_data_test():
    # generate test data
    emp1 = Employee(name="Test Emp", password_hash="123", emp_id="emp0", contactInfo="")
    equip1 = Equipment(name="Test Equip", equipId="equip0")
    log1 = Log(date=datetime(year=2024, month=2, day=16, hour=1, minute=1, second=1), logCode=LOG_CODES.CHECKOUT, empId="emp0", equipId="equip0", notes=[])
    skill1 = Skill(name="Test Skill", skillId="skill1")

    
    def read_file(fn):
        with open(fn) as f:
            return f.read()
    
    test_fns = ["employees_test.csv", "equipment_test.csv", "logs_test.csv", "skills_test.csv"]
    test = [ # data to test
        {
            "func": lambda: write_employees_to_csv(employees=[emp1], filename=test_fns[0]),  # all write funcs should create file if not exists (w+)
            "get_func": lambda: read_file(test_fns[0]), 
            "expected": "Name,Password Hashed,Employee ID,Contact Info,Borrowed Equipment IDs,Skill IDs,Number of Lost Equipments,Is Admin\nTest Emp,123,emp0,,,,0,False\n"
        }, 
        {
            "func": lambda: write_equipment_to_csv(equipment=[equip1], filename=test_fns[1]),
            "get_func": lambda: read_file("equipment_test.csv"),
            "expected": "Equipment ID,Name,Borrower ID,Skill Requirements IDs,Queue\nequip0,Test Equip,,,\n"

        }, 
        {
            "func": lambda: write_logs_to_csv(logs=[log1], filename=test_fns[2]),
            "get_func": lambda: read_file(test_fns[2]),
            "expected": "Date,Emp ID,Equip ID,Logcode,Notes\n\"16/02/2024, 01:01:01\",emp0,equip0,1,\n"
        }, 
        {
            "func": lambda: write_skills_to_csv(skills=[skill1], filename=test_fns[3]),
            "get_func": lambda: read_file(test_fns[3]),
            "expected": "Name,Skill ID\nTest Skill,skill1\n"
        }
        ]
    
    for item in test: # do the actual checks
        item["func"]()
        assert(item['get_func']() == item['expected'])

    for fn in test_fns: # remove test files that were created
        remove(fn)
    print("- Data Saving is Persistent")



# create functions here to test different parts of the system...

def do_tests():
    print("Testing...")
    test_getMissingSkills()
    persistent_data_test()
    # call the functions here


if __name__=="__main__":
    do_tests()
