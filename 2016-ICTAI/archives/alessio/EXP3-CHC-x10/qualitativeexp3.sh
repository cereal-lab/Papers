#!/bin/bash
b_getting_last_generations() {
x=155201 #Formula 311 * number of generation + 12 = START, +3*50*2 - 1 = END
y=155500
for i in ./*custom.stat
  do
    sed -n -e "$x, $y p" -e "$y q" $i > $i.gen500only
    head -n150 $i.gen500only>$i.testonly
    m=151
    n=300
    sed -n -e "$m, $n p" -e "$n q" $i.gen500only>$i.candionly    
  done

cat *candionly>candi.out
cat *testonly>test.out
rm *only
}

r_take_individuals_from_test() {
cat >test_individuals.R<<END
   file_test    = "test.out"
   file_result  = file("temp_result",open="w");
   con          = file(file_test, open="r")
   line         = readLines(con)
   for (i in 1:length(line)) {
      if (i%%3 == 0)
         writeLines(line[i], file_result)
   }
   close(file_result)  
f = read.table("temp_result")
vector = c()
for (i in 1:nrow(f)) {
  v <- c(abs(f[i,1]-f[i,2]), abs(f[i,1]-f[i,3]), abs(f[i,1]-f[i,4]), abs(f[i,2]-f[i,3]), abs(f[i,2]-f[i,4]), abs(f[i,3]-f[i,4]))
   vector[i] <- v[which.max(v)]   
}
k <- transform(f, new.col=vector)
write.table(k, "test_gene_and_difference", row.names = F, col.names = F)    
END
}

b_test_xy_difference() {
cut -f5 -d ' ' test_gene_and_difference>test_xy_difference
a=1
b=0;
while [ $a -lt 2500 ];do
   let b=a+49
   sed  -n  "$a,$b p" test_xy_difference>$a.only
   let a=a+50   
done
paste *.only>test_xy_difference_merged
rm *.only
}

r_test_xy_mean_difference() {
cat>test_xy_mean_difference.R<<END
f = read.table("test_xy_difference_merged")
k = rowMeans(f, na.rm = TRUE)
write.table(k, "test_xy_mean_difference_by_run", row.names=F, col.names=F)
END
}

r_take_individuals_from_candi() {
cat >candi_individuals.R<<END
   file_test    = "candi.out"
   file_result  = file("temp_result_candi",open="w");
   con          = file(file_test, open="r")
   line         = readLines(con)
   for (i in 1:length(line)) {
      if (i%%3 == 0)
         writeLines(line[i], file_result)
   }
   close(file_result)  
f = read.table("temp_result_candi")
k <- transform(f, new.col = abs(V1 - V2))
write.table(k, "candi_gene_and_difference", row.names = F, col.names = F)    
END
}

b_candi_xy_difference() {
cut -f3 -d ' ' candi_gene_and_difference>candi_xy_difference
a=1
b=0;
while [ $a -lt 2500 ];do
   let b=a+49
   sed  -n  "$a,$b p" candi_xy_difference>$a.only
   let a=a+50   
done
paste *.only>candi_xy_difference_merged
rm *.only
}

r_candi_xy_mean_difference() {
cat>candi_xy_mean_difference.R<<END
f = read.table("candi_xy_difference_merged")
k = rowMeans(f, na.rm = TRUE)
write.table(k, "candi_xy_mean_difference_by_run", row.names=F, col.names=F)
END
}
b_getting_last_generations 
r_take_individuals_from_test
#r_take_individuals_from_candi

module add apps/R/3.1.2
R -q -e 'source("test_individuals.R")'
#R -q -e 'source("candi_individuals.R")'

b_test_xy_difference
r_test_xy_mean_difference

#b_candi_xy_difference
#r_candi_xy_mean_difference

R -q -e 'source("test_xy_mean_difference.R")'
#R -q -e 'source("candi_xy_mean_difference.R")' 

