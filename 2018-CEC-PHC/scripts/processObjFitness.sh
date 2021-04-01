#!/bin/bash

if [ "$1" == "" ]; then
 echo "You forgot to put generation number"
 exit 1
fi

if [ "$2" == "" ]; then
  echo "You forgot to put #independent trials"
  exit 1
fi
totalBest=$(($1 * $2))
gen=$1
run=$2
genMinusOne=$(($gen-1))

b_removing_best_run_lines() {
for i in ./*out.stat
  do 
    numLines=$(cat $i | wc -l)      
    neededLines=$((numLines-10))        
    head -n${neededLines} $i > $i.only
  done
cat *.only>merged.out
rm *.only
}

r_take_genes_from_mergedout() {
cat >objective_fitness.R<<END
   file_merged    = "merged.out"
   file_result  = file("genes.out",open="w");
   con          = file(file_merged, open="r")
   line         = readLines(con)
   for (i in 1:length(line)) {
      if (i%%11 == 0)
         writeLines(line[i], file_result)
   }
   close(file_result)     
END
}



b_removing_best_run_lines 
r_take_genes_from_mergedout
module add apps/R/3.1.2
R -q -e 'source("objective_fitness.R")'

