#!/bin/bash

g_plot() {
cat > plot.gnu <<EOF
set style data lines
set yrange [0:40]
set xlabel "Evolutionary Time"
set xlabel font  " , 20"
set ylabel "Learner genotype's value"
set ylabel font ", 20"
set title "P-CHC"
set title font ",20"
set xtics font ",20"
set ytics font ",20"
plot "mu-sigma" using 1 title "Learner's genotype (Meu)",\
"mu-sigma" using 2 title "Learner's genotype (Sigma)"
pause mouse key "..."
set term png
set output "SCA"
replot

EOF
}
g_plot
gnuplot < plot.gnu


