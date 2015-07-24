'''
This code is copyrighted to Dina Bayomie and Iman Helal @2015 Research work
Information System Department, Faculty of computers and Information System
Cairo University, Egypt
'''

import sys
import math
#from tree import Tree
#from branch import Branch
#from traceLog import TraceLog

from algorithm import Algorithm
import os
import shutil
import csv 
import time # to calculate the processing time of the algorithm & used in watchdog 

# required imports for watchdog
import logging
from collections import deque
from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    
    counter = 0
    fileSize = 0
    prevFileSize = 0
    
    def on_modified(self, event):
        #print "count ",self.counter
        fileName = "C:/Iman/My Docs/VS2013-Projects/SimulatingEvents/SimulatingEvents/bin/Debug/S.csv"
        self.fileSize = self.file_len(fileName)
        #print "fileSize on change ",self.fileSize
        #print ', '.join(self.get_last_row(fileName))
        self.get_last_row(fileName)
        self.counter=self.counter+1


    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def get_last_row(self,csv_filename):
        with open(csv_filename, 'rb') as f:
            self.fileSize = self.file_len(csv_filename)
            readLines = self.fileSize - self.prevFileSize
            #print "prevFileSize on get last row ",self.fileSize, " read last lines = ",readLines
            self.prevFileSize = self.fileSize
            if (readLines == 0):
                readLines = 1
            
            multipleLines =  deque(csv.reader(f), readLines)
            for l in multipleLines:
                #print ', '.join(l)
                if(l[0].lower()!="timestamp"):
                    alg.apply_algorithm(l,dashboard_filename) # l = symbol
                    '''
                    # to continue building trace logs with each symbol (has problem in calculating confidence)
                    end_time_build_tree = time.clock()
                    print"Algorithm execution time time_build_tree :  %s seconds " % (end_time_build_tree - start_time_build_tree)
                    
                    alg.finish_algorithm(start_time_build_tree)
                    end_time_algorithm=time.clock()
                    
                    print "event logs"
                    i =1
                    for eLog in alg.constructedTraces:
                        if(i==1):
                            #eLog.write_traceLog_into_file_csv(i)
                            #eLog.write_traceLog_into_file_txt(i)
                            eLog.write_traceLog_into_XML(i)
                        eLog.prepare_traceLog(i)
                        i+=1
                    #print other traces that have produces but not completely fit
                    if (len(alg.otherConstructedTraces)>0):
                        print "other event logs "
                        for oeLog in alg.otherConstructedTraces:
                            #oeLog.write_traceLog_into_file_csv(i,otherDirectory)
                            #oeLog.write_traceLog_into_file_txt(i,otherDirectory)
                            oeLog.write_traceLog_into_XML(i,otherDirectory)
                            oeLog.prepare_traceLog(i)
                            i+=1
                    
                    print"program execution time : %s seconds " % (time.time() - start_time_program)
                    print"Algorithm execution time :  %s seconds " % (end_time_algorithm - start_time_algorithm)
                    '''
            
            #return deque(csv.reader(f), readLines)[0]



if __name__ == "__main__":
    #start run time of program
    start_time_program = time.time()
    
    from py4j.java_gateway import JavaGateway 
    
    print 'Python started'
    
    gateway = JavaGateway()
    startActivity= gateway.entry_point.getStartActivityName()
    print 'startActivity', startActivity
    
    dic=gateway.entry_point.getMatrixRelations()
    M=dict()
    for k in dic :
        M[k]=dict()
        for n in dic[k]:
            M[k][n]=dic[k][n]
    
    dicArr=gateway.entry_point.getAllParents()
    Parents=dict()
    for k in dicArr :
        Parents[k]=[]
        for n in dicArr[k]:
            Parents[k].append(n)
          
    print M
    gateway.shutdown()
    
    S = [] # Extracted unlabeled Sequence from File d directly
    '''
    #T = {'A':[2,5,10],'B':[3,5,10],'C':[4,7,9],'D':[5,7,12]}
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'none'},'B':{'A':'none','B':'xor','C':'xor','D':'seq'},'C':{'A':'none','B':'xor','C':'xor','D':'seq'},'D':{'A':'none','B':'none','C':'none','D':'xor'}}
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'none'},'B':{'A':'none','B':'xor','C':'and','D':'seq'},'C':{'A':'none','B':'and','C':'xor','D':'seq'},'D':{'A':'none','B':'none','C':'none','D':'xor'}}
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'seq','E':'none'},'B':{'A':'none','B':'xor','C':'and','D':'and','E':'seq'},'C':{'A':'none','B':'and','C':'xor','D':'and','E':'seq'},'D':{'A':'none','B':'and','C':'and','D':'xor','E':'seq'},'E':{'A':'none','B':'none','C':'none','D':'none','E':'xor'}}
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'none','E':'none'},'B':{'A':'none','B':'xor','C':'and','D':'and','E':'seq'},'C':{'A':'none','B':'and','C':'xor','D':'seq','E':'none'},'D':{'A':'none','B':'and','C':'none','D':'xor','E':'seq'},'E':{'A':'none','B':'none','C':'none','D':'none','E':'xor'}}
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'none','E':'none'},'B':{'A':'none','B':'xor','C':'xor','D':'xor','E':'seq'},'C':{'A':'none','B':'xor','C':'xor','D':'seq','E':'none'},'D':{'A':'none','B':'xor','C':'none','D':'xor','E':'seq'},'E':{'A':'none','B':'none','C':'none','D':'none','E':'xor'}}
    
    #XOR complex 
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'none','E':'none'},'B':{'A':'none','B':'xor','C':'xor','D':'xor','E':'seq'},'C':{'A':'none','B':'xor','C':'xor','D':'seq','E':'none'},'D':{'A':'none','B':'xor','C':'none','D':'xor','E':'seq'},'E':{'A':'none','B':'none','C':'none','D':'none','E':'xor'}}
    #And complex
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'seq','E':'none','F':'none'},
    #   'B':{'A':'none','B':'xor','C':'and','D':'and','E':'seq','F':'none'},
    #   'C':{'A':'none','B':'and','C':'xor','D':'and','E':'and','F':'seq'},
    #   'D':{'A':'none','B':'and','C':'and','D':'xor','E':'and','F':'seq'},
    #   'E':{'A':'none','B':'none','C':'and','D':'and','E':'xor','F':'seq'},
    #   'F':{'A':'none','B':'none','C':'none','D':'none','E':'none','F':'xor'}}
    M={'A':{'A':'xor','B':'seq','C':'seq','D':'none','E':'none'},
       'B':{'A':'none','B':'xor','C':'and','D':'seq','E':'none'},
       'C':{'A':'none','B':'and','C':'xor','D':'and','E':'seq'},
       'D':{'A':'none','B':'none','C':'and','D':'xor','E':'seq'},
       'E':{'A':'none','B':'none','C':'none','D':'none','E':'xor'}}
    
    
    # to be addded in bp code as petri net modell
    ##combine
    #M={'A':{'A':'xor','B':'seq','C':'none','D':'seq','E':'none','F':'none','G':'none','H':'none'},
    #   'B':{'A':'none','B':'xor','C':'seq','D':'xor','E':'none','F':'none','G':'none','H':'none'},
    #   'C':{'A':'none','B':'none','C':'xor','D':'xor','E':'seq','F':'none','G':'none','H':'none'},
    #   'D':{'A':'none','B':'xor','C':'xor','D':'xor','E':'seq','F':'none','G':'none','H':'none'},
    #   'E':{'A':'none','B':'none','C':'none','D':'none','E':'xor','F':'seq','G':'seq','H':'none'},
    #   'F':{'A':'none','B':'none','C':'none','D':'none','E':'none','F':'xor','G':'and','H':'seq'},
    #   'G':{'A':'none','B':'none','C':'none','D':'none','E':'none','F':'and','G':'xor','H':'seq'},
    #   'H':{'A':'none','B':'none','C':'none','D':'none','E':'none','F':'none','G':'none','H':'none'}}
    #nested
    #M={'A':{'A':'xor','B':'seq','C':'seq','D':'none','E':'none','F':'none','G':'none','H':'none'},
    #   'B':{'A':'none','B':'xor','C':'xor','D':'seq','E':'seq','F':'none','G':'xor','H':'none'},
    #   'C':{'A':'none','B':'xor','C':'xor','D':'xor','E':'xor','F':'none','G':'seq','H':'none'},
    #   'D':{'A':'none','B':'none','C':'xor','D':'xor','E':'and','F':'seq','G':'xor','H':'none'},
    #   'E':{'A':'none','B':'none','C':'xor','D':'and','E':'xor','F':'seq','G':'xor','H':'none'},
    #   'F':{'A':'none','B':'none','C':'xor','D':'none','E':'none','F':'xor','G':'xor','H':'seq'},
    #   'G':{'A':'none','B':'xor','C':'none','D':'xor','E':'xor','F':'xor','G':'xor','H':'seq'},
    #   'H':{'A':'none','B':'none','C':'none','D':'none','E':'none','F':'none','G':'none','H':'none'}}
    
    #Parents={'A': [], 'C': ['A'], 'B': ['A'], 'D': ['B','C']}
    #nested
    #Parents={'A': [], 'B': ['A'], 'C': ['A'], 'D': ['B'], 'E': ['B'], 'F': ['D','E'], 'G': ['C'], 'H': ['G','F']}
    #combine
    #Parents={'A': [], 'B': ['A'], 'C': ['B'], 'D': ['A'], 'E': ['C','D'], 'F': ['E'], 'G': ['E'], 'H': ['G','F']}
    #XOR complex
    #Parents={'A': [], 'C': ['A'], 'B': ['A'], 'D': ['C'],'E':['B','D']}
    #Parents={'A': [], 'C': ['A'], 'B': ['A'], 'D': ['A'],'E':['B','D','C']}
    #and complex
    Parents={'A': [], 'C': ['A'], 'B': ['A'], 'D': ['A'],'E':['B'],'F':['E','D','C']}
    startActivity="A"
    #M={'start':{'start':0,'A':1,'B':0,'C':0,'D':0,'End':0},'A':{'start':0,'A':0,'B':0.5,'C':0.5,'D':0,'End':0},'B':{'start':0,'A':0,'B':0,'C':0,'D':1,'End':0},'C':{'start':0,'A':0,'B':0,'C':0,'D':1,'End':0},'D':{'start':0,'A':0,'B':0,'C':0,'D':0,'End':0},'End':{'start':0,'A':0,'B':0,'C':0,'D':0,'End':0}}
    #M={'start':{'start':0,'A':1,'B':0,'C':0,'D':0,'E':0,'End':0},'A':{'start':0,'A':0,'B':0.3,'C':0.3,'D':0.3,'E':0,'End':0},'B':{'start':0,'A':0,'B':0,'C':0.3,'D':0.3,'E':0.3,'End':0},'C':{'start':0,'A':0,'B':0.3,'C':0,'D':0.3,'E':0.3,'End':0},'D':{'start':0,'A':0,'B':0.3,'C':0.3,'D':0,'E':0.3,'End':0},'E':{'start':0,'A':0,'B':0,'C':0,'D':0,'E':0,'End':1},'End':{'start':0,'A':0,'B':0,'C':0,'D':0,'E':0,'End':0}}
    '''
    GivenConfidenceLevel=0#.3
    
    ''' removing folders '''
    txtDirectory="labeledEventLog_txt/"
    csvDirectory="labeledEventLog_csv/"
    xesDirectory="labeledEventLog_xes/"
    otherDirectory="otherEventLog_all/"
    if os.path.exists(txtDirectory):
        shutil.rmtree(txtDirectory)
    if os.path.exists(csvDirectory):
        shutil.rmtree(csvDirectory)
    if os.path.exists(xesDirectory):
        shutil.rmtree(xesDirectory)
    if os.path.exists(otherDirectory):
        shutil.rmtree(otherDirectory)
    
    print "processing input ....."
    print "reading unlabeled event log"
    print "model ",M
    print "start Activity : ",startActivity
    '''reading and preparing event log input 1'''
    filename=sys.argv[1]
    splitarr=filename.split('.')
    extension=splitarr[len(splitarr)-1]
    print extension
    print filename
    timestamps=[]
    if (extension =='txt'):
        fin = open(sys.argv[1], 'r')
        for line in fin:
            tupleLog= line.strip()
            if len(tupleLog) > 0:
                record=tupleLog.split(';')
                S.append(record)    
                
        fin.close()
        print 's',S
    
    
    elif(extension == 'csv'):
        fin  = open(sys.argv[1], "r")
        reader = csv.DictReader(fin)
        fields= reader.fieldnames 
        print fields   
        for row in reader:
            event=[]
            for i in range(0, len(fields)):
                event.append(row[reader.fieldnames[i]])
            S.append(event) 
            
        fin.close()
        print 's',S
    
    
    # reading and preparing T input 2
    print "reading Activity execution times metadata"
    T=dict()
    fin  = open(sys.argv[2], "r")
    reader = csv.DictReader(fin)
    rownum = 0
    fields= reader.fieldnames
    print fields
    for row in reader:
    
            heuristic=[]
            for i in range(1, len(reader.fieldnames)):
                heuristic.append(float(row[reader.fieldnames[i]]))
            T[row[reader.fieldnames[0]]]=heuristic   
    
    fin.close()
    print 'T' ,T
    
    rs=int(sys.argv[3])
    if (rs >0):
        GivenConfidenceLevel=rs
    
    
    start_time_algorithm = time.clock()
    print "start apply labeling algorithm"
    alg=Algorithm(S,T,M,Parents,startActivity,GivenConfidenceLevel)  
    #alg.apply_algorithm() # old: running batch of S all at once 
    
    dashboard_filename = "dashboard.csv"
    header = ['Current timestamp;Case id;Actual timestamp;Activity;Ranking score']
    f = open(dashboard_filename,'wb')
    w = csv.writer(f, delimiter = ',')
    w.writerows([x.split(';') for x in header])
    f.close()
    
    # reading and preparing S, input 4 (offline/online)
    #new part code, changing call of apply_algorithm
    start_time_build_tree = time.clock()
    if (sys.argv[4].lower()=="offline"):
        for symbol in S:
            alg.apply_algorithm(symbol,dashboard_filename) # new: read symbol by symbol from S either online or offline
    
        # reach this code when offline
        end_time_build_tree = time.clock()
        print"Algorithm execution time time_build_tree :  %s seconds " % (end_time_build_tree - start_time_build_tree)
        
        alg.finish_algorithm(start_time_build_tree)
        end_time_algorithm=time.clock()
        
        print "event logs"
        i =1
        for eLog in alg.constructedTraces:
            if(i==1):
                #eLog.write_traceLog_into_file_csv(i)
                #eLog.write_traceLog_into_file_txt(i)
                eLog.write_traceLog_into_XML(i)
            eLog.prepare_traceLog(i)
            i+=1
        #print other traces that have produces but not completely fit
        if (len(alg.otherConstructedTraces)>0):
            print "other event logs "
            for oeLog in alg.otherConstructedTraces:
                #oeLog.write_traceLog_into_file_csv(i,otherDirectory)
                #oeLog.write_traceLog_into_file_txt(i,otherDirectory)
                oeLog.write_traceLog_into_XML(i,otherDirectory)
                oeLog.prepare_traceLog(i)
                i+=1
        
        print"program execution time : %s seconds " % (time.time() - start_time_program)
        print"Algorithm execution time :  %s seconds " % (end_time_algorithm - start_time_algorithm)

    
    '''
    ##########################################################################
    '''
    if (sys.argv[4].lower()=="online"):     

        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
        path = "C:/Iman/My Docs/VS2013-Projects/SimulatingEvents/SimulatingEvents/bin/Debug"
        #path = sys.argv[1] if len(sys.argv) > 1 else '.'
        #event_handler = LoggingEventHandler()#it displays the automatic output of modified file
        event_handler = MyHandler()# customized reaction to modified file
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(0)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
            
    '''
    ##########################################################################
    '''
    