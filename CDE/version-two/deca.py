import itertools
import sys, os
import numpy as np

import random

def cleanupForProbletAnalysis(results, probletSubset, one = 1.0):
  """
  Filter the data for doing problem-based analysis:
    * Strip out students for whom there's no response on
      the specified problems;
    * Set the 'testResult' to True for each problem that
      the student got at least one wrong;
    * Organize as a list of tuples, where each tuple is a problem and
      the tuple is the vector of results of what students solved
      that problem correctly;
    ***[agb:] This version does not throw the duplicates out. Because the 
    ***[agb:] the original algorithm in Bucci 2004 et.al., does not have
    ***[agb:] this flavor. So, the function just preprocess the data.
    * Throw out duplicates of specific result configurations.
  """
  # Use only students that have taken the specified problets
  students = []
  intersectedProblets = set()
  for student in results:
    studentProbletSet = set(results[student])
    #print "ddd student = " , student , "  " , studentProbletSet , "   ", intersectedProblets, "   ", probletSubset
    if probletSubset.issubset(studentProbletSet):
      #print "ddd =" 
      students.append(student)
      if len(intersectedProblets) == 0:
        intersectedProblets = studentProbletSet
      else:
        intersectedProblets = intersectedProblets.intersection(studentProbletSet)
        #print student, ", ", studentProbletSet, " , ", intersectedProblets, "\n"
  #print intersectedProblets, "\n"
  students.sort()
  problems = list(intersectedProblets)
  problems.sort()

  #print "Results", results[0][1]['score'], "\n" 
  #print "dbd", problems
  # For each problem and student, give a 'True' if the student
  # got *all* instances of that problem correct and 'False' otherwise.
  testDict = {}
  for problem in problems:
    resultList = []
    for student in students:
      resultList.append( results[student][problem]['score'] == one)
    testResult = tuple(resultList)
    numFails = abs(len(testResult) - sum(testResult))
    testDict[problem] = (testResult, numFails, problem)
  return testDict.values()

def mooCompareZeroAsFails(v1, v2):
  a = np.array(v1)
  b = np.array(v2)  
  
  if all(a==b):                    # equal
    return True, 0
  elif all(a <= b) and any(a < b): # a Pareto dominates b i.e., 00 dominates 10
    return True, 1
  elif all(b <= a) and any(b < a): # b Pareto dominates a 
    return True, -1
  else:                            # non-comparable
    return False, 0
    
def extractDimensionsZeroAsFails(filteredTests):
  dimensions = []  
  # A list of list of tuples
  dimIdx = 0    
  for test in filteredTests:
    wasInserted = False
    #print idx, "idx", "\n"
    for dim in dimensions: 
      comparable, compareValue = mooCompareZeroAsFails(dim[-1][0],test[0]) 
      ## index 0 in test[0] means the interaction outcome of that test  
      if comparable: 
        # The dimensions must be inserted at the end or there will
        # be comparison problems because of boundary cases (e.g.,
        # when all tests are passed or failed, etc.)
        dim.append(test)
        wasInserted = True
        break
      #elif comparable and compareValue == -1: #the opposite of above if condition. is that even feasible?
      #  print "ERROR: MAY BE!!"
      # wasInserted = insertTestIntoDimension(dim,test)    
    if not wasInserted:
      dimensions.append( [test] )
      dimIdx += 1 
  return dimensions
  
def summarizeProbletAnalysis(dims, numProblets, byTemplate=False):
  """
  The result will be a print out of each separate problem dimension, with each
  problem in that dimension listed in order of Pareto dominance (the top one
  dominating the others, etc).  Also listed are the number of students who
  passed that test.
  """
  reductionRatio = (float(len(dims))/float(numProblets))
  print "There are ", len(dims), "underlying objectives to this PROBLET data of", numProblets, \
        "::", reductionRatio
    
  for dim in dims:
    if byTemplate:
      print "Count \tTemplate ID"
    else:
      print "Count \tProblem ID"
      
    for test in dim:
      print "  ", test[1], "\t", test[2]      
    print

  return reductionRatio


def tupleAnd(t1,t2):
  """
  A simple wrapper function that compares two tuples using logical And.
  It assumes the tuples are the same dimensionality and contain Booleans.
  """
  return map(lambda a,b: a and b,  t1,  t2)

def filterTestsZeroAsFails(tests):
  """
  This function sorts and filters the data to ensure no unnecessary redundancies
  in configuration of results and also sorts them on number of Fails in ascending
  order
  """
    
  tests.sort(key=lambda x: x[1]) 
  keeping  = [] 
  keeping.append(tests.pop(0))
  keeping.append(tests.pop(0))
 
  for test in tests:
    t1 = keeping[-1][0]
    t2 = keeping[-2][0]
    t3 = test[0]    
    if not (list(t3) == list(tupleAnd(t1,t2))):
      keeping.append(test)
   
  return keeping































