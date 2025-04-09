
from scipy.cluster.hierarchy import single, complete, average, ward, dendrogram, centroid
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

import Parameters as param


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
    
#     fig = plt.figure(figsize=(16, 8))
#     dn = dendrogram(Z)
#     plt.title(f"Dendrogram for {method}-linkage with correlation distance")
#     plt.show()
    
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

### Regression with Accuracy
def regression_sklearn(df, print_report):

    selected_col_X = df[param.SELECTED_VARIABLES_X]
    X = selected_col_X.values

    selected_col_y = df['Clusters']
    y = selected_col_y.values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a logistic regression model for multiclass classification
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=param.ITERATION)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)


    if print_report == 1:

        # Evaluate the accuracy of the model
        accuracy = accuracy_score(y_test, predictions)
        print(f'Accuracy: {accuracy:.2f}')

        # Print classification report
        print('Classification Report:\n', classification_report(y_test, predictions))

    return model, accuracy
    

def fitness(df_x, s_score = 1):

    df_clustering = df_x.copy()
    seq_list = df_clustering['modified_sequence'].tolist()

    distance_matrix = dis_matrix_calc(seq_list)

    linkage_matrix = hierarchical_clustering(distance_matrix, param.H_LINKAGE)
    # select maximum number of clusters
    cluster_labels = fcluster(linkage_matrix, param.N_CLUSTERS, criterion='maxclust')
    cluster_labels = cluster_labels.tolist()

    df_clustering['Clusters'] = cluster_labels

    # print(cluster_labels)
    sil_score = -1
    acc = -1

    if s_score == 1:
        
        sil_score = silhouette_score(distance_matrix, cluster_labels)
        # print("sil_score: ", sil_score)

        _, acc = regression_sklearn(df_clustering, 0) # 0=do not want to print the full result

    return df_clustering, sil_score, acc