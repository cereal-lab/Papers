import matplotlib.pyplot as plt
import os
import numpy as np

dircrty = ""
def getBstObjFitsInARun (filename, entity):
    file = open(dircrty+filename, "r")
    columnId = 2 if entity == 0 else 6
    lines = file.readlines()
    bstfit = list() #for monotonic visualization, not applicable for statistical analysis
    relative_bst = list() #performance measure and statistical analysis
    for line in lines:
        fields = line.split()
        bstfit.append(float(fields[columnId]))
        relative_bst.append(float(fields[columnId - 1])/float(fields[columnId])) # bst/bst_so_far
    return bstfit, relative_bst

def getFileNames(explocation):
    for root, dirs, filenames in os.walk(explocation):
        filesShort, filesCandidate, filesTest = [], [], []
        for afile in filenames:
            if "Short" in afile:
                filesShort.append(afile)
            elif "candidate" in afile:
                filesCandidate.append(afile)
            elif "test" in afile:
                filesTest.append(afile)
        return (sorted(filesShort), sorted(filesCandidate), sorted(filesTest))

def analyzeObjectiveFit(fshort):
    bst_relative = list()
    objfits_sample = list()
    for filename in fshort:
        tmp_bst, tmp_relbst = getBstObjFitsInARun(filename, 0) #TODO - put it in constant file
        objfits_sample.append(tmp_bst)
        bst_relative.append(tmp_relbst)
    bst_fit_byrun = np.array(objfits_sample)  #run x gen
    bst_fit_bygen =   np.transpose(bst_fit_byrun) # gen x run
    avgfit_bygen = np.mean(bst_fit_bygen, axis = 1)

    bst_rel_byrun = np.array(bst_relative) #run x gen
    return (avgfit_bygen, bst_rel_byrun)
    #print np.shape(bst_fit_bygen), np.mean(bst_fit_bygen), np.std(bst_fit_bygen)
    #plt.boxplot(bst_fit_bygen)
    #plt.show()

experiments = ['componone','focusing','intransitive']
gen = [x for x in range(500)]
objGraph = list()
bst_relative = list()
for exp in experiments:
    dircrty = "./" + exp + "/"
    fshort, fcandidate, ftest = getFileNames(dircrty)
    bst_fit, bst_relative_arr = analyzeObjectiveFit(fshort)
    objGraph.append(bst_fit)
    bst_relative.append(bst_relative_arr)
print len(objGraph)
fig, axes = plt.subplots(1, 3, sharey = True)
axes[0].plot(gen, objGraph[0])
axes[0].set_title("CompOnOne")
axes[0].set_xlabel("Generations")
axes[0].set_ylabel("Performance (Sum of Genes)")
axes[1].plot(gen, objGraph[1])
axes[1].set_title("Focusing")
axes[1].set_xlabel("Generations")
axes[1].set_ylabel("Performance (Sum of Genes)")
axes[2].plot(gen, objGraph[2])
axes[2].set_title("Intransitive")
axes[2].set_xlabel("Generations")
axes[2].set_ylabel("Performance (Sum of Genes)")

fig.savefig("games.png")
plt.show()
