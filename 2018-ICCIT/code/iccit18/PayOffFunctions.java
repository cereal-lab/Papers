package iccit18;
import ec.vector.*;

public class PayOffFunctions {
	
    private int getMaxDimension(int [] genome) {
    	int max = genome[0];
    	int dimension = 0;
    	for (int i = 1; i < genome.length; i++)
    		if (genome[i] > max) {
    			max = genome[i];
    			dimension = i;
    		}
    	return dimension;
    	}
    private int getClosedDimension(int [] firstGenome, int [] secondGenome) {
    	int diff = Math.abs(firstGenome[0] - secondGenome[0]);
    	int minDimesion = 0;
    	for (int g = 1; g < firstGenome.length; g++) 
    		if (diff < Math.abs(firstGenome[g] - secondGenome[g]))
    			return g;
    	return minDimesion;
    }
	public double compOnOne(IntegerVectorIndividual tempMe, IntegerVectorIndividual tempOther) { 
		int maxDimension = getMaxDimension(tempOther.genome);
		if (tempMe.genome[maxDimension] >= tempOther.genome[maxDimension])
			return 1.0; // tempMe wins
		else return 0.0;
			
	}
	
	public double focusing(IntegerVectorIndividual tempMe, IntegerVectorIndividual tempOther) { 
		int maxDimension = getMaxDimension(tempOther.genome);
		if (tempMe.genome[maxDimension] > tempOther.genome[maxDimension])
			return 1.0; // tempMe wins
		else return 0.0;		
	}
	
	public double intransitive(IntegerVectorIndividual tempMe, IntegerVectorIndividual tempOther) { 
		int closedDim = getClosedDimension(tempMe.genome, tempOther.genome);
		if (tempMe.genome[closedDim] > tempOther.genome[closedDim])
			return 1.0; // tempMe wins
		else return 0.0;		
	}
}





