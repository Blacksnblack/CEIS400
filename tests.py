from dataStructures import *
from GUI import *
from manager import *
from Pipeline import *


def test_getMissingSkills(): # Here's an example to test the "getMissingSkills" function in dataStructures.py in the Equipment class
    skill = Skill(name="test skill", skillId=0) # create a skill
    emp1 = Employee(name="Test Name", password_hash="123", emp_id="0", contactInfo="", skillIds=["0"]) # this employee has the skill
    emp2 = Employee(name="test Name 2", password_hash="123", emp_id="1", contactInfo="", skillIds=[]) # this employee doesn't have the skill
    equip = Equipment(equipId="0", name="Test Equipment", skillRequirementsIDs=["0"]) # this equipment requires the skill

    assert(equip.getMissingSkills(emp1) == [])  # emp1 isn't missing any skills so it should return an empty list
    assert(equip.getMissingSkills(emp2) == ["0"])  # emp2 is missing the skill with id 0 so it should return a list with that id
    print("getMissingSkills() passed tests")


# create functions here to test different parts of the system...


def do_tests():
    print("Testing...")
    test_getMissingSkills()
    # call the functions here


if __name__=="__main__":
    do_tests()
