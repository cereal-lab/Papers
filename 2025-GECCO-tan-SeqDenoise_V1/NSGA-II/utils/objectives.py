from utils.config_utils import convert_to_decimal
from utils.config_utils import keep_label
from utils.config_utils import df_renumbered_occ
import utils.clustering as leven_clustering
import Parameters as param

from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score
from sklearn_extra.cluster import KMedoids ### pip3 install scikit-learn-extra

from collections import Counter

### objective2
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
# import statsmodels.api as sm

### Global Variables
selected_variables_X = param.SELECTED_VARIABLES_X

### Warning
import warnings



def fitness(df, problem, cache, clear_bits, export_df = 0, print_report = 0):
    n = convert_to_decimal(clear_bits)

    if export_df == 0 and n in cache:
        return n, cache.get(n)

    df_cleaned = df.copy()

    clear_bits_list = []
    start = 0
    for mask in problem['bit_mask']:
        end = start + mask
        clear_bits_list.append(clear_bits[start:end])
        start = end

    df_cleaned = keep_label(df_cleaned, problem['label_GA'], clear_bits_list)

    seq_list = df_cleaned['modified_sequence'].tolist()

    distance_matrix = leven_clustering.dis_matrix_calc(seq_list)

    linkage_matrix = leven_clustering.hierarchical_clustering(distance_matrix)
    cluster_labels = fcluster(linkage_matrix, problem['n_clusters'], criterion='maxclust') # select maximum number of clusters
    cluster_labels = cluster_labels.tolist()
    
    df_cleaned['Clusters'] = cluster_labels

    # Sort the cluster number based on the frequency
    df_cleaned = df_renumbered_occ(df_cleaned)

    sil_score = objective1(distance_matrix, cluster_labels)

    _, accuracy = objective2(df_cleaned, print_report)

    # r2 = objective3(df_cleaned)

    if export_df == 1:

        # Export df_cleaned to csv
        df_cleaned.to_csv('{}/{}_df.csv'.format(param.output, param.job_id), index=False) 

        # Print each cluster occurances
        clusters_count = df_cleaned.Clusters.value_counts().to_dict()
        for key, value in clusters_count.items():
            print(f'Cluster {key}: {value}')


    # return n, [sil_score, accuracy, r2]
    return n, [sil_score, accuracy]

### Sil_score    
def objective1(distance_matrix, cluster_labels):

    sil_score = silhouette_score(distance_matrix, cluster_labels)

    return sil_score

### Regression with Accuracy
def objective2(df, print_report=0):

    # df['conversion'] = df['conversion'].astype(int)
    # df['conversion_value'] = df['conversion_value'].astype(int)
    selected_col_X = df[selected_variables_X]
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

        # Print coefficients and intercepts
        coefficients = model.coef_
        intercepts = model.intercept_

        for class_idx in range(model.coef_.shape[0]):
            print(f'Cluster {class_idx+1}:')
            for feature_idx, coefficient in enumerate(coefficients[class_idx]):
                print(f'  {selected_variables_X[feature_idx]}: {coefficient:.4f}')
            print(f'  Intercept: {intercepts[class_idx]:.4f}')
            print('\n')

    return model, accuracy
