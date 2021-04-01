from matplotlib import pyplot as plt
import os
from pygmo import *
import numpy as np

dircrty = ""

def getInteractions(filename):
    file = open(dircrty+filename, "r")
    lines = file.readlines()
    file.close()
    tmp = list()
    for line in lines:
        fields = line.split()
        outcomes = [float(o) for o in fields[3:]]
        #pygmo documentation: making a maximization as minimication for analysis
        # http://esa.github.io/pygmo/tutorials/adding_a_new_optimization_problem.html#maximization-problem
        #outcomes = [np.sum(outcomes[:20])*-1.0, np.sum(outcomes[20:40])*-1.0, np.sum(outcomes[40:60])*-1.0, np.sum(outcomes[60:80])*-1.0, np.sum(outcomes[80:100])*-1.0]
        outcomes = [np.sum(outcomes[:50]), np.sum(outcomes[50:100])]
        #print outcomes
        tmp.append(outcomes)
    return tmp


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


#experiments = ['phcp', 'phcpuhs']
experiments = ['phcpuhs']
hypervolumes = []
for exp in experiments:
    dircrty = "./" + exp + "/"
    fshort, fcandidate, ftest = getFileNames(dircrty)
    #interactions = list()
    volume = list()
    #x = [1.0, 1.0, 1.0, 1.0, 1.0]
    x = [51.0, 51.0]
    for filename in fcandidate:
        #interactions.append()
        hv = hypervolume(getInteractions(filename))
        #print getInteractions(filename)
        volume.append(hv.compute(x, hv_algo = hvwfg()))
    hypervolumes.append(volume)
#print hypervolumes
#print np.mean(hypervolumes[0]), np.mean(hypervolumes[1])
fig = plt.figure()
y = getInteractions(fcandidate[1])
ax = plot_non_dominated_fronts(y)
fig.savefig("abc.png")
extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig('ax2_figure.png', bbox_inches=extent)
#plt.title("Pareto front for relaxed selection")
#plt.xlabel("first Objective")
#plt.ylabel("Second Objective")
#plt.ylim(0.0, 50.0)
#plt.xlim(0.0, 50.0)
#plt.savefig("base.png")
#plt.show()
