#!/bin/bash
generate_bst_final() {
cat > gen_bst_final.R <<EOF
f = read.table("bst.test.all")
k = rowMeans(f, na.rm = TRUE)
write.table(k, "bst.test.final", row.names = F, col.names = F)

f = read.table("bst.candi.all")
k = rowMeans(f, na.rm = TRUE)
write.table(k, "bst.candi.final", row.names = F, col.names = F)

EOF
}

paste_finals() {
   paste *.final>plot.final
}
g_plot() {
cat > plot.gnu <<EOF
set style data lines
set key font ", 15"
set yrange [0:40]
set xlabel "Evolutionary Time"
set xlabel font  " , 20"
set ylabel "Mean Objective Fitness"
set ylabel font ", 20"
set title "P-CHC"
set title font ",20"
set xtics font ",20"
set ytics font ",20"
plot "plot.final" using 1 title "Learners",\
"plot.final" using 2 title "Practice Problems"
pause mouse key "..."
set term png
set output "SCA"
replot

EOF
}
generate_RScript() {
   cat > results.R <<EOF
        library(matrixStats)
        test = read.table("bst.test.final")   
	candi = read.table("bst.candi.final")
        meanP = colMeans(test)
        sigmaP = colSds(data.matrix(test,rownames.force=NA),na.rm=TRUE)
        cat("\n Mean of Practice Problem",meanP)
        cat("\n Sigma of Practice Problem",sigmaP)   
        #print(t.test(test, candi, alternative="two.sided", mu=0, paired = FALSE, var.equals = FALSE, conf.level = 0.95)) 
         
EOF
}
generate_bst_final
module add apps/R/3.1.2
R -q -e 'source("gen_bst_final.R")'
paste_finals
g_plot
gnuplot < plot.gnu
generate_RScript
R -q -e 'source("results.R")'



