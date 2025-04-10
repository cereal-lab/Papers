# Coordinate System Extraction as the Search Driver in Test-Based Genetic Programming

This folder contains raw data and extracted with post-processing assets for the GECCO 25 article.
The implementation of the methods is stored in [this code separate repository](https://github.com/cereal-lab/cde-search/tree/v3.0).

**Folder structure**:

- **raw** contains jsonlist, one object per run of specific method ``sim_name`` on benchmark problem ``game_name``. The object contains many useful metrics, lists contains changes with generation. 

- **tables** are stored in github and latex formats. Metrics such as success rates, convergence speed and errors, cpu time. 

- **plots** contains pdf plots of metrics and measured characteristics of populations, such as semantic diversity and syntactic diversity. 


**Methods** 

1. Koza GP 
2. NSGA-2, NSGA-3
3. Derived objectives with clustering and matrix factorization 
4. Pareto front sampling strategies
4. Coordinate system extraction (once, twice, and based on discriminating tests)
