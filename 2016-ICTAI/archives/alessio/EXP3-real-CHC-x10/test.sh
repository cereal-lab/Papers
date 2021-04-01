#!/bin/bash

b_removing_best_run_lines() {
for i in ./*out.stat
  do
    #sed -s -i '1i\\' $i
    #head -n26000 $i > $i.only
    head -n1100 $i > $i.only
  done
cat *.only>merged.out
rm *.only
}

r_take_genes_from_mergedout() {
cat >objective_fitness.R<<END
   file_merged    = "merged.out"
   file_result  = file("temp_result",open="w");
   con          = file(file_merged, open="r")
   line         = readLines(con)
   for (i in 1:length(line)) {
      if (i%%11 == 0)
         writeLines(line[i], file_result)
   }
close(file_result)  
f = read.table("temp_result")
k = rowMeans(f, na.rm = TRUE) * 4 
write.table(k, "obj_fit", row.names = F, col.names = F)    
END
}

b_splitting_by_run() {
a=1
b=0;
while [ $a -lt 15000 ];do
   let b=a+99
   sed  -n  "$a,$b p" obj_fit>$a.only
   let a=a+100   
done
paste *.only>bst.test.all
rm *.only
}


r_take_genes_from_mergedout
module add apps/R/3.1.2
R -q -e 'source("objective_fitness.R")'
b_splitting_by_run 


