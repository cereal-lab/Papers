package iccit18;

import ec.*;
import ec.simple.*;
import ec.vector.*;
import ec.coevolve.*;

public class ProblemIccit18 extends Problem implements GroupedProblemForm	{    
	private static final long serialVersionUID = 1L;
	public void preprocessPopulation(final EvolutionState state, Population pop, boolean[] updateFitness, boolean countVictoriesOnly)	{ return;  }

	public void evaluate(final EvolutionState state,
			final Individual[] ind,  // the individuals to evaluate together
			final boolean[] updateFitness,  
			final boolean countVictoriesOnly,
			int[] subpops,
			final int threadnum) {
		if( ind.length != 2 || updateFitness.length != 2)
			state.output.fatal( "The InternalSumProblem evaluates only one individual at a time." );

		if( ! ( ind[0] instanceof IntegerVectorIndividual ) )
			state.output.fatal( "The individuals in the Problem should be IntegerVectorIndividuals." );
		
        for (int p = 0; p < subpops.length; p++) {
        	IntegerVectorIndividual aIndiv = (IntegerVectorIndividual)ind[p];
        	double fitness = 0;
        	for (int g = 0; g < aIndiv.genome.length; g++) 
        		fitness += aIndiv.genome[g];
        	//System.out.println(updateFitness[p] + ", " + p + ", " + fitness);
        	if(updateFitness[p]) {
        		SimpleFitness fit = (SimpleFitness) aIndiv.fitness;
        		fit.setFitness(state, fitness, false);
        	}		
        }	
	}
   
	public int postprocessPopulation(final EvolutionState state, Population pop, boolean[] updateFitness, boolean countVictoriesOnly)	{
		for( int i = 0 ; i < pop.subpops.size() ; i++ ) {
			if (updateFitness[i]) {
				for( int j = 0 ; j < pop.subpops.get(i).individuals.size() ; j++ )	            
					pop.subpops.get(i).individuals.get(j).evaluated = true;
			}
		}
		return pop.subpops.get(0).individuals.size(); //TODO - see if it returns numberOfIndiv or just 1
	}
}





