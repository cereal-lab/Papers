# Deployment of Neutral Rewrite Operator for ECJ. Arithmetic Domain. 

These are scripts to deploy NRO locally from [CEREAL/ecj](https://github.com/cereal-lab/ecj) repo (arith_domain tag) and to run experiments.

By default, ecj is installed into the same folder of deploy&#46;sh script. Java 8+ and python3 with [pip and venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) are required.

Deploy&#46;sh script does next:

1. Fetches and builds NRO implementation in ECJ framework from other CEREAL repository. Please, ignore warnings during compilation. Output is ecj jar file with NRO strategies and evolutionary process configurations.

2. Creates virtual environment for python post-processing script (analyze&#46;py). It then installs scipy/numpy and other required packages. 

Exp0&#46;sh is used on SLURM cluster (we used it on USF CIRCE) to start parallel jobs for different configurations.

Run&#46;sh can be used to start experiment localy. On run, for each configuration you will have separate folder created.

## Configuration of runs 

In exp0&#46;sh you can find how to execute one run of experiment for specified configuration. Here is an example: 
```bash
java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms
```

Here, `-from domain/regression/base.n2.params` is used to specify evolutionary pipeline with NRO inserted after classic Koza crossover. Flags `-p` are used to override defaults from that file: specify problem instance with `eval.problem.type`, number of free variables `eval.problem.vars`, rewrite startegy `koza.mutate.strategy.name`. Consider exp0&#46;sh for current possible configurations.


## Output of experiment

For each configuration separate folder will be created with output for each configuration run and aggregated result in `exp.stat` with each metric of process specified bellow. 

## Post processing scripts

Analyze&#46;py post processing script conducts statistical tests and builds box-plot charts and graphs of dodmination relation. 

It outputs:

1. `stat-0.txt` text file with analysis of each problem instance for bunch of metrics related to evolutionary process.
    - borSize - best of run individual size [category: model interpretability metric, bloat metric];
    - borDepth - best if run individual depth [category: model interpretability metric, bloat metric];
    - meanSize - last gen individuals mean size [category: bloat metric]; 
    - meanDepth - last gen individuals mean depth [category: bloat metric]; 
    - generationId - id of generation when process converges (for continuous SymReg mostly useless) [category: convergence metric]
    - solutionFound - 1 if solution was found, 0 - if not. [category: convergence metric]
    - elapsedTime - ms of run [category: complexity metric]
    - borFitness - best-of-run fitness on training set, [category: convergence metric]
    - testingSetFitness - bor fitness on testing set, [category: convergence metric]
    - stdDevFitness - phenotypic diversity metric - stddev of fitness of inds between quantiles 1 and 3 at last gen, [category: diversity metric]
    - testingSetROC - ability to generalize metric as Paul suggested. best-of-run model is used for roc calc on testing set. [category: generalization metric]    
    TODO: R2, random seeds etc
2. `t-<instance>-0.png` - bar charts of specified metrics for specified configurations at last generation
3. `d-<instance>-0.png` - domination graphs for each metrics 
  
Important: if you conduct experiment with customized set of instance problems, please modify buildAllProblemStats in the analyze.py and specify necessary configuration.
```python
    expResultFolder = [ "" ]
    experiments = ["0"]
    problems = [ "R1", "R2", "Kj3", "Kj4", "Kj11", "Ng9", "Ng12", "Pg1", "Vl1"]
    settings = {"RTsTx": [""], "RTsTmx": ["1", "10"], "RTsTxN": ["str1", "str2", "str3", "str4"] }    
    metrics = ["borSize", "borDepth", "meanSize", "meanDepth", "maxGen", "found", "ms", "borFitness", "borFitnessTestSet", "fitnessStdev", "aucRoc", "nroRate", "nroRevs"]
```