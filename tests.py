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


# --------------------------------------- everything after this point is temporary / for testing ---------------------------------------------------
def generate_random_stuff_and_add_to_pipeline(pipeline: Pipeline):
    # generate 'random' logs (9 Lost Logs, 10 Checkin Logs, 11 Chekout Logs)
    logs = [Log(date=datetime.now(), logCode=LOG_CODES.LOST, empId=0, equipId=0, notes=[])] * 9
    logs += [Log(date=datetime.now(), logCode=LOG_CODES.CHECKIN, empId=0, equipId=1, notes=[])] * 10
    logs += [Log(date=datetime.now(), logCode=LOG_CODES.CHECKOUT, empId=1, equipId=0, notes=[])] * 11
    pipeline.addLogs(logs) # add them to the pipeline

    # could import randint from the random module to really make random number but meh...
    pipeline.addNumEmployees(5) # random number of employees
    pipeline.addNumEquipment(20) # random number of equipment
    pipeline.addNumSkills(7) # random number of skills

def get_output(report):
    text = f"Header: {report['header']}\n"
    text += "Data:\n"
    for key, value in report["data"].items():
        if key == "logs":
            value = "..." # don't wanna see all the Log objects in the terminal...
        text += " "*5 + f"{key} : {value}\n"
    text += "-"*30
    return text


def test_pipeline(): 
    report = {'header': 'this is the original report', 'data': {}}
    pipeline = Pipeline(report=report)

    # add filters
    pipeline.addFilter([update_header])

    generate_random_stuff_and_add_to_pipeline(pipeline)

    # generate filtered report
    new_report = pipeline.executeFilters() # need to call this to have the filters work
    expected = f"""Header: Report {datetime.strftime(datetime.now(), '%m/%d/%Y %I:%M%p')}
Data:
     logs : ...
     numEmployees : 5
     numEquipment : 20
     numSkills : 7
------------------------------"""
    assert(get_output(new_report) == expected)
        
    # the update_header() filter using the text variable
    func = lambda report: update_header(report, "MY NEW HEADER")
    expected = f"""Header: Report {datetime.strftime(datetime.now(), '%m/%d/%Y %I:%M%p')}
Data:
     logs : ...
     numEmployees : 5
     numEquipment : 20
     numSkills : 7
------------------------------"""
    assert(get_output(report) == expected)

    pipeline.addFilter(func) 
    new_report = pipeline.executeFilters()
    expected = f"""Header: MY NEW HEADER
Data:
     logs : ...
     numEmployees : 5
     numEquipment : 20
     numSkills : 7
------------------------------"""
    assert(get_output(report) == expected)
        
    pipeline.clear_filters()
    pipeline.resetReport()

    generate_random_stuff_and_add_to_pipeline(pipeline)
    expected = f"""Header: MY NEW HEADER
Data:
     logs : ...
     numEmployees : 5
     numEquipment : 20
     numSkills : 7
------------------------------"""
    assert(get_output(report) == expected)

    pipeline.addFilter([update_header, num_lost_equipment])
    new_report = pipeline.executeFilters()
    expected = f"""Header: MY NEW HEADER
Data:
     logs : ...
     numEmployees : 5
     numEquipment : 20
     numSkills : 7
------------------------------"""
    assert(get_output(report) == expected)

    pipeline.clear_filters()
    pipeline.resetReport()

    datetime_func_lost = lambda report: calc_datetimes_of(LOG_CODES.LOST, report, 
                                                        datetime(year=2024, month=2, day=9, hour=0, minute=0), 
                                                        datetime(year=2024, month=2, day=11, hour=23, minute=59))
    pipeline.addFilter(datetime_func_lost)
    new_report = pipeline.executeFilters()
    expected = """Header: MY NEW HEADER
Data:
     logs : ...
     numEmployees : 5
     numEquipment : 20
     numSkills : 7
------------------------------"""
    assert(get_output(report) == expected)


    pipeline.clear_filters()
    funcs = [
        lambda report: calc_frequency_of(LOG_CODES.CHECKIN, report), 
        lambda report: calc_frequency_of(LOG_CODES.CHECKOUT, report), 
        lambda report: calc_frequency_of(LOG_CODES.LOST, report),
        calculate_percentage_lost
        ]
    pipeline.addFilter(funcs)
    new_report = pipeline.executeFilters()

    assert(get_output(report) == expected)
    print("- Pipeline passed tests")


# create functions here to test different parts of the system..
def do_tests():
    print("Testing...")
    test_getMissingSkills()
    persistent_data_test()
    test_pipeline()
    # call the functions here


if __name__=="__main__":
    do_tests()
