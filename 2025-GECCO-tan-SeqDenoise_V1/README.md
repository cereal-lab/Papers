## **Adaptive Denoising of Sequential Data with Multi-Objective Genetic Algorithms**

### **Overview**
This repository contains the implementation of our proposed **adaptive denoising method** for sequential data, integrating a **multi-objective genetic algorithm (GA)** with **semi-supervised learning**. This approach selectively filters out noise while preserving critical information, avoiding over-sanitization that could degrade data quality. The method dynamically adapts fitness functions using partial ground truth to enhance data mining outcomes.

This code accompanies the paper:

📄 **"Adaptive Denoising of Sequential Data with Multi-Objective Genetic Algorithms"**  
[Insert publication link when available]

### **Datasets**
The repository includes two datasets:

1. **df_parsons_puzzles.csv**  
   - Captures students' interactions while solving Parsons Puzzles.
   - Provided by **Dr. Amruth N. Kumar** ([ACM publication](https://dl.acm.org/doi/10.1145/3159450.3159576)).
   - Pre-processed and ready for use.

2. **df_advertising.csv**  
   - Captures consumer behavior in digital marketing.
   - Based on the dataset from [Kaggle](https://www.kaggle.com/code/hughhuyton/multitouch-attribution-modelling/notebook).
   - Cleaned and formatted for this project.

🔹 **Custom Data Usage:**  
Users can use their own dataset, but it must contain:  
   - A **"modified_sequence"** column indicating the sequential data.  
   - At least **two predictor variables** that can be used in regression.

### **Algorithms Implemented**
This repository includes three different algorithms to denoise the dataset:

1. **Hill Climbing with Iterated Local Search (ILS)**  
2. **Genetic Algorithm (GA)**  
3. **NSGA-II (Multi-objective Genetic Algorithm)**  

These algorithms optimize two key measures:
- **Silhouette Score** (Cluster quality assessment)
- **Regression Accuracy** (Prediction performance)

ILS and Genetic Algorithm optimize only **one** measure at a time, while NSGA-II can optimize **both simultaneously**.

### **Parameter Configuration**
Each algorithm requires users to set parameters in `Parameters.py`. Some key parameters that need to be manually configured include:

#### **Common Parameters (All Algorithms)**
- `INPUT_FILE`: Dataset to use
- `SELECTED_VARIABLES_X`: Predictor variables for regression
- `LABELS_DENOISING`: Labels of the sequence that need to be denoised
- `N_CLUSTERS`: Number of clusters in the hierarchical algorithm
- `ITERATION`: Maximum number of iterations for optimization in LogisticRegression
- `N_TRIALS`: Number of times the experiment is run (typically 30 for statistical robustness)

#### **Algorithm-Specific Parameters**

**1. Hill Climbing with ILS**
- `MEASURE`: Optimization target (`SIL` for Silhouette Score, `ACC` for Accuracy)
- `H_LINKAGE`: Linkage method (`complete`, `single`, `average`, `ward`, `centroid`)
- `ILS`: Iterated Local Search mode (`0 = Random Restart`, `1 = ILS`)
- `NUMBER_NEIGHBOR`: Number of neighbors to be searched
- `NUMBER_RESTART`: Number of restarts

**What is Iterated Local Search (ILS)?**
ILS is a **metaheuristic optimization technique** that enhances local search by incorporating perturbation and re-optimization. It helps escape local optima by slightly modifying solutions and refining them iteratively.

**2. Genetic Algorithm**
- `H_LINKAGE`: Linkage method (`complete`, `single`, `average`, `ward`, `centroid`)
- `MEASURE`: Optimization target (`SIL` for Silhouette Score, `ACC` for Accuracy)
- `N_GEN`: Number of generations to run
- `N_POP`: Initial population size

**3. NSGA-II (Multi-objective Genetic Algorithm)**
- `N_GEN`: Number of generations to run
- `N_POP`: Initial population size

### **Running the Code**
After setting the parameters in `Parameters.py`, execute the corresponding algorithm by running:

```bash
python main.py  # Run inside the corresponding algorithm folder
```

Example:
```bash
cd Genetic_Algorithm
python main.py
```

### **Outputs**
Each algorithm generates two types of outputs in the `output/` folder:
1. **Complete Output** – Logs all generations/restarts across multiple trials.
2. **Summary Output** – Displays the average values per generation. For ILS, this summary contains the best chromosome and its performance measure for each restart.

### **Installation**
To set up the environment and install dependencies, follow these steps:

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### **Dependencies**
This project requires the following Python libraries:

```txt
numpy==1.26.3
pandas==2.1.4
scikit-learn==1.3.2
scipy==1.11.4
matplotlib==3.8.2
seaborn==0.13.1
joblib==1.3.2
statsmodels==0.14.1
sklearn-extra==0.3.0
tqdm==4.67.1
```

### **Contact**
If you have any questions or concerns regarding the code, please email **kokcheng@usf.edu**.

---


