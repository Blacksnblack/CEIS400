from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from dataStructures import Employee, Equipment, Skill, LOG_CODES, Log


class Pipeline:
    def __init__(self):
        self.filters = list()
 
    def add(self, filter):
        self.filters.extend(filter)
 
    def execute(self, report):
        print("Executing pipeline...")
        for report_filter in self.filters:
            report_filter(report)
 
def double_data(report):
    report['data'] = [x*2 for x in report['data']]
 
def update_header(report):
    report['header'] = 'this is the updated report'
 
pipeline = Pipeline()
 
pipeline.add([double_data, update_header])
 
report = {'header': 'this is the original report', 'data': [1,2,3]}
 
for key, value in report.items():
    print(key + ' : ' + str(value))
    


# Filtering Employees
    
quantities = [25, 49, 21, 17, 14, 28]
def checkQuantities(employees):
	if employees < 20:
		return True
	else:
		return False
filtered_employees = filter(checkQuantities, quantities)
print(list(filtered_employees)) 

   
             
# Filtering Equipment
    
quantities = [25, 49, 21, 17, 14, 28]
def checkQuantities(equipment):
 	if equipment < 20:
 		return True
 	else:
 		return False
filtered_equipment = filter(checkQuantities, quantities)
print(list(filtered_equipment))  

 
    
# Filtering Skills
    
quantities = [25, 49, 21, 17, 14, 28]
def checkQuantities(skills):
	if skills < 20:
		return True
	else:
		return False
filtered_skills = filter(checkQuantities, quantities)
print(list(filtered_skills))   


 
# Filtering LOG_CODES

quantities = [25, 49, 21, 17, 14, 28]
def checkQuantities(log_codes):
	if log_codes < 20:
		return True
	else:
		return False
filtered_log_codes = filter(checkQuantities, quantities)
print(list(filtered_log_codes))



# Filtering Log

quantities = [25, 49, 21, 17, 14, 28]
def checkQuantities(logs):
	if logs < 20:
		return True
	else:
		return False
filtered_logs = filter(checkQuantities, quantities)
print(list(filtered_logs))

