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
from utils.config_utils import convert_to_decimal
from utils.config_utils import duration_checking
from utils.config_utils import df_pop_constr
from utils.config_utils import df_com_constr
from utils.config_utils import output_constr

from utils.GA_operations import GA_operation



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# %% ### Initialization
### Initialization
pop_cache = {}
row_num = 0


# %% ### Main()
### Main()
if __name__ == "__main__":
    print_parameters()
    
    df_original = pd.read_csv(param.INPUT_FILE)

    df_complete = pd.DataFrame(columns = ['Trial', 'Generation', 'Best_sol', 'Gen_SearchSpace', 'Total_SearchSpace', 'SIL', 'ACC'])

    for trial in range(param.N_TRIALS):
        df = df_original.copy()

        pop = [randint(0, 2, param.N_BITS).tolist() for _ in range(param.N_POP)] # initial population

        ts_trial_before = time.time() # Record the begin time of a new trial starts
        pop_set = set() ### storing the genotype to count the search space

        print("Trial", trial+1, ":")
        for gen in range(param.N_GEN):
            row_num += 1
            ts_gen_before = time.time()
            df_pop = pd.DataFrame(columns = ['Pattern', 'SIL', 'ACC']) ### df_pop used to store every chromosomes's fitness

            ### counting the search space
            curGen_pop_cache = len(pop_set)
            for p in pop:
                pop_set.add(convert_to_decimal(p))

            ### calculating the fitness of each cleaning encode in parallel
            pool = mp.Pool(16)
            combined_args = partial(calc_score, df, pop_cache)
            result = pool.map(func=combined_args, iterable=pop)
            pool.close()
            pool.join()

            ### prepare population for GA
            pop_cache, pop, scores, best_decimal = df_pop_constr(result, pop_cache, df_pop)
                        
            ### obtain measurement index
            if param.MEASURE == 'SIL':
                m_index = 0
            elif param.MEASURE == 'ACC':
                m_index = 1
            else:
                m_index = -1

            ### print generation result
            print(f'Gen: {gen+1}, Best_measure ({param.MEASURE}): {round(pop_cache.get(best_decimal)[m_index], 4)}, S_space: {len(pop_set)-curGen_pop_cache}, Time: {duration_checking(ts_gen_before)}s')

            ### prepare the complete result
            df_complete = df_com_constr(df_complete, row_num, trial, gen, best_decimal, pop_cache, pop_set, curGen_pop_cache)

            ### Do not run any operation if this is the last gen
            if (gen+1) == param.N_GEN:
                break

            ### GA Operations----------------------------
            pop = GA_operation(pop, scores)

        print(f'Done--------------------------------------, Total Search: {len(pop_set)}, Time Taken: {duration_checking(ts_trial_before)}s')


    output_constr(df_complete)