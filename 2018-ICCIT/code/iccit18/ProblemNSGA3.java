package iccit18;

import ec.*;
import ec.coevolve.*;

public class ProblemNSGA3 extends Problem implements GroupedProblemForm	{    
	private static final long serialVersionUID = 1L;
	public void preprocessPopulation(final EvolutionState state, Population pop, boolean[] updateFitness, boolean countVictoriesOnly)	{ return;  }

	public void evaluate(final EvolutionState state,
			final Individual[] ind,  // the individuals to evaluate together
			final boolean[] updateFitness,  
			final boolean countVictoriesOnly,
			int[] subpops,
			final int threadnum) { }
   
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





