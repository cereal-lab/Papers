import Parameters as param
from numpy.random import rand
import time

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
    print(f"ILS                   : {int(param.ILS)}")
    print(f"Number of Neighbors   : {int(param.NUMBER_NEIGHBOR)}")
    print(f"Number of Restarts    : {int(param.NUMBER_RESTART)}")
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

# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

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





