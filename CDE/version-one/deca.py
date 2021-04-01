import itertools
import sys, os
import numpy as np

import random

def cleanupForProbletAnalysis(results, probletSubset, scoreThreshold = 1.0):
  """
  Filter the data for doing problem-based analysis:
    * Strip out students for whom there's no response on
      the specified problems;
    * Set the 'testResult' to True for each problem that
      the student got at least one wrong;
    * Organize as a list of tuples, where each tuple is a problem and
      the tuple is the vector of results of what students solved
      that problem correctly;
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
      # Paul, did you mean to include when correct < total or should this have been correct >= total?
      # Amruth, For problet analysis, a 'win' for the problet is when the student gets at least one wrong 
      resultList.append(results[student][problem]['score'] < scoreThreshold)
    testResult = tuple(resultList)
   # Ensures only one copy of tests with a specific result configuration
    # is retained (i.e., preserves uniqueness of result)
    testDict[testResult] =  (testResult, sum(testResult), problem)

  return testDict.values()

def mooCompare(v1, v2):
  """
  Compare two vectors in a multiobjective sense.  This routine returns two values.
  The first indicates whether or not the two vectors can be compared in terms of
  total ordering.  The second returns the result of the comparison, assuming they
  can be compared.  If the two vectors are equal, it returns True and 0.  If the
  first vector Pareto dominates the second, return True and 1.  If the second
  Pareto dominates the first, return True and -1.  Otherwise it returns False and
  0, though the zero value is meaningless in this case.
  """
  a = np.array(v1)
  b = np.array(v2)  
  
  if all(a==b):
    return True, 0
  elif all(a >= b) and any(a > b):
    return True, 1
  elif all(b >= a) and any(b > a):
    return True, -1
  else:
    return False, 0
  
  
    
def extractDimensions(filteredTests):
  """
  Construct the geometric dimensions of interaction comparisons
  according the Anthony Bucci's dimensions extraction method from:

    Bucci, Pollack, & de Jong (2004).  "Automated Extraction
    of Problem Structure".  In Proceedings of the 2004 Genetic
    and Evolutionary Computation Conference.

  The routine returns a list of dimensions.  Each dimension
  corresponds to an underlying objective of the problem.  The
  dimension is itself a list of tests such that:

    1) All tests in a given dimension are comparable; and
    2) They are ordered in terms of Pareto dominance.
  """

  dimensions = []  
  # A list of list of tuples
  dimIdx = 0    

  for test in filteredTests:
    wasInserted = False
    #print idx, "idx", "\n"
    for dim in dimensions: 
      comparable, compareValue = mooCompare(dim[-1][0],test[0])
      ## index 0 in test[0] means the interaction outcome of that test  
      if comparable :
        # The dimensions must be inserted at the end or there will
        # be comparison problems because of boundary cases (e.g.,
        # when all tests are passed or failed, etc.)
        dim.append(test)
        wasInserted = True
        break
      # wasInserted = insertTestIntoDimension(dim,test)
    
    if not wasInserted:
      dimensions.append( [test] )
      dimIdx += 1
    #print test, "vs ", dimensions, "dim Index", dimIdx, "\n"
    
  # We appended tests to the end, so the axes are backward.  Fix
  # this so that they are ordered correctly.
  for dim in dimensions:
    dim.sort(key=lambda x: x[1])
  #print "dimensions: ", dimensions, "\n"

  # The data structure that is returned is a list of each axis (dimension) with the
  # tests embedded into these dimensions as lists of tuples, ordered by the number
  # of passes or fails.  In the case of problets, each axis is ordered from the test
  # that fewer students fail to the problet where more students fail ... but all 
  # problets along an axis are comparable.  In the case of the students, each axis
  # is ordered from the student who passes the fewest problets to the student who
  # passes the most.  Again, all students on an axis are comparable.  That is:  the
  # leaf nodes are always the most dominant problemts or students (depending on the
  # analysis)    
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

def filterTestsModified(tests):
  """
  This function sorts and filters the data to ensure no unnecessary redundancies
  in configuration of results and also sorts them on number of Fails in ascending
  order
  """
    
  tests.sort(key=lambda x: x[1])
  tests.reverse()    
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

def filterTests(tests):
  """
  This function sorts and filters the data to ensure no unnecessary redundancies
  in configuration of results and also sorts them in order of the number of
  successful tests.
  """
  tests.sort(key=lambda x: x[1]) 
  tests.reverse()  
  keeping  = []
  keeping.append(tests.pop(0))
  keeping.append(tests.pop(0))
  
  for test in tests:
    t1 = keeping[-1][0]
    t2 = keeping[-2][0]
    t3 = test[0] 
    if not (t3 == tupleAnd(t1,t2)):
      keeping.append(test)
  return keeping































