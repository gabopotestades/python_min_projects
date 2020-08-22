import os
import time
import math
import datetime
import threading
import multiprocessing
from csv import reader

class sProcess(multiprocessing.Process):
    def __init__(self, processID):
        multiprocessing.Process.__init__(self)
        self.processID = processID
    
    def run(self):
        global data
        #global lock
        for item in data:
            print(item)
            break

        #read data here

class sThread(threading.Thread):
    def __init__(self, threadID, startPoint, midPoint):
        threading.Thread.__init__(self)
        self.id = threadID
        self.startPoint = startPoint
        self.endPoint = midPoint
    def run(self):
        #print('Thread', self.id, ' has started')
        global data
        global total_cases
        global dictAge
        global dictSex
        global dictAdmitted
        global dictHealthStatus
        global dictMonthRecovered
        global dictMonthDied
        global dictCasesPerRegion
        global shared_resource_lock

        # total_casesThread = 0
        # dictAgeThread = {
        # '0 to 4': 0,
        # '5 to 9' : 0,
        # '10 to 14': 0,
        # '15 to 19': 0,
        # '20 to 24': 0,
        # '25 to 29': 0,
        # '30 to 34': 0,
        # '35 to 39': 0,
        # '40 to 44': 0,
        # '45 to 49': 0,
        # '50 to 54': 0,
        # '55 to 59': 0,
        # '60 to 64': 0,
        # '65 to 69': 0,
        # '70 to 74': 0,
        # '75 to 79': 0,
        # '80+': 0,
        # '': 0
        # }
        # dictSexThread = { 'FEMALE' : 0, 'MALE': 0, '': 0 }
        # dictAdmittedThread = { 'NO': 0, 'YES': 0, '': 0}
        # dictHealthStatusThread = {
        #     'RECOVERED': 0, 
        #     'ASYMPTOMATIC' : 0, 
        #     'MILD': 0, 
        #     'SEVERE': 0,
        #     'CRITICAL': 0,
        #     'DIED': 0,
        #     '': 0
        # }
        # dictMonthRecoveredThread = {
        #     1: 0,
        #     2: 0,
        #     3: 0,
        #     4: 0,
        #     5: 0,
        #     6: 0,
        #     7: 0,
        #     8: 0,
        #     9: 0,
        #     10: 0,
        #     11: 0,
        #     12: 0
        # }
        # dictMonthDiedThread = {
        #     1: 0,
        #     2: 0,
        #     3: 0,
        #     4: 0,
        #     5: 0,
        #     6: 0,
        #     7: 0,
        #     8: 0,
        #     9: 0,
        #     10: 0,
        #     11: 0,
        #     12: 0
        # }
        # dictCasesPerRegionThread = {}

        for row in data[self.startPoint:self.endPoint]:
            shared_resource_lock.acquire()
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
            
            shared_resource_lock.release()

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
    file_name = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200811 - 04 Case Information.csv'
    file_name2 = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200810 - 04 Case Information.csv'

    #Choose S for serial and P for parallel
    while mode not in ['S', 'P']:
        os.system(command)
        mode = input('Select mode (S/P): ').upper()

    #Set counters
    data = []
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

    with open(file_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        for item in csv_reader:
            data.append(item)

    with open(file_name2, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        data.extend(list(csv_reader))
    for i in range(1):
        clone = data.copy()
        data.extend(clone)

    start_time = time.time()

    if mode == 'S':
        
        for row in data:
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

    else:
        shared_resource_lock = threading.Lock()
        divideBy = 2
        perDivision = math.ceil(len(data)/divideBy)
        sections = []
        section = 0
        for n in range(divideBy):
            section += perDivision
            sections.append(section)

        #lock = multiprocessing.Lock()
        #pointer = multiprocessing.Value('i', 0)
        
        firstBatch = sThread(1, 0, sections[0])
        secondBatch = sThread(2, sections[0], sections[1])
        #thirdBatch = sThread(3, sections[1], sections[2])
        firstBatch.start()
        secondBatch.start()
        #thirdBatch.start()
        firstBatch.join()
        secondBatch.join()
        #thirdBatch.join()

    ifBlank = 'NOT STATED'

    print('\nCases per Age:')
    for key, value in dictAge.items():
        item = ifBlank if key == '' else key
        print(item, ':', value)

    print('\nSex count:')
    for key, value in dictSex.items():
        item = ifBlank if key == '' else key
        print(item, ':', value)
    
    print('\nCurrent health status for every case:')
    for key, value in dictHealthStatus.items():
        item = ifBlank if key == '' else key
        print(item, ':', value)

    print('\nAdmitted to hospital:')
    for key, value in dictAdmitted.items():
        item = ifBlank if key == '' else key
        print(item, ':', value)

    print('\nCases per region:')
    for key in sorted(dictCasesPerRegion.keys()):
        item = ifBlank if key == '' else key
        value = dictCasesPerRegion[key]
        print(item, '-', value)

    recovered = 0
    print('\nRecoveries per month:')
    for key, value in dictMonthRecovered.items():
        if value > 0:
            #item = ifBlank if key == '' else key
            print(dictMonthName[key], ': ', value)
            recovered += value
 
    print('\nDeaths per month:')
    deaths = 0
    for key, value in dictMonthDied.items():
        if value > 0:
            #item = ifBlank if key == '' else key
            print(dictMonthName[key], ': ', value)
            deaths += value

    print('\nTotal cases:', total_cases)
    active_cases = total_cases - (deaths + recovered)
    print('Total deaths:', deaths)
    print('Total recoveries:', recovered)
    print('Total active cases:', active_cases)


    print('\n Time processed::')
    print("--- %s seconds ---" % (time.time() - start_time))


