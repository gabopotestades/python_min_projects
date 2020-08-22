import os
import time
import math
import datetime
import threading
import multiprocessing
from csv import reader

class caseThread(threading.Thread):
    def __init__(self, threadID, fileName):
        threading.Thread.__init__(self)
        self.id = threadID
        self.fileName = fileName
    def run(self):
        global case_data
        global total_cases
        global dictAge
        global dictSex
        global dictAdmitted
        global dictHealthStatus
        global dictMonthRecovered
        global dictMonthDied
        global dictCasesPerRegion

        for row in case_data:
            total_cases += 1
            dictAge[row[2]] += 1
            dictSex[row[3]] += 1
            dictAdmitted[row[10]] += 1
            dictHealthStatus[row[15]] += 1

            if row[7]: 
                dateDied = datetime.datetime.strptime(row[7], "%Y-%m-%d")
                dictMonthDied[dateDied.month] += 1
            if row[8]: 
                dateRecovered = datetime.datetime.strptime(row[8], "%Y-%m-%d")
                dictMonthRecovered[dateRecovered.month] += 1
            
            if row[11] not in dictCasesPerRegion.keys():
                dictCasesPerRegion[row[11]] = 1
            else:
                dictCasesPerRegion[row[11]] += 1
        
        printInformation(self.fileName, 'cases')

class printInformation():
    def __init__(self, fileName, fileType):
        self.fileName = fileName
        self.fileType = fileType

        if self.fileType == 'cases':
            self.printCases()

    def printCases(self):
        global case_data
        global total_cases
        global dictAge
        global dictSex
        global dictAdmitted
        global dictHealthStatus
        global dictMonthRecovered
        global dictMonthDied
        global dictCasesPerRegion

        f = open(self.fileName, "w+")

        f.write('Cases per Age:\n')
        for key, value in dictAge.items():
            item = ifBlank if key == '' else key
            f.write('{0} : {1}\n'.format(item, value))
        f.write('=================================================\n')

        f.write('Sex count: \n')
        for key, value in dictSex.items():
            item = ifBlank if key == '' else key
            f.write('{0} : {1}\n'.format(item, value))
        f.write('=================================================\n')
        
        f.write('Current health status for every case: \n')
        for key, value in dictHealthStatus.items():
            item = ifBlank if key == '' else key
            f.write('{0} : {1}\n'.format(item, value))
        f.write('=================================================\n')

        f.write('Admitted to hospital: \n')
        for key, value in dictAdmitted.items():
            item = ifBlank if key == '' else key
            f.write('{0} : {1}\n'.format(item, value))
        f.write('=================================================\n')

        f.write('Cases per region: \n')
        for key in sorted(dictCasesPerRegion.keys()):
            item = ifBlank if key == '' else key
            value = dictCasesPerRegion[key]
            f.write('{0} : {1}\n'.format(item, value))
        f.write('=================================================\n')

        recovered = 0
        f.write('Recoveries per month: \n')
        for key, value in dictMonthRecovered.items():
            if value > 0:
                f.write('{0} : {1}\n'.format(dictMonthName[key], value))
                recovered += value
        f.write('=================================================\n')
    
        f.write('Deaths per month: \n')
        deaths = 0
        for key, value in dictMonthDied.items():
            if value > 0:
                f.write('{0} : {1}\n'.format(dictMonthName[key], value))
                deaths += value
        f.write('=================================================\n')

        f.write('Total cases: {0}\n'.format(total_cases))
        active_cases = total_cases - (deaths + recovered)
        f.write('Total deaths: {0}\n'.format(deaths))
        f.write('Total recoveries: {0}\n'.format(recovered))
        f.write('Total active cases: {0}\n'.format(active_cases))

        f.close()

if __name__ == '__main__':
    
    #Set initial values
    mode = ''
    command = 'cls' if os.name == 'nt' else 'clear'
    dictMonthName = {
        1: 'JANUARY',
        2: 'FEBRUARY',
        3: 'MARCH',
        4: 'APRIL',
        5: 'MAY',
        6: 'JUNE',
        7: 'JULY',
        8: 'AUGUST',
        9: 'SEPTEMBER',
        10: 'OCTOBER',
        11: 'NOVEMBER',
        12: 'DECEMBER'
    }
    cases_fname = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200811 - 04 Case Information.csv'
    file_name2 = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200810 - 04 Case Information.csv'
    hospital_status_fname = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200811 - 05 DOH Data Collect - Daily Report.csv'
    inventory_status_fname = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200811 - 06 DOH Data Collect - Weekly Report.csv'

    #Choose S for serial and P for parallel
    while mode not in ['S', 'P']:
        os.system(command)
        mode = input('Select mode (S/P): ').upper()

    #Set counters for Cases
    case_data = []
    total_cases = 0
    dictAge = {
        '0 to 4': 0,
        '5 to 9' : 0,
        '10 to 14': 0,
        '15 to 19': 0,
        '20 to 24': 0,
        '25 to 29': 0,
        '30 to 34': 0,
        '35 to 39': 0,
        '40 to 44': 0,
        '45 to 49': 0,
        '50 to 54': 0,
        '55 to 59': 0,
        '60 to 64': 0,
        '65 to 69': 0,
        '70 to 74': 0,
        '75 to 79': 0,
        '80+': 0,
        '': 0
    }
    dictSex = { 'FEMALE' : 0, 'MALE': 0, '': 0 }
    dictAdmitted = { 'NO': 0, 'YES': 0, '': 0}
    dictHealthStatus = {
        'RECOVERED': 0, 
        'ASYMPTOMATIC' : 0, 
        'MILD': 0, 
        'SEVERE': 0,
        'CRITICAL': 0,
        'DIED': 0,
        '': 0
    }
    dictMonthRecovered = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }
    dictMonthDied = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }
    dictCasesPerRegion = {}

    #Set counters for Hospital status
    hospitals_data = []
    total_Hospitals = 0
    icu_Occupied = 0
    icu_Vacant = 0
    bed_Occupied = 0
    bed_Vacant = 0
    isoBeds_Occupied = 0
    isoBeds_Vacant = 0
    mechVent_Occupied = 0
    mechVent_Vacant = 0
    icuNonCovid_Occupied = 0
    icuNonCovid_Vacant = 0
    nonICU_NonCovid_Occupied = 0
    nonICU_NonCovid_Vacant = 0
    mechVent_NonCovid_Occupied = 0
    mechVent_NonCovid_Vacant = 0
    doctorsQuarantined = 0
    nursesQuarantined = 0
    

    #Read files

    #Cases
    with open(cases_fname, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        case_data = list(csv_reader)
        # for item in csv_reader:
        #     case_data.append(item)

    #Hospitals
    with open(hospital_status_fname, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        hospitals_data = list(csv_reader)

    # with open(file_name2, 'r') as read_obj:
    #     csv_reader = reader(read_obj)
    #     header = next(csv_reader)
    #     case_data.extend(list(csv_reader))
    # for i in range(1):
    #     clone = case_data.copy()
    #     case_data.extend(clone)

    start_time = time.time()
    ifBlank = 'NOT STATED'
    casesFileName = 'Case_Summary.txt'

    if mode == 'S':
        
        for row in case_data:
            total_cases += 1
            dictAge[row[2]] += 1
            dictSex[row[3]] += 1
            dictAdmitted[row[10]] += 1
            dictHealthStatus[row[15]] += 1

            if row[7]: 
                dateDied = datetime.datetime.strptime(row[7], "%Y-%m-%d")
                dictMonthDied[dateDied.month] += 1
            if row[8]: 
                dateRecovered = datetime.datetime.strptime(row[8], "%Y-%m-%d")
                dictMonthRecovered[dateRecovered.month] += 1
            
            if row[11] not in dictCasesPerRegion.keys():
                dictCasesPerRegion[row[11]] = 1
            else:
                dictCasesPerRegion[row[11]] += 1

        printInformation(casesFileName, 'cases')

    else:
        
        casesInformationThread = caseThread(1, casesFileName)
        casesInformationThread.start()
        casesInformationThread.join()

    print('\n Time processed::')
    print("--- %s seconds ---" % (time.time() - start_time))


