        library(matrixStats)
        test = read.table("bst.test.final")   
	candi = read.table("bst.candi.final")
        meanP = colMeans(test)
        sigmaP = colSds(data.matrix(test,rownames.force=NA),na.rm=TRUE)
        cat("\n Mean of Practice Problem",meanP)
        cat("\n Sigma of Practice Problem",sigmaP)   
        #print(t.test(test, candi, alternative="two.sided", mu=0, paired = FALSE, var.equals = FALSE, conf.level = 0.95)) 
         
