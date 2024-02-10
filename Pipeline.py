from enum import Enum
from datetime import datetime
from dataStructures import *
from collections.abc import Callable # for having the types of functions which is called callable



class Pipeline:
	_report_template = {"header": "", "data": {}}

	def __init__(self, report: dict = _report_template, filters: list[Callable] = []):
		self.filters: list[Callable] = filters
		self.report: dict = report # basic initialization of report
		
	# ----data inputs------                     These will add to the report that the filters will alter or use to make new entries
	def addLogs(self, logs: list[Log]) -> None:
		self.report['data']['logs'] = logs

	def addNumEmployees(self, num: int) -> None:
		self.report['data']['numEmployees'] = num
	
	def addNumSkills(self, num: int) -> None:
		self.report['data']['numSkills'] = num

	def addNumEquipment(self, num: int) -> None:
		self.report['data']['numEquipment'] = num
	# --------------------
		
	# ---filter stuff-----
	def addFilter(self, filter: Callable|list[Callable]) -> None: #  Callable|list[Callable] means that you can either pass in a function or a list of functions
		if isinstance(filter, list):
			self.filters.extend(filter) # if its a list, combine it with the other filters
			return
		self.filters.append(filter) # otherwise add it the list of filters

	def removeFilter(self, filter: Callable) -> None:
		self.filters.remove(filter)
 
	def executeFilters(self) -> dict:
		for report_filter in self.filters: # the report will be ran through each filter so order of filters matter
			self.report = report_filter(self.report)
		return self.getReport()
    
	def clear_filters(self) -> None:
		self.filters.clear()
	# --------------------
	
	# ----report stuff----
	def getReport(self) -> dict: # for accessing report from pipeline in case you don't want to execute the filters again to get it...
		return self.report
	
	def setReport(self, report: dict) -> None:
		self.report = report

	def resetReport(self):
		self.report = self._report_template
	# --------------------


# Filters
def update_header(report: dict, text: str=f"Report {datetime.strftime(datetime.now(), '%m/%d/%Y %I:%M%p')}") -> None:
	report['header'] = text
	return report  # all filters need to return the report or else it won't work

def num_lost_equipment(report: dict):
	if "logs" not in report["data"]:
		return 
	count = [log.logCode for log in report["data"]["logs"]].count(LOG_CODES.LOST)
	report['data']['numLostEquipment'] = count
	return report

def calculate_percentage_lost(report: dict):
    return (report:dict) * 100
    return report
   
def calc_frequency_of(logCode: int, report: dict):
    frequency = [logCode.count for logCode in report]
    return dict(list(zip(logCode,frequency)))
    return report

def calc_datetimes_of(checkedin:int, checkedout:int, lost: int, report:dict)
    datetimes = [checkedin.times, checkedout.times, lost.times for checkedin, checkedout, lost in report]
    return dict(list(zip(checkedin, checkedout, lost, datetimes)))
    return report

class Filters(Enum): # easier to access all the filters ex: Filters.update_header (autocomplete will )
	update_header = update_header
	num_lost_equipment = num_lost_equipment
	calculate_percentage_lost = calculate_percentage_lost
	calc_frequency_of = calc_frequency_of
        calc_datetimes_of = calc_datetimes_of





# --------------------------------------- everything after this point is temporary / for testing ---------------------------------------------------

def generate_random_stuff_and_add_to_pipeline(pipeline: Pipeline):
	# generate random logs
	logs = [Log(date=datetime.now(), logCode=LOG_CODES.LOST, empId=0, equipId=0, notes=[])] * 10
	logs += [Log(date=datetime.now(), logCode=LOG_CODES.CHECKIN, empId=0, equipId=1, notes=[])] * 10
	pipeline.addLogs(logs) # add them to the pipeline

	# could import randint from the random module to really make random number but meh...
	pipeline.addNumEmployees(5) # random number of employees
	pipeline.addNumEquipment(20) # random number of equipment
	pipeline.addNumSkills(7) # random number of skills

def print_report(report):
		print(f"Header: {report['header']}")
		print("Data:")
		for key, value in report["data"].items():
			if key == "logs":
				value = "..." # don't wanna see all the Log objects in the terminal...
			print(" "*5 + f"{key} : {value}")
		print("-"*30)

def do_test(): 
	report = {'header': 'this is the original report', 'data': {}}
	pipeline = Pipeline(report=report)

	# add filters
	pipeline.addFilter([update_header])
	
	# generate filtered report
	new_report = pipeline.executeFilters() # need to call this to have the filters work
	print_report(new_report)
      
	# the update_header() filter using the text variable
def func(report):
	update_header(report, text="MY NEW HEADER")
    print report

	pipeline.addFilter(func) 
	new_report = pipeline.executeFilters()
	print_report(new_report)
    
	pipeline.clear_filters()
	pipeline.resetReport()

	generate_random_stuff_and_add_to_pipeline(pipeline)

	print_report(pipeline.getReport())

	pipeline.addFilter([Filters.update_header, Filters.num_lost_equipment])
	new_report = pipeline.executeFilters()
	print_report(new_report)

    
if __name__=="__main__": # standard to show that this file is runnable but this is just temporary for testing
	do_test()
	print_report(new_report)

    
if __name__=="__main__": # standard to show that this file is runnable but this is just temporary for testing
	do_test(
