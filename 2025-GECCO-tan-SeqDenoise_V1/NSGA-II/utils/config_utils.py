import pandas as pd
from collections import Counter
import time

### Print parameters
def print_parameters(algo_param, problem_param):
    print("------------Parameters------------")
    print("Cluster: ", problem_param['n_clusters'])
    print(f"Fitness_to_optimize: {problem_param['obj1']} | {problem_param['obj2']}")
    print("generation: ", algo_param.generation)
    print("population: ", algo_param.pop_size)
    print("total_bits: ", problem_param['n_bits'])
    print("bits_mask: ", problem_param['bit_mask'])
    print("cleaning_label: ", problem_param['label_GA'])
    print("----------------------------------")

### Calculate Average Score from df
def cal_avg_score(df_x, x, pos):

    seq = list(df_x.loc[df_x['Gen'] == pos, x])
    avg_score = sum(seq)/len(seq)

    return avg_score

def df_complete_creation(col_complete_result, gen_info, trial):
        
        ## Record dataframe for complete result
        df_gen = pd.DataFrame(gen_info)
        # Transpose the DataFrame
        df_gen = df_gen.transpose()
        # Reset index to make keys a column
        df_gen.reset_index(inplace=True)
        # Rename the columns
        df_gen.columns = col_complete_result[1:]
        # Create the trial column
        trial_list = [trial] * len(gen_info)
        df_gen.insert(0, "Trial", trial_list)
        ##

        df_gen["Search_Space"] = df_gen["Search_Space"].astype(int)

        return df_gen


def df_summary_creation(col_df_summary, df_complete_result, problem):
    df_summary = pd.DataFrame(columns = col_df_summary)

    max_gen = df_complete_result['Gen'].max()

    for i in range(max_gen+1):
        df_summary.loc[i, 'Gen'] = i 
        df_summary.loc[i, 'Search_Space'] = cal_avg_score(df_complete_result, 'Search_Space', i)
        df_summary['Search_Space'] = df_summary['Search_Space'].astype(int)
        df_summary.loc[i, 'AVG_{}'.format(problem["obj1"])] = cal_avg_score(df_complete_result, problem["obj1"], i)
        df_summary.loc[i, 'AVG_{}'.format(problem["obj2"])] = cal_avg_score(df_complete_result, problem["obj2"], i)

    return df_summary


### Convert a list of binary bits to a decimal number
def convert_to_decimal(binary_list):
    res = int("".join(str(x) for x in binary_list), 2)
    
    return int(res)

### Convert a decimal number a list of binary bits
def convert_to_binary(decimal_num, bits):
    res = format(decimal_num, "0{}b".format(bits))
    res = [int(x) for x in res]
    
    return res

# ### Loading cache from the json
# def load_cache(problem):
#     try:
#         with open('Caches/Cache_{}_{}/{}_{}_{}_cache.json'.format(problem['dataset'], problem['n_clusters'], problem['n_bits'], problem['bit_mask'], problem['label_GA']), 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}

# def save_cache(cache, problem):
#     # Construct the folder and file paths
#     folder = 'Caches/Cache_{}_{}'.format(problem['dataset'], problem['n_clusters'])
#     file_path = os.path.join(folder, '{}_{}_{}_cache.json'.format(problem['n_bits'], problem['bit_mask'], problem['label_GA']))
    
#     # Check if the folder exists; if not, create it
#     os.makedirs(folder, exist_ok=True)
    
#     # Create or overwrite the file
#     with open(file_path, 'w') as file:
#         json.dump(cache, file)

### Check processing duration
def duration_checking(begin_time):
    after_time = time.time()
    duration = after_time - begin_time

    return round(duration, 2)


### keep labels based on the conditions
def keep_label(df_x, chars, num):

    for i in range(len(chars)):
        df_x['modified_sequence'] = df_x['modified_sequence'].apply(lambda x: processedString_2(x, chars[i], num[i]))
    
    return df_x

### keep the character according to the list
### variable 'keep' is the list with binary, e.g. = [0,1,0,1]
def processedString_2(str2, removedChar, keep):
    
    count = 0
    seq = ""
    for j in str2:        
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

def df_renumbered_occ(df):
    # Rename the cluster number based on occurances
    list_c = df['Clusters'].tolist()

    # Count occurrences of each element
    element_counts = Counter(list_c)

    # Sort elements based on their counts
    sorted_elements = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)

    # Assign new values based on rank
    new_values = {}
    for i, (element, _) in enumerate(sorted_elements):
        new_values[element] = i + 1

    # Map original list to new values
    modified_list = [new_values[element] for element in list_c]

    df['Clusters'] = modified_list

    return df