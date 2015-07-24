'''
This code is copyrighted to Dina Bayomie and Iman Helal @2015 Research work
Information System Department, Faculty of computers and Information System
Cairo University, Egypt

@author:  Dina Bayomie, Iman Helal
'''
#from tree import Tree
#from branch import Branch
#from traceLog import TraceLog
#from branchTree import BranchTree
from tree import Tree
from traceLog import TraceLog
from branch import Branch

import math
#import itertools
# to access the bp object
#from py4j.java_gateway import JavaGateway
import time 
#start run time of program
start_time_program = time.time()

class Algorithm:
    '''
    classdocs
    '''
    S = []  # Extracted unlabeled Sequence from File directly [timestamp , activity]
    T = dict()
    M = dict()
    Parents = dict()
    GivenConfidenceLevel = 0
    
    activitiesProb = dict()  # check to small letter
    
    traces = Tree()    
    tracesLeafs = []
    eventLogsDic = dict()#<key :case id,value:list of nodes added in traces tree>
    eventLogsIdForCases = dict()#<key : case id , value [ids used for this case in eventLogsDic ]
    eventLogID = 1
    currentCaseBranch = []
    constructedTraces = []#right traces
    otherConstructedTraces = []#that may missing some events or cases
    branchId = 1
    #BranchConfidenceLevel = dict() # key leaf node : value calculated
    #confidence level p(leaf| branch)
    #Branches = []
   
    root = None  # root of traces\cases tree [tree]
    branchRoot = None  # root of traceLogs tree [branchTree]
    branches = []
    startActivity = ''
    totalBranchesConfidenceLevel = 0.0  # 1.0
    numOfCases = 0
    CasesBranches = dict()

    def __init__(self, S, T, M, Parents, startActivity, GivenConfidenceLevel):
        self.M = M
        self.Parents = Parents
        self.T = T
        self.S = S
        self.startActivity = startActivity
        self.traces.add_node(1, 1, 0, 'start', 0, None)
        #self.eventLogsDic[self.eventLogID]=[]
        self.root = self.traces.get_root()
        self.calculate_activity_probability(self.S)
        self.GivenConfidenceLevel = GivenConfidenceLevel
   
    def trunc(self, number, digit=4):
        return (math.floor(number * pow(10, digit) + 0.5)) / pow(10, digit)
    
    '''Calculate probability of each activity withing giving sequence'''
    def calculate_activity_probability(self, sequence):
        sequnceLength = len(sequence)
        appearances = dict()
        for curr in sequence:
            if(not appearances.has_key(curr[1])):
                appearances[curr[1]] = 1.0
            else:
                appearances[curr[1]] = appearances[curr[1]] + 1.0
        for a in appearances:
            value = self.trunc(appearances[a] / sequnceLength, 4)
            self.activitiesProb[a] = value
    
    def distinct_possible_cases(self, possibleNodes):
        distinctNodes = []
        for n in possibleNodes:
            if(n not in distinctNodes):
                distinctNodes.append(n)
        return distinctNodes 
         
    '''Explore all possible cases for each symbol'''    
    
    def check_possible_branches_based_on_Model(self, symbol):
        possibleNodes = dict()
        event = symbol[1]  
        
        if(event == self.startActivity):     
            possibleNodes[self.root] = None
            
        else: 
            for l in self.tracesLeafs:#self.traces.get_leafs(self.root):
                node = l
                while (node != self.root):
                    activity = node.activity
                    relation = self.M.get(activity).get(event)
                    
                    if(relation.lower() == "seq"):
                        
                        arrParents = self.Parents[event]
                        
                        flag = 0
                        for j in range(0, len(arrParents)):
                            if(len(arrParents) == 1):
                                possibleNodes[node] = None
                                break
                            
                            if(flag == 1):
                                break
                            for i in range(1, len(arrParents)):
                                if i == j :
                                    continue
                                rel = self.M.get(arrParents[j]).get(arrParents[i])
                                if(rel == 'and'):
                                    f1 = self.traces.check_existance_in_branch(node, arrParents[j])
                                    f2 = self.traces.check_existance_in_branch(node, arrParents[i])
                                    if(f1 and f2):
                                        possibleNodes[node] = None
                                        flag = 1
                                        break
                            
                                elif(rel == 'xor'):
                                    possibleNodes[node] = None
                        break
                    elif(relation.lower() == "xor"):                        
                        node = node.parent
                        continue
                    elif(relation.lower() == "and"):
                        isExist = self.traces.check_existance_in_branch(node, event)
                        if(not isExist):
                            modelSeqNode = None
                            arrParents = self.Parents[event]
                            for p in arrParents:
                                modelSeqNode = self.traces.get_existed_activity_in_branch(node, p)
                            
                            possibleNodes[node] = modelSeqNode
                        node = node.parent
                        continue
                    elif(relation.lower() == "none"):
                        node = node.parent
                        continue
               
        return possibleNodes            

    '''Heuristic calculation method [min, avg , max]'''
    def check_possible_branches_based_on_heuristics(self, symbol, possibleNodes):
        symbolTimestamp = symbol[0]
        avgArr = []
        minArr = []
        maxArr = []
        metadataTime = self.T.get(symbol[1])
        for n in possibleNodes:
            node = n
            if(possibleNodes[n] != None):
                node = possibleNodes[n]
                
            if(n == self.root):
                avgArr.append(n)
                continue            
            diff = int(symbolTimestamp) - int(node.timestamp)
            if(diff == metadataTime[1]):
                avgArr.append(n)
            elif diff >= metadataTime[0] and diff < metadataTime[1]:
                minArr.append(n)
            elif diff > metadataTime[1] and diff <= metadataTime[2]:
                maxArr.append(n)     
        calcPool = {'avg':avgArr, 'min':minArr, 'max':maxArr}
        return calcPool
    
    '''need to change how it handel if all  in average '''
    
    '''calculate given probability of  node per branch'''
    def calculate_percentage(self, calcPool, highestPriority='avg'):
        calcPrecentage = dict()
        noOfCases = len(sum(calcPool.values(), []))
        otherHeuristic = list(set(sum(calcPool.values(), [])) - set(calcPool[highestPriority]))
        noOfHighestPriority = len(calcPool[highestPriority])
        noOfOtherHeuristic = len(otherHeuristic)
        total = 0
        totalNumber = noOfCases * noOfCases
        if(noOfCases == 1):
            totalNumber = 1#2.0
        totalNumber *= 1.0
        if(noOfOtherHeuristic > 0):
            for a in calcPool[highestPriority]:
                calcPrecentage[a] = ((noOfCases + 1.0) / totalNumber)
                total += calcPrecentage[a]
            for m in otherHeuristic:
                calcPrecentage[m] = ((noOfCases - (noOfHighestPriority * 1.0 / noOfOtherHeuristic * 1.0)) / totalNumber) * 1.0
                total += calcPrecentage[m]
        else:
            for a in calcPool[highestPriority]:
                calcPrecentage[a] = ((noOfCases) / totalNumber)
                total += calcPrecentage[a]                    
            
        return calcPrecentage   
    
    '''Return all possible nodes based on model and heuristic calculation'''
    def filter_possible_cases(self, symbol):
        
        possibleCasesFromM = self.check_possible_branches_based_on_Model(symbol)
        calcPool = self.check_possible_branches_based_on_heuristics(symbol, possibleCasesFromM)
        possibleNodes = self.calculate_percentage(calcPool, 'avg')
        
        return possibleNodes   

     
    '''building tree for given unlabeled event log and distribute the event to cases tree '''
    # add fun to remove all keys that have 1 branch from dic
    def build_branches_tree(self):
               
        labelCaseId = 1
        for symbol in self.S:
            dictionary = self.filter_possible_cases(symbol)
            numPossibleBranches = len(dictionary)
            for n in dictionary :
                caseId = n.caseId
                if(caseId == 0):
                    caseId = labelCaseId
                    labelCaseId = labelCaseId + 1        
                percentage = dictionary[n]  
                symbolNode = self.traces.add_node(percentage, 1.0 / numPossibleBranches, symbol[0], symbol[1], caseId, n)
                # keep trace for leafs instead of traverse multiple time on
                # tree
                if(n in self.tracesLeafs):
                    self.tracesLeafs.remove(n)
                if(symbolNode not in self.tracesLeafs):
                    self.tracesLeafs.append(symbolNode)


    
    '''Calculate confidence level for each branch in cases traces tree and also build the branches trace log tree'''
    # will change this function so instead of adding to tracelog tree it will
    # add branch to event log dict
    def calculate_confidence_level_branch(self):
        #self.CasesBranches = dict()
        self.branchId = 1
        tracesLeafs = sorted(self.tracesLeafs, key=lambda Node: Node.caseId) 
        eventLogsIdForCases = dict()# <key case id ,value [] of eventlog id used for this case>store ids used per
                                    # case so when start new case remove all un
                                                                        # used
                                                                                                            # event
                                                                                                            # log
                                                                                                            # to
                                                                                                            # decrease
                                                                                                            # the
                                                                                                            # size
        isDicClean = False
        duplicateEL = []
        for leaf in tracesLeafs:#self.traces.get_leafs(self.root):
            nodes = []
            caseId = leaf.caseId
            # create branch
            if(leaf.parent != self.root):
                nodes = self.traces.get_branch_nodes(leaf, nodes)
            else:
                nodes.append(leaf)
            branch = Branch(self.branchId, caseId, nodes) 
            self.branchId += 1
            #print "case id : ",caseId," timestamp : ",branch.timestampList
            
            #handle first case
            if(branch.caseId == 1):
                newEvents = []
                newEvents.append(branch)
                isAdded = False
                for eLogID in self.eventLogsDic:
                    cb = self.getBranch(self.eventLogsDic[eLogID],caseId)
                    if(cb != None):
                        diff = list(set(branch.timestampList) - set(cb.timestampList))
                        if(len(diff) == 0):
                            isAdded = True
                            continue
                        if(set(branch.timestampList).issuperset(set(cb.timestampList))):
                            if(self.checkEventLogExistance(newEvents,self.eventLogsIdForCases,1)):
                                #del self.eventLogsDic[eLogID]
                                duplicateEL.append(eLogID)
                                continue
                            self.eventLogsDic[eLogID].remove(cb)
                            self.eventLogsDic[eLogID].append(branch)
                            isAdded = True
                            #if(self.checkEventLogExistance(self.eventLogsDic[eLogID],self.eventLogsIdForCases[1],1)):
                            #    del self.eventLogsDic[eLogID]
                            #    continue
                            continue
                if(not isAdded):
                    self.eventLogsDic[self.eventLogID] = newEvents
                    if(not self.eventLogsIdForCases.has_key(caseId)):
                        self.eventLogsIdForCases[caseId] = []
                    self.eventLogsIdForCases[caseId].append(self.eventLogID)
                    self.eventLogID+=1
                continue
            
            # handle comin\ following cases
            if(len(duplicateEL)>0):#(not isDicClean):
                for eLogID in duplicateEL:
                    del self.eventLogsDic[eLogID]
                self.eventLogsIdForCases[caseId - 1] = [x for x in self.eventLogsDic.keys()]
                duplicateEL=[]
                

            if(self.eventLogsIdForCases.has_key(caseId - 1)):
                currentEventLogIds = self.eventLogsIdForCases[caseId - 1]
            else:
                currentEventLogIds = [x for x in self.eventLogsDic.keys()]
            
            #currentEventLogIds=[x for x in self.eventLogsDic.keys()]
            #print "size of all dic",len(self.eventLogsDic)
            #print "size of of prev case",len(eventLogsIdForCases[caseId-1])
            currentEventLogIds = list(sorted(currentEventLogIds))
            for eLogID in currentEventLogIds:#tempCaseBranches:
                branches = self.eventLogsDic[eLogID]
                #conflictBranches = self.conflictBranch(branch, branches)
                # get conflict branches then check if the conflicted branches
                # containg 1 case or previous case then ignore other wise check
                #if its a repeated sequence of branches then ignore , otherwise
                #add a new event log data normally
                # and if there is no conflicted branches then add the branch to
                # the current event log
                conflictBranches = self.CheckViolatingBranches(branch, branches)                
                if(len(conflictBranches) > 0):
                    #that's mean no case can be added wihout its previous cases
                    #as thats normal im searching for combination between
                    #branches
                    #while handling all noise will occurs at labelling level
                    if(self.checkParentCasesExistence(conflictBranches,caseId)):
                        continue
                    cb = self.getBranch(conflictBranches,caseId)
                    if(cb != None):
                        diff = list(set(branch.timestampList) - set(cb.timestampList))
                        if(len(diff) == 0):
                            continue
                        if(set(branch.timestampList).issuperset(set(cb.timestampList))):
                            self.eventLogsDic[eLogID].remove(cb)
                            self.eventLogsDic[eLogID].append(branch)
                            continue
                        elif(set(cb.timestampList).issuperset(set(branch.timestampList))):
                            continue
                    newEvents = list(set(branches) - set(conflictBranches))
                    newEvents.append(branch)
                    duplicateEL=self.checkEventLogExistance(newEvents,self.eventLogsIdForCases,caseId)
                    #if(len(duplicateEL)>0):
                    #    continue
                   
                    self.eventLogsDic[self.eventLogID] = newEvents
                    if(not self.eventLogsIdForCases.has_key(caseId)):
                        self.eventLogsIdForCases[caseId] = []
                    if(self.eventLogID not in self.eventLogsIdForCases[caseId]):
                        self.eventLogsIdForCases[caseId].append(self.eventLogID)
                    self.eventLogID+=1
                else:
                    self.eventLogsDic[eLogID].append(branch)
                    if(not self.eventLogsIdForCases.has_key(caseId)):
                        self.eventLogsIdForCases[caseId] = []
                    if(eLogID not in self.eventLogsIdForCases[caseId]):
                        self.eventLogsIdForCases[caseId].append(eLogID)
      

            
    def checkParentCasesExistence(self,branches,caseId):
        #isExist=False
        for b in range(len(branches) - 1,-1,-1): #branches:
            if(branches[b].caseId in range(1,caseId)):
                return True
        return False
    def getBranch(self,branches,caseId):
        for b in range(len(branches) - 1,-1,-1): #branches:
            if(branches[b].caseId == caseId):
                return branches[b]
        return None
    def checkEventLogExistance(self,newEvents,eventLogsIdForCases,caseId):
        #for elogId in self.eventLogsDic:
        dublicated = []
        if(eventLogsIdForCases.has_key(caseId)):
            for elogId in eventLogsIdForCases[caseId]:
                if(set(newEvents).issuperset((self.eventLogsDic[elogId]))):
                  dublicated.append(elogId)  
        '''
        for elogId in range(len(self.eventLogsDic),0,-1):
            if(set(newEvents) == set(self.eventLogsDic[elogId])):
                return True
        '''
        return dublicated
    '''@return True if branch is from the same case of any of the branches or has common timestamp event , False otherwise '''       
    # need to change return from just boolean to conflict branch so i can slice
    # this branch from the log'''
    #def conflictBranch(self, branch, branches):
        #conflictBranches = self.CheckBranchesPerCase(branch, branches)
        #conflictBranches.extend(self.CheckViolatingBranches(branch, branches))
        #conflictBranches=self.distinct_possible_cases(conflictBranches)
        #conflictBranches=self.CheckViolatingBranches(branch, branches)
        #return conflictBranches
           
          
            
    #def CheckBranchesPerCase(self, selectedBranch, remainingBranches):
        #isSameCaseId = False
        #violatedBranch=[]
        #for rb in range(len(remainingBranches)-1,-1,-1):
            #if(remainingBranches[rb].caseId == selectedBranch.caseId):
                #violatedBranch.append(remainingBranches[rb])
        #return violatedBranch
    
    def CheckViolatingBranches(self, selectedBranch, remainingBranches):
        #isSameTimestamp = False
        violatedBranches = []
        for rb in range(len(remainingBranches) - 1,-1,-1):
            intersect = list(set(remainingBranches[rb].timestampList).intersection(set(selectedBranch.timestampList)))
            if len(intersect) != 0:
                violatedBranches.append(remainingBranches[rb])  
            if(remainingBranches[rb].caseId == selectedBranch.caseId):
                violatedBranches.append(remainingBranches[rb])  
        violatedBranches = self.distinct_possible_cases(violatedBranches)

        return violatedBranches 
          

    def build_traceLog(self):
        traceLogId = 1
        for elogId in self.eventLogsDic:
            branches = []
            branches = self.eventLogsDic[elogId]
            if(len(branches) == self.numOfCases):
                traceLogObject = TraceLog(traceLogId,branches,self.activitiesProb,self.root)
                #if(len(branches)==self.numOfCases and
                #len(traceLogObject.events)==len(self.S) and
                #traceLogObject.confidenceLevel >= self.GivenConfidenceLevel):
                if(len(traceLogObject.events) == len(self.S) and traceLogObject.confidenceLevel >= self.GivenConfidenceLevel):
                    #print "the same no of cases"
                    self.constructedTraces.append(traceLogObject)
                else:
                    self.otherConstructedTraces.append(traceLogObject)
                traceLogId+=1

    def apply_algorithm(self):
        print "build cases tree"
        start_time_build_tree = time.clock()
        self.build_branches_tree()
        self.numOfCases = len(self.root.children)
        end_time_build_tree = time.clock()
        print"Algorithm execution time time_build_tree :  %s seconds " % (end_time_build_tree - start_time_build_tree)

        print "number of cases in given event log : ",self.numOfCases
        self.traces.display(self.root)
        print "prepare labeled event logs "
        print "construct branches tree from cases tree"
        start_time_build_tree = time.clock()
        self.calculate_confidence_level_branch()
        end_time_build_tree = time.clock()
        print"Algorithm execution time build event log dic :  %s seconds " % (end_time_build_tree - start_time_build_tree)
        print "total num of branches ", self.branchId
        print "total number of branches combinations ", len(self.eventLogsDic)

        #self.traceLogsTree.display(self.branchRoot)
        print "compose event logs from branches tree"
        start_time_build_tree = time.clock()

        self.build_traceLog()
        end_time_build_tree = time.clock()
        print"Algorithm execution time build_traceLog :  %s seconds " % (end_time_build_tree - start_time_build_tree)


        self.constructedTraces = sorted(self.constructedTraces, key=lambda TraceLog: TraceLog.confidenceLevel, reverse=True)
        #print "number of labeled event logs :" , self.constructedTraces
