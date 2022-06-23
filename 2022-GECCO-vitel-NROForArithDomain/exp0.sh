#!/bin/bash
#SBATCH --job-name=NRO
#SBATCH --time=48:00:00
#SBATCH --output=%j.out
#SBATCH --mem=8G
#SBATCH --array=0-62

declare -A cfg
cfg[R1-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=r-1 -p eval.problem.vars=x'
cfg[R1-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[R1-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[R1-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[R1-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[R1-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[R1-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-1 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[R2-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=r-2 -p eval.problem.vars=x'
cfg[R2-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=r-2 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[R2-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=r-2 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[R2-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-2 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[R2-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-2 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[R2-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-2 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[R2-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=r-2 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Kj3-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x'
cfg[Kj3-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Kj3-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Kj3-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Kj3-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Kj3-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Kj3-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-3 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Kj4-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x'
cfg[Kj4-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Kj4-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Kj4-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Kj4-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Kj4-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Kj4-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-4 -p eval.problem.vars=x -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Kj11-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y'
cfg[Kj11-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Kj11-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Kj11-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Kj11-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Kj11-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Kj11-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=keijzer-11 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Ng9-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y'
cfg[Ng9-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Ng9-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Ng9-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Ng9-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Ng9-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Ng9-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-9 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Ng12-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y'
cfg[Ng12-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Ng12-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Ng12-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Ng12-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Ng12-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Ng12-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=nguyen-12 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Pg1-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y'
cfg[Pg1-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Pg1-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Pg1-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Pg1-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Pg1-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Pg1-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=pagie-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

cfg[Vl1-RTsTx]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y'
cfg[Vl1-RTsTmx-1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.01'
cfg[Vl1-RTsTmx-10]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y -p gp.koza.xover.source.0=ec.gp.koza.MutationPipeline -p gp.koza.xover.source.1=same -p gp.koza.mutate.likelihood=0.1'
cfg[Vl1-RTsTxN-str1]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms'
cfg[Vl1-RTsTxN-str2]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms2'
cfg[Vl1-RTsTxN-str3]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms3'
cfg[Vl1-RTsTxN-str4]='java -cp ../ecj-27.jar ec.Evolve -at ec.Evolve -from domain/regression/base.n2.params -p eval.problem.type=vladislavleva-1 -p eval.problem.vars=x,y -p gp.koza.mutate.strategy.name=ec.domain.regression.strategy.Axioms4'

keys=(${!cfg[@]})
pickedKey=${keys[$SLURM_ARRAY_TASK_ID]}
pickedCfg=${cfg[$pickedKey]}
mkdir "$pickedKey-$SLURM_ARRAY_JOB_ID"
cd "$pickedKey-$SLURM_ARRAY_JOB_ID"
echo "task id: $SLURM_ARRAY_TASK_ID, key: $pickedKey, cfg: $pickedCfg"
eval "$pickedCfg"