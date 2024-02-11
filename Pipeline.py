from enum import Enum
from datetime import datetime, timedelta
from dataStructures import *
from collections.abc import Callable 

# TODO: move Testing done at bottom into tests.py

DEBUG = False

class Pipeline:
	_report_template = {"header": f"Report {datetime.strftime(datetime.now(), '%m/%d/%Y %I:%M%p')}", "data": {}}

	def __init__(self, report: dict = _report_template, filters: list[Callable] = [], data: list=None):
		self.filters: list[Callable] = filters
		self.report: dict = report # basic initialization of report
		if data is not None and isinstance(data, list) and len(data) == 4:
			self.addLogs(data[0])
			self.addNumEmployees(data[1])
			self.addNumEquipment(data[2])
			self.addNumSkills(data[3])
		
	# ----data inputs------                     
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
	def addFilter(self, filter: Callable|list[Callable]) -> None: # can pass in a function or a list of functions
		if isinstance(filter, list):
			self.filters.extend(filter) # if its a list, combine it with the other filters
			return
		self.filters.append(filter) # otherwise add the func to the list of filters

	def removeFilter(self, filter: Callable) -> None:
		self.filters.remove(filter)
 
	def executeFilters(self) -> dict|None:
		if not self.hasAllData():
			return {"Missing Data..."}
		for report_filter in self.filters: # Order of filters matter
			self.report = report_filter(self.report)
		return self.report
    
	def clear_filters(self) -> None:
		self.filters.clear()
	# --------------------
	
	# ----report stuff----
	def getReport(self) -> dict: 
		return self.report
	
	def setReport(self, report: dict) -> None:
		self.report = report

	def resetReport(self):
		self.report = self._report_template
	# --------------------
	
	# ------- Misc --------
	def hasAllData(self):
		if any([x not in self.report['data'] for x in ['logs', 'numEmployees', 'numSkills', 'numEquipment']]): # make sure we have the data before executing the filters...
			return False
		return True
	# --------------------


# MISC
def getLogCodeName(logCode: LOG_CODES) -> str:
	return {v:k for k,v in LOG_CODES.__dict__.items() if v in [LOG_CODES.LOST, LOG_CODES.CHECKIN, LOG_CODES.CHECKOUT]}[logCode]

# Filters
def update_header(report: dict, text: str=f"Report {datetime.strftime(datetime.now(), '%m/%d/%Y %I:%M%p')}") -> dict:
	report['header'] = text
	return report

def num_lost_equipment(report: dict) -> dict:
	count = [log.logCode for log in report["data"]["logs"]].count(LOG_CODES.LOST)
	report['data']['numLostEquipment'] = count
	return report

def calculate_percentage_lost(report: dict) -> dict:
	if 'numLostEquipment' not in report['data']:
		report = num_lost_equipment(report)
	numLost: int = report['data']['numLostEquipment']
	if report['data']['numEquipment'] != 0:
		report['data']['percentageLost'] = f"{round(numLost / report['data']['numEquipment'] * 100, 2) } %"
	else:
		report['data']['percentageLost'] = f"N/A"
	return report
   
def _calc_frequency_of(logCode: int, report: dict):
	logCodeName = getLogCodeName(logCode=logCode)
	if len(report['data']['logs']) == 0:
		report['data'][f'frequencyOf{logCodeName}'] = "NA"
	frequency = [log.logCode for log in report['data']['logs']].count(logCode)
	report['data'][f'frequencyOf{logCodeName}'] = frequency
	return report

def _calc_datetimes_of(logCode: int, report:dict, start_date: datetime, end_date: datetime=datetime.today()):
	logCodeName = getLogCodeName(logCode=logCode)
	if len(report['data']['logs']) == 0:
		report['data'][f'dateTimesOf{logCodeName}'] = "NA"
	datetimes = [log.date for log in report['data']['logs'] if log.logCode == logCode and (start_date <= log.date <= end_date)]
	report['data'][f'dateTimesOf{logCodeName}'] = datetimes
	return report


AllFilters = [
	{"name": "Update Header", "func": update_header},
	{"name": "Calculate Number of Lost Equipment", "func": num_lost_equipment},
	{"name": "Calculate Percentage Of Lost Equipment", "func": calculate_percentage_lost}] + [
	{"name": f"Calculate Frequency of Lost Equipment", "func":  lambda report: _calc_frequency_of(logCode=LOG_CODES.LOST, report=report)},
	{"name": "Calculate Frequency of Checked-In Equipment", "func": lambda report: _calc_frequency_of(logCode=LOG_CODES.CHECKIN, report=report)},
	{"name": "Calculate Frequency of Checked-Out Equipment", "func": lambda report: _calc_frequency_of(logCode=LOG_CODES.CHECKOUT, report=report)}
	] + [
	{
		"name": "Get Dates and times of Lost Equipment in last day", 
		"func": lambda report: _calc_datetimes_of(logCode=LOG_CODES.LOST, report=report, start_date=datetime.today()-timedelta(days=1))
	},
	{
		"name": "Get Dates and times of Lost Equipment in last day",
		"func": lambda report: _calc_datetimes_of(logCode=LOG_CODES.LOST, report=report, start_date=datetime.today()-timedelta(days=7))	
	},
	{
		"name": "Get Dates and times of Lost Equipment in last month",
		"func": lambda report: _calc_datetimes_of(logCode=LOG_CODES.LOST, report=report, start_date=datetime.today()-timedelta(days=30))
	}
	]


# --------------------------------------- everything after this point is temporary / for testing ---------------------------------------------------
def generate_random_stuff_and_add_to_pipeline(pipeline: Pipeline):
	# generate random logs
	logs = [Log(date=datetime.now(), logCode=LOG_CODES.LOST, empId=0, equipId=0, notes=[])] * 9
	logs += [Log(date=datetime.now(), logCode=LOG_CODES.CHECKIN, empId=0, equipId=1, notes=[])] * 10
	logs += [Log(date=datetime.now(), logCode=LOG_CODES.CHECKOUT, empId=1, equipId=0, notes=[])] * 11
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
	
	generate_random_stuff_and_add_to_pipeline(pipeline)

	# generate filtered report
	new_report = pipeline.executeFilters() # need to call this to have the filters work
	print_report(new_report)
      
	# the update_header() filter using the text variable
	func = lambda report: update_header(report, "MY NEW HEADER")
	print_report(report)

	pipeline.addFilter(func) 
	new_report = pipeline.executeFilters()
	print_report(new_report)
    
	pipeline.clear_filters()
	pipeline.resetReport()

	generate_random_stuff_and_add_to_pipeline(pipeline)

	print_report(pipeline.getReport())

	pipeline.addFilter([update_header, num_lost_equipment])
	new_report = pipeline.executeFilters()
	print_report(new_report)

	pipeline.clear_filters()
	pipeline.resetReport()

	datetime_func_lost = lambda report: _calc_datetimes_of(LOG_CODES.LOST, report, 
													   datetime(year=2024, month=2, day=9, hour=0, minute=0), 
													   datetime(year=2024, month=2, day=11, hour=23, minute=59))
	pipeline.addFilter(datetime_func_lost)
	new_report = pipeline.executeFilters()
	print_report(new_report)
	

	pipeline.clear_filters()
	funcs = [
		lambda report: _calc_frequency_of(LOG_CODES.CHECKIN, report), 
		lambda report: _calc_frequency_of(LOG_CODES.CHECKOUT, report), 
		lambda report: _calc_frequency_of(LOG_CODES.LOST, report),
		calculate_percentage_lost
		]
	print(funcs)
	pipeline.addFilter(funcs)
	new_report = pipeline.executeFilters()

	print_report(new_report)

    
if __name__=="__main__": # standard to show that this file is runnable but this is just temporary for testing
	do_test()
