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
 
report = {'header': 'this is the original report',
           'data': [1,2,3]}
 
for key, value in report.items():
    print(key + ' : ' + str(value))

