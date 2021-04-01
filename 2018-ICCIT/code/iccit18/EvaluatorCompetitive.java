package iccit18;

import ec.coevolve.*;
import ec.util.Parameter;
import ec.*;
	
public class EvaluatorCompetitive extends MultiPopCoevolutionaryEvaluator {
	private static final long serialVersionUID = 1L; 
	public void setup( final EvolutionState state, final Parameter base )	{
		super.setup( state, base );
	}
	//This shuffle does not shuffle the indexes of other subpopulation's individuals because we want the individuals pair in terms of index
	protected void shuffle(EvolutionState state, int[] a)	{ return;	}
}

