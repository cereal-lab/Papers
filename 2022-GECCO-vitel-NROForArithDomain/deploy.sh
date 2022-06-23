# runtime: java 1.8 or later, python3, git
git clone --depth 1 --branch arith_domain https://github.com/cereal-lab/ecj.git #to fetch arith_domain tagged version to ecj folder
cd ecj 
make jar # builds ecj with NRO 
# use java commands from data/exp0 or next one 
# NRO rewrites are placed in ec.domain.regression.strategy package AxiomsX classes
java -cp target/ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4

# post processing
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
# specify instead of 2 number of runs for one experiment
# check analyze.py for information of evolutionary process configuration and output or see README
python3 analyze.py 2
deactivate