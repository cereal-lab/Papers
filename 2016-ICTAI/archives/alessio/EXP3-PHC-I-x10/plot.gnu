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
plot "plot.final" using 1 title "Learners","plot.final" using 2 title "Practice Problems"
pause mouse key "..."
set term png
set output "SCA"
replot

