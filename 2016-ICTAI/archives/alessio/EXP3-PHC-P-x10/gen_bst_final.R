f = read.table("bst.test.all")
k = rowMeans(f, na.rm = TRUE)
write.table(k, "bst.test.final", row.names = F, col.names = F)

f = read.table("bst.candi.all")
k = rowMeans(f, na.rm = TRUE)
write.table(k, "bst.candi.final", row.names = F, col.names = F)

