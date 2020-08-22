import os
import time
import math
import pandas as pd
import operator
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
        global cases_fname
        global total_cases
        global dictAge
        global dictSex
        global dictAdmitted
        global dictHealthStatus
        global dictMonthRecovered
        global dictMonthDied
        global dictCasesPerRegion

        #Cases
        with open(cases_fname, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            case_data = list(csv_reader)

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

class hospitalsThread(threading.Thread):
    def __init__(self, threadID, fileName):
        threading.Thread.__init__(self)
        self.id = threadID
        self.fileName = fileName
    def run(self):
        global hospital_status_fname
        global hospitals_data
        global listHospitals
        global total_Hospitals
        global icu_Occupied
        global icu_Vacant
        global bed_Occupied
        global bed_Vacant
        global isoBeds_Occupied
        global isoBeds_Vacant
        global mechVent_Occupied
        global mechVent_Vacant
        global icuNonCovid_Occupied
        global icuNonCovid_Vacant
        global nonICU_NonCovid_Occupied
        global nonICU_NonCovid_Vacant
        global mechVent_NonCovid_Occupied
        global mechVent_NonCovid_Vacant
        global doctorsQuarantined
        global nursesQuarantined
        global othersQuarantined
        global doctorsAdmitted
        global nursesAdmitted
        global othersAdmitted
        global total_Patients
        global dict_Hospital_Per_Region

        #Hospitals
        with open(hospital_status_fname, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            hospitals_data = pd.DataFrame(list(csv_reader), columns = header)
            hospitals_data = hospitals_data.sort_values(['cfname','updateddate'], ascending = [True, False])
            hospitals_data = hospitals_data.values.tolist()

        for row in hospitals_data:
            
            if row[2] in listHospitals:
                continue
            
            total_Hospitals += 1
            listHospitals.append(row[2])
            icu_Vacant += int(row[6])
            icu_Occupied += int(row[7])
            isoBeds_Vacant += int(row[8])
            isoBeds_Occupied += int(row[9])
            bed_Vacant += int(row[10])
            bed_Occupied += int(row[11])
            mechVent_Vacant += int(row[12])
            mechVent_Occupied += int(row[13])

            if row[14] != '': icuNonCovid_Vacant += float(row[14])
            if row[15] != '': icuNonCovid_Occupied += float(row[15])
            if row[16] != '': nonICU_NonCovid_Vacant += float(row[16])
            if row[17] != '': nonICU_NonCovid_Occupied += float(row[17])
            if row[18] != '': mechVent_NonCovid_Vacant += float(row[18])
            if row[19] != '': mechVent_NonCovid_Occupied += float(row[19])

            nursesQuarantined += int(row[20])
            doctorsQuarantined += int(row[21])
            othersQuarantined += int(row[22])

            nursesAdmitted += int(row[23])
            doctorsAdmitted += int(row[24])
            othersAdmitted += int(row[25])

            if row[41] != '': total_Patients += float(row[41])
            
            if row[46] not in dict_Hospital_Per_Region.keys():
                dict_Hospital_Per_Region[row[46]] = 1
            else:
                dict_Hospital_Per_Region[row[46]] += 1

        printInformation(self.fileName, 'hospitals')

class inventoryThread(threading.Thread):
    def __init__(self, threadID, fileName):
        threading.Thread.__init__(self)
        self.id = threadID
        self.fileName = fileName
    def run(self):
        global inventory_data
        global inventory_status_fname
        global gown
        global goggles
        global gloves
        global shoe_Cover
        global head_Cover
        global face_Shield
        global surg_Mask
        global n95_Mask
        global coverAll

        #Inventory
        with open(inventory_status_fname, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            inventory_data = list(csv_reader)

        for row in inventory_data:

            gown += int(row[6])
            gloves += int(row[7])
            head_Cover += int(row[8])
            goggles += int(row[9])
            coverAll += int(row[10])
            shoe_Cover += int(row[11])
            face_Shield += int(row[12])
            surg_Mask += int(row[13])
            n95_Mask += int(row[14])
        
        printInformation(inventoryFileName, 'inventory')

class printInformation():
    def __init__(self, fileName, fileType):
        self.fileName = fileName
        self.fileType = fileType

        if self.fileType == 'cases':
            self.printCases()
        elif self.fileType == 'hospitals':
            self.printHospitals()
        elif self.fileType == 'inventory':
            self.printInventory()

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
        global ifBlank

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

    def printHospitals(self):
        global hospitals_data
        global total_Hospitals
        global icu_Occupied
        global icu_Vacant
        global bed_Occupied
        global bed_Vacant
        global isoBeds_Occupied
        global isoBeds_Vacant
        global mechVent_Occupied
        global mechVent_Vacant
        global icuNonCovid_Occupied
        global icuNonCovid_Vacant
        global nonICU_NonCovid_Occupied
        global nonICU_NonCovid_Vacant
        global mechVent_NonCovid_Occupied
        global mechVent_NonCovid_Vacant
        global doctorsQuarantined
        global nursesQuarantined
        global othersQuarantined
        global doctorsAdmitted
        global nursesAdmitted
        global othersAdmitted
        global total_Patients
        global dict_Hospital_Per_Region
        global ifBlank

        f = open(self.fileName, "w+")

        f.write('Total hospitals: {0}\n'.format(total_Hospitals))
        f.write('Total patients: {0}\n'.format(int(total_Patients)))
        f.write('=================================================\n')

        f.write('Beds: \n')
        f.write('Occupied: {0}\n'.format(bed_Occupied))
        f.write('Vacant: {0}\n'.format(bed_Vacant))
        f.write('=================================================\n')

        f.write('Isolation Beds: \n')
        f.write('Occupied: {0}\n'.format(isoBeds_Occupied))
        f.write('Vacant: {0}\n'.format(isoBeds_Vacant))
        f.write('=================================================\n')

        f.write('Mechanical Ventilators: \n')
        f.write('Occupied by COVID Patients: {0}\n'.format(mechVent_Occupied))
        f.write('Vacant for COVID Patients: {0}\n'.format(mechVent_Vacant))
        f.write('Occupied by non-COVID Patients: {0}\n'.format(int(mechVent_NonCovid_Occupied)))
        f.write('Vacant for non-COVID Patients: {0}\n'.format(int(mechVent_NonCovid_Vacant)))
        f.write('=================================================\n')

        f.write('ICU Beds: \n')
        f.write('Occupied by COVID Patients: {0}\n'.format(icu_Occupied))
        f.write('Vacant for COVID Patients: {0}\n'.format(icu_Vacant))
        f.write('Occupied by non-COVID Patients: {0}\n'.format(int(icuNonCovid_Occupied)))
        f.write('Vacant for non-COVID Patients: {0}\n'.format(int(icuNonCovid_Vacant)))
        f.write('=================================================\n')

        f.write('Health Workers Quarantined: \n')
        f.write('Doctors: {0}\n'.format(doctorsQuarantined))
        f.write('Nurses: {0}\n'.format(nursesQuarantined))
        f.write('Other Staff: {0}\n'.format(othersQuarantined))
        f.write('=================================================\n')

        f.write('Health Workers Admitted: \n')
        f.write('Doctors: {0}\n'.format(doctorsAdmitted))
        f.write('Nurses: {0}\n'.format(nursesAdmitted))
        f.write('Other Staff: {0}\n'.format(othersAdmitted))
        f.write('=================================================\n')

        f.write('Hospitals per region: \n')
        for key in sorted(dict_Hospital_Per_Region.keys()):
            item = ifBlank if key == '' else key
            value = dict_Hospital_Per_Region[key]
            f.write('{0} : {1}\n'.format(item, value))
        f.write('=================================================\n')

        f.close()

    def printInventory(self):
        global gown
        global goggles
        global gloves
        global shoe_Cover
        global head_Cover
        global face_Shield
        global surg_Mask
        global n95_Mask
        global coverAll

        f = open(self.fileName, "w+")

        f.write('Current Inventory: \n')
        f.write('Gloves -  {0}\n'.format(gloves))
        f.write('Goggles -  {0}\n'.format(goggles))
        f.write('Gloves -  {0}\n'.format(gloves))
        f.write('Shoe Cover -  {0}\n'.format(shoe_Cover))
        f.write('Head Cover -  {0}\n'.format(head_Cover))
        f.write('Face Shield -  {0}\n'.format(face_Shield))
        f.write('Surgical Mask -  {0}\n'.format(surg_Mask))
        f.write('N95 Mask -  {0}\n'.format(n95_Mask))
        f.write('Cover All -  {0}\n'.format(coverAll))
        f.write('=================================================\n')

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
    listHospitals = []
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
    othersQuarantined = 0
    doctorsAdmitted = 0
    nursesAdmitted = 0
    othersAdmitted = 0
    total_Patients = 0
    dict_Hospital_Per_Region = {}

    #Set counters for inventory
    inventory_data = []
    gown = 0
    goggles = 0
    gloves = 0
    shoe_Cover = 0
    head_Cover = 0
    face_Shield = 0
    surg_Mask = 0
    n95_Mask = 0
    coverAll = 0

    start_time = time.time()
    ifBlank = 'NOT STATED'
    casesFileName = 'Case_Summary.txt'
    hospitalFileName = 'Hospital_Summary.txt'
    inventoryFileName = 'Inventory_Summary.txt'

    if mode == 'S':
        
        #Read files

        #Cases
        with open(cases_fname, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            case_data = list(csv_reader)

        #Hospitals
        with open(hospital_status_fname, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            hospitals_data = pd.DataFrame(list(csv_reader), columns = header)
            hospitals_data = hospitals_data.sort_values(['cfname','updateddate'], ascending = [True, False])
            hospitals_data = hospitals_data.values.tolist()

        #Inventory
        with open(inventory_status_fname, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            inventory_data = list(csv_reader)

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

        for row in hospitals_data:
            
            if row[2] in listHospitals:
                continue

            total_Hospitals += 1
            listHospitals.append(row[2])
            icu_Vacant += int(row[6])
            icu_Occupied += int(row[7])
            isoBeds_Vacant += int(row[8])
            isoBeds_Occupied += int(row[9])
            bed_Vacant += int(row[10])
            bed_Occupied += int(row[11])
            mechVent_Vacant += int(row[12])
            mechVent_Occupied += int(row[13])

            if row[14] != '': icuNonCovid_Vacant += float(row[14])
            if row[15] != '': icuNonCovid_Occupied += float(row[15])
            if row[16] != '': nonICU_NonCovid_Vacant += float(row[16])
            if row[17] != '': nonICU_NonCovid_Occupied += float(row[17])
            if row[18] != '': mechVent_NonCovid_Vacant += float(row[18])
            if row[19] != '': mechVent_NonCovid_Occupied += float(row[19])

            nursesQuarantined += int(row[20])
            doctorsQuarantined += int(row[21])
            othersQuarantined += int(row[22])

            nursesAdmitted += int(row[23])
            doctorsAdmitted += int(row[24])
            othersAdmitted += int(row[25])

            if row[41] != '': total_Patients += float(row[41])
            
            if row[46] not in dict_Hospital_Per_Region.keys():
                dict_Hospital_Per_Region[row[46]] = 1
            else:
                dict_Hospital_Per_Region[row[46]] += 1

        printInformation(hospitalFileName, 'hospitals')

        for row in inventory_data:
            
            gown += int(row[6])
            gloves += int(row[7])
            head_Cover += int(row[8])
            goggles += int(row[9])
            coverAll += int(row[10])
            shoe_Cover += int(row[11])
            face_Shield += int(row[12])
            surg_Mask += int(row[13])
            n95_Mask += int(row[14])
        
        printInformation(inventoryFileName, 'inventory')

    else:
        
        casesInformationThread = caseThread(1, casesFileName)
        hospitalsInformationThread = hospitalsThread(2, hospitalFileName)
        inventoryInformationThread = inventoryThread(3, inventoryFileName)

        hospitalsInformationThread.start()
        casesInformationThread.start()
        inventoryInformationThread.start()

        inventoryInformationThread.join()
        casesInformationThread.join()
        hospitalsInformationThread.join()

    print('\n Time processed::')
    print("--- %s seconds ---" % (time.time() - start_time))