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
    emp1 = Employee(name="Test Name", password_hash="123", emp_id="0", contactInfo="", skillIds=["0"]) # has the skill
    emp2 = Employee(name="test Name 2", password_hash="123", emp_id="1", contactInfo="", skillIds=[]) # doesn't have the skill
    equip = Equipment(equipId="0", name="Test Equipment", skillRequirementsIDs=["0"]) # requires the skill

    assert(equip.getMissingSkills(emp1) == [])  # emp1 ISN'T missing any skills so it should return an empty list; we assert that what that function returns is an empty list
    assert(equip.getMissingSkills(emp2) == ["0"])  # emp2 IS missing the skill with id 0 so it should return a list with that id; we assert that what the function returns is that list
    print("- getMissingSkills() passed tests")  # Success / No Assert Errors


def persistent_data_test():
    # generate test data
    emp1 = Employee(name="Test Emp", password_hash="123", emp_id="emp0", contactInfo="")
    equip1 = Equipment(name="Test Equip", equipId="equip0")
    log1 = Log(date=datetime(year=2024, month=2, day=16, hour=1, minute=1, second=1), logCode=LOG_CODES.CHECKOUT, empId="emp0", equipId="equip0", notes=[])
    skill1 = Skill(name="Test Skill", skillId="skill1")

    
    def read_file(fn):  # function to read file (used to check against expected value)
        with open(fn) as f:
            d = f.read()
        return d
    
    test_fns = ["employees_test.csv", "equipment_test.csv", "logs_test.csv", "skills_test.csv"] # files for testing (so default files aren't overriden or corrupted)
    test_dicts = [ # list of dicts that have the functions that test & get a return value and an item that's the expected outcome
        {   # * all write funcs should create file if not exists (w+) *
            "func": lambda: write_employees_to_csv(employees=[emp1], filename=test_fns[0]),  # Test writing employees to file
            "get_func": lambda: read_file(test_fns[0]), 
            "expected": "Name,Password Hashed,Employee ID,Contact Info,Borrowed Equipment IDs,Skill IDs,Number of Lost Equipments,Is Admin\nTest Emp,123,emp0,,,,0,False\n"
        }, 
        {
            "func": lambda: write_equipment_to_csv(equipment=[equip1], filename=test_fns[1]), # Test writing equipment to file
            "get_func": lambda: read_file("equipment_test.csv"),
            "expected": "Equipment ID,Name,Borrower ID,Skill Requirements IDs,Queue\nequip0,Test Equip,,,\n"

        }, 
        {
            "func": lambda: write_logs_to_csv(logs=[log1], filename=test_fns[2]),  # Test writing logs to file
            "get_func": lambda: read_file(test_fns[2]),
            "expected": "Date,Emp ID,Equip ID,Logcode,Notes\n\"16/02/2024, 01:01:01\",emp0,equip0,1,\n"
        }, 
        {
            "func": lambda: write_skills_to_csv(skills=[skill1], filename=test_fns[3]), # Test writing skills to file
            "get_func": lambda: read_file(test_fns[3]),
            "expected": "Name,Skill ID\nTest Skill,skill1\n"
        }
        ]
    
    for item in test_dicts: # do the actual checks
        item["func"]()  # call the function that will write the correct data
        assert(item['get_func']() == item['expected']) # check if it matches expected value

    for fn in test_fns: # remove test files that were created
        remove(fn)
    print("- Data Saving is Persistent") # if it get's this far, success! So print result!



# create functions here to test different parts of the system...

def do_tests():
    print("Testing...")
    test_getMissingSkills()
    persistent_data_test()
    # call the functions here


if __name__=="__main__":
    do_tests()
