import Parameters as param
from numpy.random import rand
import time
import pandas as pd

from utils.clustering import fitness

def print_parameters():
    """Prints selected parameters in a readable format."""
    print("---- Selected Parameters ----")
    print(f"Input File            : {param.INPUT_FILE}")
    print(f"Labels for Denoising  : {param.LABELS_DENOISING}")
    print(f"Label Mask            : {param.LABEL_MASK}")
    print(f"Number of Bits        : {int(param.N_BITS)}")
    print(f"Measure               : {param.MEASURE}")
    print(f"Selected Variables (X): {', '.join(param.SELECTED_VARIABLES_X)}")
    print(f"Number of Clusters    : {int(param.N_CLUSTERS)}")
    print(f"Trials                : {int(param.N_TRIALS)}")
    print(f"Number of Generations : {int(param.N_GEN)}")
    print(f"Number of Populations : {int(param.N_POP)}")
    print(f"Crossover Rate        : {float(param.R_CROSS)}")    
    print(f"Mutation Rate         : {round(float(param.R_MUT), 2)}")
    print("-----------------------------")

# Convert a decimal number a list of binary bits
def convert_to_binary(decimal_num, bits):

    res = format(decimal_num, "0{}b".format(bits))
    res = [int(x) for x in res]
    
    return res

# Convert a list of binary bits to a decimal number
def convert_to_decimal(binary_list):
    res = int("".join(str(x) for x in binary_list), 2)
    
    return int(res)

### Check processing duration
def duration_checking(begin_time):
    after_time = time.time()
    duration = after_time - begin_time

    return round(duration, 2)

### keep the character according to the list
### variable 'keep' is the list with binary, e.g. = [0,1,0,1]
def processedString(str, removedChar, keep):
    
    count = 0
    seq = ""
    
    for j in str:        
        if count < len(keep):
            if j == removedChar and keep[count] == 1:
                count += 1
                seq += j
                continue
                

        if j == removedChar:
            count += 1
            continue
            
        seq += j

    return seq

# keep labels based on the conditions
def keep_label(df_x, chars, num):

    for i in range(len(chars)):
        df_x['modified_sequence'] = df_x['modified_sequence'].apply(lambda x: processedString(x, chars[i], num[i]))
    
    return df_x

### Calculate Average Score from df
def cal_avg_score(df_x, x, pos):

    seq = list(df_x.loc[df_x['Generation'] == pos, x])
    avg_score = sum(seq)/len(seq)

    return avg_score

### Build population df
def df_pop_constr(res, p_cache, df_x):

    for i in range(len(res)):
        p_cache[res[i][0]] = list(res[i][1:])

        df_x.loc[i, 'Pattern'] = convert_to_binary(res[i][0], param.N_BITS)
        df_x.loc[i, 'SIL'] = res[i][1]
        df_x.loc[i, 'ACC'] = res[i][2]

    df_x = df_x.sort_values(by=param.MEASURE, ascending=False)
    df_x = df_x.reset_index(drop=True)
    p = list(df_x["Pattern"].head(param.N_POP))
    s = list(df_x[param.MEASURE].head(param.N_POP))

    ### Get the best combination and score
    best = p[0]
    best_eval = s[0]

    for i in range(param.N_POP):
        if s[i] >= best_eval:
            best, best_eval = p[i], s[i]


    best_dec = convert_to_decimal(best)

    return p_cache, p, s, best_dec

### Build complete df for all results
def df_com_constr(df_x, r_num, t, g, best_dec, p_cache, p_set, curGen_p):

    # best_pattern = convert_to_binary(best_dec, param.n_bits)

    df_x.loc[r_num, 'Trial'] = t
    df_x.loc[r_num, 'Generation'] = g
    df_x.loc[r_num, 'Best_sol'] = str(convert_to_binary(best_dec, param.N_BITS))
    df_x.loc[r_num, 'Gen_SearchSpace'] = len(p_set)-curGen_p
    df_x.loc[r_num, 'Total_SearchSpace'] = len(p_set)
    df_x.loc[r_num, 'SIL'] = p_cache.get(best_dec)[0]
    df_x.loc[r_num, 'ACC'] = p_cache.get(best_dec)[1]

    return df_x

### Create and Export final df
def output_constr(DF_com):

    ### Storing complete result for all trials
    DF_com.to_csv('{}/GA_complete_output.csv'.format(param.OUTPUT_DIR), index=False)  

    ### Storing average result (focus on checking GA performance)
    df_GA = pd.DataFrame(columns = ['Generation', 'Population', 'Gen_SearchSpace', 'Total_SearchSpace', 'BEST_fitness', 'BEST_sol', 'AVG_fitness'])
    for i in range(param.N_GEN):
    
        max_fitness = max(list(DF_com.loc[DF_com['Generation'] == i, param.MEASURE]))
        max_sol = DF_com.loc[DF_com[param.MEASURE] == max_fitness, 'Best_sol'].values

        df_GA.loc[i, 'Population'] = param.N_POP
        df_GA.loc[i, 'Generation'] = i 
        df_GA.loc[i, 'BEST_fitness'] = max_fitness
        df_GA.loc[i, 'BEST_sol'] = max_sol[0]
        df_GA.loc[i, 'AVG_fitness'] = cal_avg_score(DF_com, param.MEASURE, i)
        df_GA.loc[i, 'Gen_SearchSpace'] = cal_avg_score(DF_com, 'Gen_SearchSpace', i)
        df_GA.loc[i, 'Total_SearchSpace'] = cal_avg_score(DF_com, 'Total_SearchSpace', i)

        for j in ['SIL', 'ACC']:
            if j != param.MEASURE:
                df_GA.loc[i, 'AVG_{}'.format(j)] = cal_avg_score(DF_com, '{}'.format(j), i)

    
    df_GA.to_csv('{}/GA_summary_output.csv'.format(param.OUTPUT_DIR), index=False)  


### Calculate Score
def calc_score(df_x, score_cache, clear_bits):

    n = convert_to_decimal(clear_bits)
    if n in score_cache:
        ss = score_cache.get(n)[0]
        acc = score_cache.get(n)[1]
        # pseudoR = score_cache.get(n)[2]
        # clusters_count = score_cache.get(n)[3]

    else:
        clear_bits_list = []
        start = 0
        for mask in param.LABEL_MASK:
            end = start + mask
            clear_bits_list.append(clear_bits[start:end])
            start = end

        df_cleaned = keep_label(df_x, param.LABELS_DENOISING, clear_bits_list) # clean the sequence based on the mask

        df_clustered, ss, acc = fitness(df_cleaned)

    return n, ss, acc





