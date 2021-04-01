package iccit18;

import ec.select.*;
import ec.*;
import ec.util.*;
import ec.steadystate.*;
/*
 * Implements selection mechanism in Bucci, 2003 paper 
 */
public class NoSelection extends SelectionMethod implements SteadyStateBSourceForm	 {
	private static final long serialVersionUID = 1L;
	public static final String P_CUSTOM = "custom";
	private int index;
	private int callCount;

	public Parameter defaultBase()	
	{
		return SelectDefaults.base().push(P_CUSTOM);	
	}

	public void prepareToProduce(final EvolutionState s,
			final int subpopulation,
			final int thread)	{
		index = -1;	
		callCount = 0;
	}

	public int produce(final int subpopulation,
			final EvolutionState state,
			final int thread)	{
		
		callCount++;   		
		if (callCount % 2 != 0) { //Each time produce in selection method calls produce in this class two times.
			if (index ==  state.population.subpops.get(subpopulation).individuals.size())  index = 0;		
			else index++;	
		}		
		return index;
	}	

	public void individualReplaced(final SteadyStateEvolutionState state,
			final int subpopulation,
			final int thread,
			final int individual) { return; }

	public void sourcesAreProperForm(final SteadyStateEvolutionState state)	{ return; }    
}
