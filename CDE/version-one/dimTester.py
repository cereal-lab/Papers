import sys
import numpy as np
import scipy.stats as stats
import deca
import itertools
import collections

def getDataset(fileName):
  
  f = open(fileName)
  lines = f.readlines()
  f.close()

  stdId = 0
  stuDS = dict()
  numProblems = 0
  for line in lines:
    try:
      fields = line.strip().split()
      probId = 0
      probDS = dict()
      
      for field in fields:
        dic = dict()
        dic['problem'] = probId
        score = float(field)
        dic['score'] = score
        dic['time'] = -1
        probDS[probId] = dic
        probId += 1
        
      stuDS[stdId] = probDS
      stdId += 1 
      numProblems = max(numProblems, len(fields))
      
    except:
      print "Warning:  Could not process line: ", line 
  numStudents = len(stuDS)
  return stuDS, numProblems

def compareBothVersions(fileInteraction):
  dataset , numProblems  = getDataset(fileInteraction) 
  probletSubset = set(range(numProblems))
  rawTests  = deca.cleanupForProbletAnalysis(dataset, probletSubset)    
  rawTestsBackup = rawTests[:] 
  filteredTests = deca.filterTests(rawTests)
  fTestsAnother = deca.filterTestsModified(rawTestsBackup)
  print len(filteredTests), len(fTestsAnother)
  dim = deca.extractDimensions(filteredTests)
  dim2 = deca.extractDimensions(fTestsAnother)
  print len(dim), len(dim2)
 
if __name__ == '__main__':
  fileName = "job.0.interaction.txt.problem.100by100"
  compareBothVersions(fileName)  
