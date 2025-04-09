# %% ### Importing packages
### Importing packages

import pandas as pd
import time
from numpy.random import randint
import multiprocessing as mp
from functools import partial


import Parameters as param

from utils.config_utils import print_parameters
from utils.config_utils import calc_score
from utils.config_utils import convert_to_binary
from utils.config_utils import convert_to_decimal
from utils.config_utils import mutation
from utils.config_utils import duration_checking



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# %% ### Functions
### Functions

def getNeighbours(sol):
    
    neighbours = []
    neighbours.append(sol)
    
    while len(neighbours) < param.NUMBER_NEIGHBOR:
        neigbhour = sol.copy()
        mutation(neigbhour, param.R_MUT)
    
        if neigbhour not in neighbours:
            neighbours.append(neigbhour)
        
    return neighbours

def getBestNeighbour(sols, df):
    
    neighbour_dict = {}
    pool = mp.Pool(16)
    combined_args = partial(calc_score, df, pop_cache)
    results = pool.map(func=combined_args, iterable=sols)
    pool.close()
    pool.join()
        
    for i in range(len(results)):
        pop_cache[results[i][0]] = list(results[i][1:])   
        neighbour_dict[results[i][0]] = [results[i][1], results[i][2]]

    bestN = max(neighbour_dict, key=lambda k: neighbour_dict[k][0])
    bestNFit = neighbour_dict[bestN]

    bestN = convert_to_binary(bestN, param.N_BITS)
    
    return bestN, bestNFit

def hillClimbing(sol, df, m):
    
    running_num = 0

    neighbourSol = getNeighbours(sol)    
    bestNeighbour, bestNeighbourFit = getBestNeighbour(neighbourSol, df)
    
    fit = [pop_cache.get(convert_to_decimal(sol))[0], pop_cache.get(convert_to_decimal(sol))[1]]
    
    while bestNeighbourFit[m] > fit[m]:
        sol = bestNeighbour
        fit = bestNeighbourFit
        neighbourSol = getNeighbours(sol)
        bestNeighbour, bestNeighbourFit = getBestNeighbour(neighbourSol, df)
        running_num += 1

    return sol, fit, running_num

# %% ### Main()
### Main()
if __name__ == "__main__":
    print_parameters()

    df = pd.read_csv(param.INPUT_FILE)

    df_complete = pd.DataFrame(columns = ['Restart','Best_Sol', 'Best_Fitness_BTW_Neighbours', 'Neighbour_searched', "Space_searched"])
    df_summary = pd.DataFrame(columns = ['Trials', 'Best_Sol' , 'Best_Fitness_BTW_Restarts', 'Total_space_searched', 'Avg_SIL', 'Avg_ACC'])

    ts_before = time.time()
    flag_random = 0

    for trial in range(param.N_TRIALS):
        pop_cache = {}
        n_restart = 1
        last_cache = 0
        bestFitness = [0,0]
        avgFitness = 0
        avgFitness_2 = 0

        if param.MEASURE == 'SIL':
            avgFitness_measure = "SIL"
            measure = 0
        else:
            avgFitness_measure = "ACC"
            measure = 1


        print()
        print("Trial: ", trial+1)

        while n_restart <= param.NUMBER_RESTART:
            print()
            print("Restart: ", n_restart)

            if flag_random == 0:
                ### Random Start
                newSolution = randint(0, 2, param.N_BITS).tolist()

                if param.ILS == 1:
                    flag_random = 1
            
            else:
                ### ILS
                mutation(currentSolution, param.R_MUT)
                newSolution = currentSolution

            currentSolution, currentFitness, running_number = hillClimbing(newSolution, df, measure)
            space_searched = len(pop_cache) - last_cache
            avgFitness += currentFitness[0]
            avgFitness_2 += currentFitness[1]

            if currentFitness[measure] > bestFitness[measure]:
                bestSolution = currentSolution
                bestFitness = currentFitness
            
            print("Best {}:".format(avgFitness_measure), currentFitness[measure], "| Neighbours check:", running_number, 
                  "| Space Searched:", space_searched)
            
            new_row = [n_restart, str(currentSolution), currentFitness, running_number, space_searched]
            df_complete.loc[len(df_complete)] = new_row

            last_cache = len(pop_cache)
            n_restart += 1
        
        avgFitness = avgFitness / param.NUMBER_RESTART
        avgFitness_2 = avgFitness_2 / param.NUMBER_RESTART
        new_row = [trial, str(bestSolution), bestFitness, len(pop_cache), avgFitness, avgFitness_2]
        df_summary.loc[len(df_summary)] = new_row

        print("Trial:", trial, "| Total Searched:", len(pop_cache), "| Best Solution:", convert_to_decimal(bestSolution),
                  "| Best Fitness:", bestFitness, "| Avg SIL:", avgFitness, "| Avg ACC:", avgFitness_2)
        
    print("Time usage: ", duration_checking(ts_before)) 
    df_complete.to_csv('{}/ILS_complete_output.csv'.format(param.OUTPUT_DIR), index=False)  
    df_summary.to_csv('{}/ILS_summary_output.csv'.format(param.OUTPUT_DIR), index=False) 


