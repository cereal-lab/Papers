t = read.table("finalmu")
k = rowMeans(t, na.rm=TRUE) 
write.table(k, "finalmu_only", row.names=F, col.names=F)
