from source import dbconnect

class Event_Detail_Report():
    def __init__(self, empNum, startTime, endTime, reportType):
        self.empNum = empNum
        self.startTime = startTime
        self.endTime = endTime
        self.reportType = reportType
        self.csvRows = []
        self.headerRow = ['Event Type', 'Start Time', 'End Time']
        self.connection = dbconnect.dbconnect()
        self.compute_detail_report()

    def compute_detail_report(self):
        data = []
        if self.reportType == "Shifts":
            data = self.connection.get_shifts(str(self.empNum), self.startTime, self.endTime)
            self.headerRow = ['Shift Start', 'Shift End', 'Station', 'Role']
            if data != None:
                for event in data:
                    row = []
                    row.append(event[1])
                    row.append(event[2])
                    row.append(event[3])
                    row.append(event[4])
                    self.csvRows.append(row)
            return
        elif self.reportType == "Actual Calls":
            data = self.connection.get_actual_calls(str(self.empNum), self.startTime, self.endTime)
            self.headerRow = ['Call Time', 'Call Type', 'Duration (min)']
            if data != None:
                for event in data:
                    row = []
                    row.append(event[1])
                    row.append(event[2])
                    row.append(str(event[3].seconds / 60))
                    self.csvRows.append(row)
            return
        elif self.reportType == "LOSAP":
            data = self.connection.get_status_changes_for_range(str(self.empNum), self.startTime, self.endTime)
            self.headerRow = ['New Status', 'Effective Date', 'Notes']
            if data != None:
                for event in data:
                    row = []
                    row.append(event[0])
                    row.append(event[1])
                    row.append(event[2])
                    self.csvRows.append(row)
            return
        elif self.reportType == "Training":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'training%')
        elif self.reportType == "Work Detail":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'Work Detail%')
        elif self.reportType == "Sundays & Weeklies":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'Work Detail - Daily')
            data2 = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'Work Detail - Weekly')
            data3 = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'Work Detail - Sunday')
            if data == None:
                data = []
            if data2 != None:
                for dat in data2:
                    data.append(dat)
            if data3 != None:
                for dat in data3:
                    data.append(dat)
        # fix when fundraisers and meetings are in the database
        elif self.reportType == "Fundraisers":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'work detail-fundraiser')
        elif self.reportType == "Business Meetings":
            data = self.connection.get_events(str(self.empNum), self.startTime, self.endTime, 'business-meeting')
        if data != None:
            for event in data:
                row = []
                row.append(event[2])
                row.append(event[0])
                row.append(event[1])
                self.csvRows.append(row)
        self.connection.close()
        
