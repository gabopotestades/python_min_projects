import os
import time
import datetime
import multiprocessing
from csv import reader

class fibThread(multiprocessing.Process):
    def __init__(self, processID):
        multiprocessing.Process.__init__(self)
        self.processID = processID
        self.p = 0
    
    def run(self):
        global lock

        #read data here

if __name__ == '__main__':

    #Set initial values
    mode = ''
    command = 'cls' if os.name == 'nt' else 'clear'
    file_name = 'Threading for DOH COVID Data\DOH COVID Data Drop_ 20200811 - 04 Case Information.csv'

    #Choose S for serial and P for parallel
    while mode not in ['S', 'P']:
        os.system(command)
        mode = input('Select mode (S/P): ').upper()

    num = 0
    start_time = time.time()

    #Set counters
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
            data = list(csv_reader)
            data.extend(list(csv_reader))

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
        
        print(dictCasesPerRegion)

    else:
        pass
        lock = multiprocessing.Lock()
        pointer = multiprocessing.Value('i', 0)
        #fib1 = fibThread(1)
        #fib1.start()
        #fib1.join()

    end_time = time.time()

    print("--- %s seconds ---" % (time.time() - start_time))


