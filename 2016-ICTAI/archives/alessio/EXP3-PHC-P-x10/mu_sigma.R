 t = read.table("mu.all")
 k = rowMeans(t,na.rm=TRUE)* 3
 write.table(k, "test.mu", row.names=F, col.names=F);
 
 f = read.table("ssigma.all");
 k = rowMeans(f, na.rm = TRUE)  
 write.table(k, "sigma_only", row.names = F, col.names = F);
