import os
import time
import linecache
from guppy import hpy

def display_top(snapshot, key_type='lineno', limit=5):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

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
        casesInformationProcess = ParallelProcessing.caseProcess(1, casesFileName)
        hospitalsInformationProcess = ParallelProcessing.hospitalsProcess(2, hospitalFileName)
        inventoryInformationProcess = ParallelProcessing.inventoryProcess(3, inventoryFileName)

        casesInformationProcess.start()
        hospitalsInformationProcess.start()
        inventoryInformationProcess.start()

        casesInformationProcess.join()
        hospitalsInformationProcess.join()
        inventoryInformationProcess.join()

    print('\n Time processed:')
    end_time = time.time() - start_time
    print("--- %s seconds ---" % end_time)

    print(h.heap())

    if mode == 'S':
        f = open('Serial_Testing.txt', 'a+')
        f.write(str(end_time)+'\n')
        f.close()
    elif mode == 'T':
        f = open('Threading_Testing.txt', 'a+')
        f.write(str(end_time)+'\n')
        f.close()
    else:
        f = open('Process_Testing.txt', 'a+')
        f.write(str(end_time)+'\n')
        f.close()