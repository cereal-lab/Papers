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

def dimTesterForProblems(fileInteraction):
  dataset , numProblems  = getDataset(fileInteraction) 
  probletSubset = set(range(numProblems))
  rawTests  = deca.cleanupForProbletAnalysis(dataset, probletSubset)
  print len(rawTests)

  filteredTests = deca.filterTestsZeroAsFails(rawTests) 
  print len(filteredTests) 
 
  dims = deca.extractDimensionsZeroAsFails(filteredTests)
  deca.summarizeProbletAnalysis(dims, numProblems) 
  print "#dim ", len(dims)
    
if __name__ == '__main__':
 
  fileName = "job.0.interaction.txt.learner.9by9" 
  dimTesterForProblems(fileName) 
  
