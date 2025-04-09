### Refer codes from Mostapha Kalami Heris, NSGA-II in Python (URL: https://yarpiz.com), Yarpiz, 2023.

# %% ### Importing Package
### Importing Package
### General 
import pandas as pd
import time
import Parameters as param
from utils.nsga2 import NSGA2
from utils.config_utils import df_complete_creation, df_summary_creation

### Show more rows/columns
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# %% ### Initialization
### Initialization

# Problem Definition
problem = {
    'file_input': param.INPUT_FILE,
    'obj1': param.obj1,
    'obj2': param.obj2,
    'n_clusters': param.N_CLUSTERS,
    'n_bits': param.N_BITS,
    'bit_mask': param.LABEL_MASK,
    'label_GA': param.LABELS_DENOISING,
    'label_max_num': param.LABEL_MAX
}

# Initialize Algorithm
alg = NSGA2(
    generation = param.N_GEN,
    pop_size = param.N_POP,
    p_crossover = param.R_CROSS,
    alpha = param.ALPHA,
    p_mutation = param.R_MUT,
    n_lr_iter = param.ITERATION
)

n_trial = param.N_TRIALS
pop_cache = {}

# Create df
col_complete_result = ["Trial" ,"Gen","Search_Space", problem['obj1'], problem['obj2'], "Pareto_Front" ]
df_complete_result = pd.DataFrame()

col_df_summary = ['Gen', 'Search_Space', 'AVG_{}'.format(problem['obj1']), 'AVG_{}'.format(problem['obj2'])]

# %% ### main codes
### main codes
if __name__ == '__main__':
    # Solve the Problem
    for trial in range(1, n_trial+1):
        print()
        start_time = time.time() # Record the start time
        print(f"Trial {trial}/{n_trial} ---")

        results, gen_information = alg.run(problem)
        print()
        print("---------------------FINAL Result---------------------")
        for key, value in results.items():
            print(f"Gene: {key}, Fitness: {value[0][0]:.4f} | {value[0][1]:.2f}, rank: {value[1]}")

        print("------------------------------------------------------")

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Process completed in {elapsed_time:.2f} seconds.")

        df_gen = df_complete_creation(col_complete_result, gen_information, trial)
        df_complete_result = pd.concat([df_complete_result, df_gen], ignore_index=True)

    df_complete_result.to_csv('{}/MOEA_complete_output.csv'.format(param.OUTPUT_DIR), index=False) 

    df_summary = df_summary_creation(col_df_summary, df_complete_result, problem)
    df_summary.to_csv('{}/MOEA_summary_output.csv'.format(param.OUTPUT_DIR), index=False) 