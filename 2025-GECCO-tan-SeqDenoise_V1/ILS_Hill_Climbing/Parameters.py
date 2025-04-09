
# %%
import pandas as pd

### --- FILE PATHS --- ###
OUTPUT_DIR = "output"

# # Parsons Puzzle Dataset
# INPUT_FILE = '../Datasets_CSV/df_parsons_puzzles.csv' # File path for the dataset
# SELECTED_VARIABLES_X = ['steps', 'time_spent']  # Predictor variables for regression 
# LABELS_DENOISING = 'RT'  # Labels of the sequence that need to be denoised: "R", "T"

# Advertising Dataset
INPUT_FILE = '../Datasets_CSV/df_advertising.csv' # File path for the dataset
SELECTED_VARIABLES_X = ['conversion', 'conversion_value'] # Predictor variables for regression
LABELS_DENOISING = 'IDS'  # Labels of the sequence that need to be denoised: "I", "D", "S", "F", "V"

### --- DATA CONFIGURATION --- ###
df = pd.read_csv(INPUT_FILE)
MEASURE = 'SIL'  # Options: SIL/ACC

### --- CLUSTERING CONFIGURATION --- ###
N_CLUSTERS = 3  # Number of clusters in the hierarchical algorithm
H_LINKAGE = 'complete'  # Linkage method: complete/single/average/ward/centroid
ITERATION = 500 # Set the maximum number of iterations for optimization.

### --- ILS CONFIGURATION --- ###
N_TRIALS = 2  # Number of trials
ILS = 1  # 0 = Random Restart, 1 = ILS
NUMBER_NEIGHBOR = 4  # Number of neighbors to be searched
NUMBER_RESTART = 5 # Number of restarts

### --- CHROMOSOME CONFIGURATION --- ###
# Determine the chromosome size based on label occurrences in sequences.
# For each label in LABELS_DENOISING, find the maximum times it appears 
# in any sequence within the "modified_sequence" column. Store these 
# values in LABEL_MASK, then sum them to get N_BITS, which represents 
# the total number of bits in the chromosome.
LABEL_MASK = []  # Mask for the chromosome based on label occurrences
for label in LABELS_DENOISING:
    max_count = df["modified_sequence"].apply(lambda x: x.count(label)).max()
    LABEL_MASK.append(max_count)

N_BITS = sum(LABEL_MASK)  # Number of bits in the chromosome

### --- MUTATION & CROSSOVER RATES --- ###
R_MUT = 2.0 / float(N_BITS)  # Mutation rate









