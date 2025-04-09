
from scipy.cluster.hierarchy import single, complete, average, ward, dendrogram, centroid
import pandas as pd
import numpy as np


def hierarchical_clustering(dist_mat, method='complete'):
    if method == 'complete':
        Z = complete(dist_mat)
    if method == 'single':
        Z = single(dist_mat)
    if method == 'average':
        Z = average(dist_mat)
    if method == 'ward':
        Z = ward(dist_mat)
    if method == 'centroid':
        Z = centroid(dist_mat)
    
    return Z

def levenshtein_ratio_and_distance(s, t, ratio_calc=True):
    """
    Optimized Levenshtein distance/ratio calculation using two rows to reduce memory usage.
    """
    rows, cols = len(s) + 1, len(t) + 1

    # Initialize two rows
    previous_row = np.arange(cols)
    current_row = np.zeros(cols, dtype=int)

    for row in range(1, rows):
        current_row[0] = row
        for col in range(1, cols):
            cost = 0 if s[row - 1] == t[col - 1] else (2 if ratio_calc else 1)
            current_row[col] = min(
                previous_row[col] + 1,          # Deletion
                current_row[col - 1] + 1,       # Insertion
                previous_row[col - 1] + cost    # Substitution
            )
        # Swap rows
        previous_row, current_row = current_row, previous_row

    # The final edit distance is in the last cell of the previous row
    edit_distance = previous_row[-1]

    if ratio_calc:
        return ((len(s) + len(t)) - edit_distance) / (len(s) + len(t))
    else:
        return edit_distance
    
def dis_matrix_calc(seq):
    edit_distance = []

    flag = 0

    for i in range(0, len(seq)):
        edit_distance = []
        for j in range(0, len(seq)):

            edit_distance.append(levenshtein_ratio_and_distance(seq[i], seq[j]))

        if flag == 0:

            # distance_matrix = pd.DataFrame([edit_distance[0:len(seq)]])
            distance_matrix = list([edit_distance[0:len(seq)]])
            flag = 1


        else:
            # distance_matrix = distance_matrix.concat([edit_distance[0:len(seq)]])
            # distance_matrix.loc[len(distance_matrix)] = [edit_distance[0:len(seq)]]
            distance_matrix.append(edit_distance[0:len(seq)])

    # distance_matrix = distance_matrix.reset_index(drop=True)
    distance_matrix = pd.DataFrame(distance_matrix)

    
    return distance_matrix