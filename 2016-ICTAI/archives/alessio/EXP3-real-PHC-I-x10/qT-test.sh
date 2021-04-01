#!/bin/bash
paste_finals() {
   paste *.only>plot.final
}
g_plot() {
cat > plot.gnu <<EOF
set style data lines
plot "plot.final" using 1 title "PCHC candidate ",\
"plot.final" using 2 title "PPHC candidate", \
"plot.final" using 3 title "PPHC test"
pause mouse key "..."
set term png
set xlabel "Evolutionary Time"
set ylabel "Mean difference of two dimensions"
#set title "Noise Level = 0%"
set output "IG-N0"
replot
EOF
}
generate_RScript() {
   cat > results.R <<EOF
	library(matrixStats)   
	#pphccandi = read.table("candi_xy_mean_difference_by_run")
        test = read.table ("test_xy_mean_difference_by_run")   
         #print(t.test(pchc, pphc, alternative="two.sided", mu=0, paired = FALSE, var.equals = FALSE, conf.level = 0.99)) 

         #meanPPHCcandi  = colMeans(pphccandi)
         meanP = colMeans(test)

         #sigmaPPHCcandi = colSds(data.matrix(pphccandi,rownames.force=NA), na.rm=TRUE)
         sigmaP  = colSds(data.matrix(test,rownames.force=NA), na.rm=TRUE)

         #cat ("\n PPHC-candi Mean  ", meanPPHCcandi)
         #cat ("\n PPHC-test Mean  ",  meanPPHCtest)
 
         cat ("\n mean of Practice Problem  ", meanP)
         cat("\n Sigma of Practice Problem  ", sigmaP)
EOF
}

module add apps/R/3.1.2

paste_finals
#g_plot
#gnuplot < plot.gnu
generate_RScript
R -q -e 'source("results.R")'



