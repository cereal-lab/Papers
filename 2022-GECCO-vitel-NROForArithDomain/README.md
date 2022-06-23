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

After runs, analyze&#46;py extracts information from ECJ target/classes/out&#46;stat to csv files. These files contains best fitness for each generation and each configuration in params. You can use other functions from analyze&#46;py and exp&#46;py to visualize converganse process and calculate Friedman and Nemenyi p-values to conclude configuration domination. 

## Post processing scripts
