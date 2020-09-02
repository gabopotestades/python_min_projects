import os
import time
import linecache
from guppy import hpy

#For testing purposes
if __name__ == '__main__':
    
    #Set initial values
    mode = ''
    command = 'cls' if os.name == 'nt' else 'clear'

    casesFileName = 'Case_Summary.txt'
    hospitalFileName = 'Hospital_Summary.txt'
    inventoryFileName = 'Inventory_Summary.txt'

    #Choose S for serial and P for parallel
    while mode not in ['S', 'P', 'T']:
        os.system(command)
        mode = input('Select mode (S/T/P): ').upper()

    start_time = time.time()
    #tracemalloc.start()
    h = hpy()

    if mode == 'S':
        import SerialProcessing
    elif mode == 'T':
        
        import ThreadProcessing
        casesInformationThread = ThreadProcessing.caseThread(1, casesFileName)
        hospitalsInformationThread = ThreadProcessing.hospitalsThread(2, hospitalFileName)
        inventoryInformationThread = ThreadProcessing.inventoryThread(3, inventoryFileName)

        casesInformationThread.start()
        hospitalsInformationThread.start()
        inventoryInformationThread.start()

        casesInformationThread.join()
        hospitalsInformationThread.join()
        inventoryInformationThread.join()

    elif mode == 'P':

        import ParallelProcessing
        casesInformationProcess = ParallelProcessing.caseProcess(1, casesFileName, True)
        hospitalsInformationProcess = ParallelProcessing.hospitalsProcess(2, hospitalFileName, True)
        inventoryInformationProcess = ParallelProcessing.inventoryProcess(3, inventoryFileName, True)

        casesInformationProcess.start()
        hospitalsInformationProcess.start()
        inventoryInformationProcess.start()

        casesInformationProcess.join()
        hospitalsInformationProcess.join()
        inventoryInformationProcess.join()

    end_time = time.time() - start_time
    print('\n Time processed:')
    print("--- %s seconds ---" % end_time)

    mem_usage = h.heap()
    
    txt_file = ''
    if mode == 'S': txt_file = 'Serial_Testing.txt'
    elif mode == 'T': txt_file = 'Thread_Testing.txt'
    else: txt_file = 'Process_Testing.txt'
    
    f = open(txt_file, 'a+')
    f.write(str(end_time)+'\t\t' + str(mem_usage.size) +' bytes\n')
    f.close()