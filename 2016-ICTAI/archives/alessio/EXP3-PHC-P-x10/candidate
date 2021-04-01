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
   k = rowMeans(f, na.rm=TRUE)*4
   write.table(k,"obj_fit", row.names=F, col.names=F)
   
END
}

b_mu_sigma_seperate() {
a=1
b=0;
while [ $a -lt 15000 ];do
   let b=a+99
   sed  -n  "$a,$b p" temp_result>$a.only
   let a=a+100   
done

for i in ./*.only
 do
  cut --fields=1,2,3 -d ' ' $i>$i.mu.all
 done
cat *.mu.all>mu.all 

for i in ./*.only
  do
   cut -f4 -d ' ' $i>$i.sigma.all
  done
paste *.sigma.all>ssigma.all

rm *.only
rm *.mu.all
rm *.sigma.all
}

r_mu_sigma_single() {
cat>mu_sigma.R<<END
 t = read.table("mu.all")
 k = rowMeans(t,na.rm=TRUE)* 3
 write.table(k, "test.mu", row.names=F, col.names=F);
 
 f = read.table("ssigma.all");
 k = rowMeans(f, na.rm = TRUE)  
 write.table(k, "sigma_only", row.names = F, col.names = F);
END
}

b_mu_seperate() {
a=1
b=0;
while [ $a -lt 15000 ];do
   let b=a+99
   sed  -n  "$a,$b p" test.mu>$a.testmu
   let a=a+100   
done
paste *.testmu>finalmu
rm *.testmu
}

b_final_mu() {
cat >finalmu.R<<END
t = read.table("finalmu")
k = rowMeans(t, na.rm=TRUE) 
write.table(k, "finalmu_only", row.names=F, col.names=F)
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
paste *.only>bst.candi.all
paste finalmu_only sigma_only>mu-sigma
rm *.only
}

b_removing_best_run_lines 
r_take_genes_from_mergedout
#module add apps/R/3.1.2
R -q -e 'source("objective_fitness.R")'
b_mu_sigma_seperate
r_mu_sigma_single
R -q -e 'source("mu_sigma.R")'
b_mu_seperate
b_final_mu
R -q -e 'source("finalmu.R")'
b_splitting_by_run


