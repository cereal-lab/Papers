from operator import index
import os
from pprint import pprint, pformat
import re
import io
import csv 
import sys
import numpy as np

params = [ "vl1.n" ]
#statPath = "out.stat"
statPath = "target/classes/out.stat"
def cmd(p): 
    return f"cd target/classes && java ec.Evolve -file ec/domain/regression/{p}.params"
    #return f"java -cp ecj-27.jar ec.Evolve -from domain/regression/{p}.params -at ec.Evolve"

# pattern = re.compile('(?<=Standardized=)(.*?)(?=\.)')
pattern = re.compile('(?<=Standardized=)(.*?)\s')
def run(acc, cmd, n, expectedLen = 103):  #102 for bool domain
    for i in range(n):
        print(f"Running test {i}")
        os.system(cmd);
        with open(statPath, "r") as statFile:
            txt = statFile.read()
        res = [ float(s) for s in pattern.findall(txt) ]
        if len(res) < expectedLen: 
            res = res + [0 for i in range(expectedLen - len(res))]
        res.pop() #last is best fitness
        acc.append(res)
    return acc

def save(name, runs, mean, std, meanofmean):
    with open(name, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(runs)
        # wr.writerow(['mean', 'std'])
        # wr.writerow(mean)
        # wr.writerow(std)
        # wr.writerow(['meanofmean'])
        # wr.writerow([meanofmean])

def read(name):
    res = []
    with open(name, 'r', newline='') as csvfile:
        rd = csv.reader(csvfile)        
        for row in rd:             
            if row[0] == 'mean':
                break 
            res.append([float(v) for v in row]) #changed int to float
    return res; 

import scipy.stats as stats

import scikit_posthocs as sp

# def tvalue(f1, f2):
#     return stats.ttest_ind(f1, f2, equal_var=False)

# //https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test
# //https://projecteuclid.org/download/pdf_1/euclid.aoms/1177730491
# //https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
# def uvalue(f1, f2, alt='greater'):
    # res1 = read(f1)
    # lastGen1 = [ v[len(v) - 1] for v in res1 ]
    # res2 = read(f2)
    # lastGen2 = [ v[len(v) - 1] for v in res2 ]
    # return stats.mannwhitneyu(lastGen1, lastGen2, alternative=alt)
# //>>> uvalue("11.csv", "11-3.csv")
# //MannwhitneyuResult(statistic=1179.5, pvalue=0.6886706822413166    

# //https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html?highlight=kruskal
def hvalue(f1, f2):
    res1 = read(f1)
    lastGen1 = [ v[len(v) - 1] for v in res1 ]
    res2 = read(f2)
    lastGen2 = [ v[len(v) - 1] for v in res2 ]
    return stats.kruskal(lastGen1, lastGen2)
# >>> hvalue("11.csv", "11-3.csv")
# KruskalResult(statistic=0.23874997725577796, pvalue=0.6251104082753336)    

def bor(exp):
    ''' best of run, exp is (f1, f2, ...)
    '''
    return tuple([run[-1] for run in r1] for r1 in exp)

import pandas as pd

def allStats(fs):
    fsa = np.array(fs)
    # print(fsa)
    # print(fsa.T)
    moments = [ { "mean": np.mean(f), 'std1': np.std(f) } for f in fsa ]
    if len(fs) <= 2:         
        return { 'm_std': moments,
                # 'friedman': stats.friedmanchisquare(*fsa),
                # 'nemenyi': sp.posthoc_nemenyi_friedman(fsa.T) 
                'ttest': stats.ttest_ind(fs[0], fs[1], equal_var=False, alternative='two-sided'), 'utest': stats.mannwhitneyu(fs[0], fs[1],alternative='two-sided')
                }
    return { 'm_std': moments,
            'friedman': stats.friedmanchisquare(*fsa),
            'nemenyi': sp.posthoc_nemenyi_friedman(fsa.T) 
            # 'ttest': stats.ttest_ind(fs[0], fs[1], equal_var=False, alternative='two-sided'), 'utest': stats.mannwhitneyu(fs[0], fs[1],alternative='two-sided')
            }

    
    stats.friedmanchisquare(*fs)

# def allStats(f1, f2, althyp='two-sided'): 
#     return { 'mean1': np.mean(f1), 'std1': np.std(f1), 'mean2': np.mean(f2), 'std2': np.std(f2), \
#                 'ttest': stats.ttest_ind(f1, f2, equal_var=False, alternative=althyp), 'utest': stats.mannwhitneyu(f1, f2,alternative=althyp)}

def diag(f1, f2):
    res1 = read(f1)
    lastGen1 = [ v[len(v) - 1] for v in res1 ]
    res2 = read(f2)
    lastGen2 = [ v[len(v) - 1] for v in res2 ]
    print(sorted(lastGen1))
    print(sorted(lastGen2))


import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.lines as mlines
from matplotlib.axes import Axes



def charts(problems, file="test.png"): 
    ''' problems is [ [chart1Fs, chart2Fs, ...] ... ]
    chartFs is { [ f1, f2 ... ] + title info }
    f is all obtained fitnesses on all gens 
    so first we calc the size of chart 
    '''
    plt.clf()
    plt.subplots_adjust(hspace=1)
    fig, axs = plt.subplots(nrows=len(problems), ncols=len(problems[0]))

    # plts = []
    for (i, problemLine) in enumerate(problems): 
        for (j, problem) in enumerate(problemLine):
            ax = (axs[i,j] if type(axs) is np.ndarray else axs)
            for (k, f) in enumerate(problem['fs']): 
                fgens = np.transpose(f['data'])
                conf_int_gens = [ (mean, ) + stats.t.interval(0.95, len(gen)-1, loc=mean, scale=stats.sem(gen)) for gen in fgens for mean in [ np.mean(gen) ] ]
                gens = list(range(len(conf_int_gens)))
                
                ax.plot(gens, [m for (m, l, u) in conf_int_gens ], color=f['color'], label=f['title'], marker=f['marker'],ms=5, markevery=10, linewidth=1) #, linestyle="dotted")
                ax.set_xlabel("Generation")
                ax.set_ylabel("Fitness value")
                ax.fill_between(gens, [u for (m, l, u) in conf_int_gens ], [l for (m, l, u) in conf_int_gens ], color=[f['color'] + "20"])
            ax.legend(shadow=True, fancybox=True)
            # if problem['title'] is not None:
            #     ax.set_title(problem['title'])  
# axs[1].set_xlabel('time (s)')
# axs[1].set_title('subplot 2')
# axs[1].set_ylabel('Undamped')
    fig.tight_layout()
    plt.savefig(file)

def boxplots(problems, file="boxplot.png"): 
    """
        :param problems should be list of { "<label1>": [<value1>,...], "<label2>": ... }
    """
    # labels = [problem.label for problem in problems]
    # values = [problem.values for problem in problems]
    plt.clf()
    # plt.subplots_adjust(hspace=1)
    fig, ax = plt.subplots()
    ax.boxplot(problems.values()) #values, vert=True, patch_artist=True, labels=labels) 
    ax.set_xticklabels(problems.keys())
    # plt.ylabel(ylabel)
    # plt.title('Multiple Box Plot : Vertical Version')
    fig.tight_layout()
    plt.savefig(file)        

def groupMetrics(expResultFolder, experiments, problems, settings, metrics, skip=1, settingsFilter = {}, metricFilters={}):
    """
    :param expResultFolder = [ "data", "2022-04-15" ]
    :param experiments = ["7379006"]
    :param problems = [ "R1", "R2", "Kj3", "Kj4", "Kj11", "Ng9", "Ng12", "Pg1", "Vl1"]
    :param settings = {"RTsTx": [""], "RTsTmx": ["1", "10"], "RTsTxN": ["str1", "str2", "str3", "str4"] }    
    :param metrics = ["borSize", "borDepth", "meanSize", "meanDepth", "maxGen", "found", "ms", "borFitness", "borFitnessTestSet", "fitnessStdev", "aucRoc", "nroRate", "nroRevs"]
            metric parameter order should be same is in exp result file 
    :param skip - skip runId or any other params
    :param settingsFilter - filter datasetups which do not have specific metric
    :param metricFilters - filters outliners for different metrics
    :return stats in format { expId: {problemId: { metricId: {setupId: [value1, value2, ...]}}}}
    """
    stats = {}
    for e in experiments:
        stats[e] = {} #metrics for each settings and problems
        for p in problems:
            problemStats = {metric: {} for metric in metrics}
            stats[e][p] = problemStats
            for s, configs in settings.items():
                for c in configs:
                    resFolder = "-".join(part for part in [p, s, c, e] if part != "")                
                    resFilePath = os.path.join("", *(expResultFolder + [ resFolder, "exp.stat"]))
                    label = c if c != "" else s #", ".join(part for part in [s, c] if part != "")
                    for metric, metricValues in problemStats.items():
                        if s in settingsFilter and not settingsFilter[s](metric): 
                            continue
                        metricValues[label] = [];
                    print(f"Result path: {resFilePath}")
                    with open(resFilePath, 'r') as resFile:
                        for line in resFile.readlines():
                            if line != "":
                                metricValues = [ float(value.strip()) for value in line.split("\t") ][skip:]
                                for (metric, metricValue) in zip(metrics, metricValues):
                                    if (metric in metricFilters and not metricFilters[metric](metricValue)) or (s in settingsFilter and not settingsFilter[s](metric)):
                                        continue
                                    problemStats[metric][label].append(metricValue)
    return stats

def saveBoxPlots(stats, problem, metric, fileNamePrefix = ""):
    """
    Builds box plots for stats in format returned from groupMetrics and specified problem and metric
    Exach experiment has separate file with box plots. File contains 1 row per problem which contains one boxplot per setup.    
    :param stats in format { expId: {problemId: { metricId: {setupId: [value1, value2, ...]}}}}
    :param problem - specific problem to which we plot boxplots
    :param metric - metric to draw, should be inside stats
    :param fileNamePrefix - prefix of file were to store result. 
    :return None, Saves boxplots into file fileNamePrefix-problem-experimentId-metric
    """
    for e in stats: 
        plotFile = "-".join(part for part in [fileNamePrefix, problem, e, metric] if part != "")
        values = stats[e][problem][metric]
        plt.clf()
        # plt.subplots_adjust(hspace=1)

        fig, ax = plt.subplots()
        # pprint(values.values())
        #ax.violinplot(values.values()) #values, vert=True, patch_artist=True, labels=labels) 
        # ax.boxplot(values.values(), notch = True, showmeans=True, showfliers=False) #values, vert=True, patch_artist=True, labels=labels) 
        ax.boxplot(values.values(), showfliers=False) #values, vert=True, patch_artist=True, labels=labels) 
        ax.set_xticklabels(values.keys(),rotation=15, ha="center")
        # plt.ylabel(ylabel)
        # plt.title('Multiple Box Plot : Vertical Version')
        fig.tight_layout()
        plt.savefig(plotFile)        

def saveBoxPlotsForMetrics(stats, problem, metrics, fileNamePrefix = ""):
    """
    Builds box plots for stats in format returned from groupMetrics and specified problem and metric matrix
    Exach experiment has separate file with box plots. File contains 1 row per problem which contains one boxplot per setup.    
    :param stats in format { expId: {problemId: { metricId: {setupId: [value1, value2, ...]}}}}
    :param problem - specific problem to which we plot boxplots
    :param metrics - [[borFitness, borFitnessTestSet]]
    :param fileNamePrefix - prefix of file were to store result. 
    :return None, Saves boxplots into file fileNamePrefix-experimentId
    """
    for e in stats: 
        plotFile = "-".join(part for part in [fileNamePrefix, problem, e] if part != "")        
        plt.clf()

        fig, axs = plt.subplots(len(metrics), len(metrics[0]))
        plt.subplots_adjust(hspace=0.01, wspace=0.01, bottom=0.01, top=0.99)
        # pprint(values.values())
        #ax.violinplot(values.values()) #values, vert=True, patch_artist=True, labels=labels) 
        # ax.boxplot(values.values(), notch = True, showmeans=True, showfliers=False) #values, vert=True, patch_artist=True, labels=labels) 
        for row, rowMetrics in zip(axs, metrics):
            for ax, (metric, metricName, addXLabels) in zip(row, rowMetrics):   
                if metric is None: 
                    fig.delaxes(ax)
                    continue     
                values = stats[e][problem][metric]        
                ax.boxplot(values.values(), showfliers=False, showmeans=False, patch_artist=True) #values, vert=True, patch_artist=True, labels=labels) 
                ax.set_title(metricName, pad=-10, loc="left", size=10)
                if addXLabels:
                    ax.set_xticklabels(values.keys() ) #,rotation=90, ha="center")
                else:
                    ax.set_xticklabels([])
        # plt.ylabel(ylabel)
        # plt.title('Multiple Box Plot : Vertical Version')
        fig.set_tight_layout(True)
        fig.set_figheight(16)
        plt.savefig(plotFile)          

def buildAllProblemStats():
    expResultFolder = [ "data", "2022-04-15" ]
    experiments = ["7379006"]
    problems = [ "R1", "R2", "Kj3", "Kj4", "Kj11", "Ng9", "Ng12", "Pg1", "Vl1"]
    settings = {"RTsTx": [""], "RTsTmx": ["1", "10"], "RTsTxN": ["str1", "str2", "str3", "str4"] }    
    metrics = ["borSize", "borDepth", "meanSize", "meanDepth", "maxGen", "found", "ms", "borFitness", "borFitnessTestSet", "fitnessStdev", "aucRoc", "nroRate", "nroRevs"]
    stats = groupMetrics(expResultFolder, experiments, problems, settings, metrics, \
                skip = 1, \
                settingsFilter={"RTsTx": lambda m: not m.startswith("nro"), "RTsTmx": lambda m: not m.startswith("nro")}, \
                metricFilters={"borFitnessTestSet": lambda v:v < 1e6})
    return (stats, metrics, problems)

def buildAllBoxPlots(stats, metrics, problems):
    # for metric in metrics:
    for p in problems:
        saveBoxPlotsForMetrics(stats, p, [\
            [(metrics[7], "bor fitness", False), (metrics[8], "bor fitness test set", False)], \
            [(metrics[0], "bor size", False), (metrics[2], "mean size", False)], \
            [(metrics[1], "bor depth", False), (metrics[3], "mean depth", False)], \
            [(metrics[9], "std dev fitness", False), (metrics[10], "AUC ROC", False)], \
            [(metrics[4], "max gen", True), (metrics[5], "1 - found, 0 - not found", True)], \
            [(metrics[6], "time, ms", True), (None, "", False)], \
            [(metrics[11], "NRO rate", True), (metrics[12], "NRO revs", True)] \
            ], fileNamePrefix="t")

from igraph import Graph, plot as graphPlot

def buildAllStats(stats, metrics, dominationLevels = [0.05, 0.1], filePrefix="stat"): 
    dominations = {}
    for e in stats:
        lines = []
        d = {}
        dominations[e] = d
        # plt.subplots_adjust(hspace=0.01, wsp/ace=0.01, bottom=0.01, top=0.99)
        for p in stats[e]:                
            lines.append(p)
            plt.clf()
            fig, axs = plt.subplots(len(metrics), len(dominationLevels))
            for row in axs:
                for ax in row:
                    ax.set_axis_off()
            axI = 0 
            for m in metrics:
                md = {dl:{} for dl in dominationLevels}
                cmp = metrics[m]
                d[m] = md
                lines.append("\t" + m)
                setups = stats[e][p][m]
                setupNames = list(setups.keys())
                values = [setups[k] for k in setupNames]
                minLen = len(min(values, key=lambda x:len(x)))
                values = [v if len(v) == minLen else v[:minLen] for v in values]
                res = allStats(values)
                means = {}
                for m_std, name in zip(res["m_std"], setupNames):
                    lines.append("\t{:7s} {:7.2f} ± {:7.2f}".format(name, round(m_std["mean"], 2), round(m_std["std1"], 2)))
                    means[name] = m_std["mean"]
                pValue = res["friedman"].pvalue
                lines.append("\tFriedman: {:.5f} (stat: {:7.2f})".format(pValue, res["friedman"].statistic))
                lines.append("\tNemenyi: ")
                for (i, line) in res["nemenyi"].iterrows():
                    lineStr = "".join("{:7.2f}".format(el) for el in line)
                    lines.append("\t\t" + lineStr)
                    curName = setupNames[i]
                    for nPValue, otherName in zip(line, setupNames):
                        for dl in md:
                            if pValue <= dl and nPValue <= dl and cmp(means[curName], means[otherName]):
                                if curName not in md[dl]: 
                                    md[dl][curName] = set()
                                md[dl][curName].add(otherName)
                axJ=0
                for dl in md:
                    if len(md[dl]) == 0:
                        # fig.delaxes(axs[i][j])
                        axJ = axJ + 1
                        continue
                    lines.append("\tDomination: " + str(dl))
                    for name in md[dl]:
                        lines.append("\t\t" + name + " is better than " + ", ".join(md[dl][name]))
                    dgr = Graph.TupleList([(v, s) for s, vs in md[dl].items() for v in vs], directed=True)
                    # print(dgr)
                    # dgr.vs["label"] = dgr.vs["name"]
                    # g.vs["color"] = [color_dict[gender] for gender in g.vs["gender"]]
                    layout = dgr.layout("kamada_kawai")
                    graphPlot(dgr, target=axs[axI][axJ], layout = layout, vertex_label = dgr.vs["name"], edge_color="#8989a3", autocurve = True, edge_width = 0.5, edge_arrow_width=3, edge_arrow_size=3, vertex_size = 5, vertex_frame_width=0.0, vertex_color = '#AAAAFF')
                    axs[axI][axJ].set_title(m + ", " + str(dl), pad=10, loc="left", size=10)
                    axJ = axJ + 1
                lines.append("")
                axI = axI + 1
            lines.append("")
            lines.append("")
            fig.set_tight_layout(True)
            fig.set_figheight(16)
            fileName = "-".join(part for part in ["d", p, e] if part != "") + ".png"
            plt.savefig(fileName)
            # res["problem"] = p
            # res["experiment"] = e
            # res["names"] = list(setupNames)
            # pprint(res)
        fileName = "-".join(part for part in [filePrefix, e] if part != "") + ".txt"
        with open(fileName, "w") as f:
            f.writelines(line + '\n' for line in lines)
    return dominations

def extractBogFitness(folder, prefix, expectedLen): 
    """
        extracts best-of-generation fitness into file out from job files 
        :param folder - folder with job files 
        :param prefix - prefix of file names in folder
        :returns list of all trials where one trial is list of generation best fitnesses
    """
    results = []
    for fileName in os.listdir(folder):        
        if fileName.startswith(prefix):
            with open(os.path.join(folder, fileName), 'r') as file: 
                txt = file.read()
            res = [ float(s) for s in pattern.findall(txt) ]
            res.pop() #discard fitness on testing set
            res.pop() #discard conclusion about bor
            if len(res) < expectedLen: 
                res = res + [0 for i in range(expectedLen - len(res))]            
            results.append(res)
    return results
    
def extractBogFitnessToCsv(folder, prefix, name, expectedLen): 
    runs = extractBogFitness(folder, prefix, expectedLen)
    with open(name, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(runs)

def extractExpBogFitnessToCsv(folder, eid, pid, setups, expectedLen): 
    for setup in setups: 
        fileName = f"{pid}-{setup}-{eid}"
        folderName = os.path.join(folder, fileName)
        extractBogFitnessToCsv(folderName, "job.", "bog-" + fileName + ".csv", expectedLen)
        
if __name__ == "__main__":    
    # extractExpBogFitnessToCsv("data/2022-04-15", "7379006", "Kj11", ["RTsTx", "RTsTxN-str4", "RTsTxN-str3", "RTsTxN-str2", "RTsTxN-str1", "RTsTmx-1", "RTsTmx-10"], 101)
    extractExpBogFitnessToCsv("data/2022-04-15", "7379006", "Kj3", ["RTsTx", "RTsTxN-str4", "RTsTxN-str3", "RTsTxN-str2", "RTsTxN-str1", "RTsTmx-1", "RTsTmx-10"], 101)

    
    # (s, metrics, problems) = buildAllProblemStats() 
    # ls = lambda x,y: x < y
    # gt = lambda x,y: x > y   
    # buildAllStats(s, {"borSize": ls, "borDepth": ls, "meanSize": ls, "meanDepth": ls, "ms": ls, "borFitness": ls, "borFitnessTestSet": ls, "fitnessStdev": gt, "aucRoc": gt })


    # buildAllBoxPlots(s, metrics, problems)
    #[metrics[11], metrics[12]
    # pprint(stats)

    # if len(sys.argv) > 1:
    #     n = int(sys.argv[1]) 
    #     # rng = numpy.arange(5)
    #     for p in params:
    #         c = cmd(p)
    #         runs = run([], c, n)
    #         # print(runs)
    #         mean = np.mean(runs, axis=0)
    #         std = np.std(runs, axis=0)
    #         save(p + ".csv", runs, mean, std, np.mean(mean))
    #         # plt.clf()
    #         # # ticks = [i for i in range(1,51) if i % 5 == 0]
    #         # # plt.tick_params(axis='x', labelbottom=False)            
    #         # plt.boxplot(np.transpose(runs).tolist(), sym='')
    #         # plt.xticks(ticks=[1,11,21,31,41,51], labels=[0,10,20,30,40,50])
    #         # plt.savefig(p + '.png', bbox_inches='tight')


# plt.plot([1,2,3], [2,3,4])
# plt.show()

