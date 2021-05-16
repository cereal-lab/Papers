# Deployment of Neutral Rewrite Operator for ECJ 

These are scripts to deploy NRO locally from [CEREAL/ecj](https://github.com/cereal-lab/ecj) repo and to start experiments.
By default, ecj is installed in folder of deploy&#46;sh script. Java 8+ and python3 with [pip and venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) are required.

Deploy&#46;sh script does next:

1. Fetches and builds NRO implementation in ECJ framework from our other CEREAL repository. Please, ignore warnings during compilation. 

2. Creates virtual environment for python automation script (analyze&#46;py) for experiments with NRO. It then installs scipy/numpy and other required packages. 

3. Runs analyze&#46;py which starts experiments with NRO. For better understanding please check deploy&#46;sh and nro/ecj/analyze&#46;py.

##Configuration of experiments 

Deploy&#46;sh runs analyze&#46;py with parameter 2. Change it to value of number of runs of evolutionary process pipeline per experiment. Analyze&#46;py contains next variable params = [ "mul.n", "par.n", "maj.n", "cmp.n" ]. It defines what configurations to run. Check corresponding files in nro/ecj/src/main/resources/ec/app/rewrites. If you want to add configuration and change params variable, do not forget to rebuild ecj with nro project (make nro). 

##Output and additional analysis 

After runs, analyze&#46;py extracts information from ECJ target/classes/out&#46;stat to csv files. These files contains best fitness for each generation and each configuration in params. You can use other functions from analyze&#46;py and exp&#46;py to visualize converganse process and calculate Friedman and Nemenyi p-values to conclude configuration domination. 
