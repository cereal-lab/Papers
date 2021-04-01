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
