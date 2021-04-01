import matplotlib.pyplot as plt
import os
import pygmo as pg
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


experiments = ['focusing']
for exp in experiments:
    dircrty = "./" + exp + "/"
    fshort, fcandidate, ftest = getFileNames(dircrty)
    interactions = list()
    for filename in fcandidate:
        interactions.append(getInteractions(filename))
    layers_count = list()
    front_members_count = list()
    last_layers_count = list()

    for arun in range(len(interactions)):
        ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(interactions[arun])
        layers_count.append(len(ndf))
        front_members_count.append(len(ndf[len(ndf) - 1]))
        last_layers_count.append(len(ndf[0]))
    print(np.mean(front_members_count), np.mean(last_layers_count), np.mean(layers_count))
    plt.boxplot([last_layers_count, front_members_count, layers_count])
    plt.xticks([1, 2, 3],['#solution in last layer', '#solutions in front', '#Pareto layers'])
    plt.ylabel("Maximum Possible Number of Pareto Layers")
    plt.title("Distribution of candidate solutions in PHCP-UHSelection")
    plt.ylim(1, 100)
    plt.savefig("layers.png")
    plt.show()
