package iccit18;
import java.util.ArrayList;

import ec.EvolutionState;
import ec.Population;
import ec.multiobjective.nsga3.NSGA3Breeder;
import ec.util.Parameter;


public class BreederNSGA3 extends NSGA3Breeder {
	  /**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public void setup(final EvolutionState state, final Parameter base) {
		  super.setup(state, base);
      }
	  
	  public Population breedPopulation(EvolutionState state) {
		  Population oldPop = (Population) state.population;
		  Population newPop = super.breedPopulation(state);
		  
		  ArrayList<ec.Subpopulation> subpops = oldPop.subpops;
		  ArrayList<ec.Individual> combinedIndivs = new ArrayList<ec.Individual>() ;
		  ArrayList<ec.Subpopulation> oldSubPops = new ArrayList<ec.Subpopulation>();
		  ArrayList<ec.Subpopulation> newSubpop = new ArrayList<ec.Subpopulation>();
		  
		  for (int i = 0; i < subpops.size(); i++) {
			  oldSubPops.add(oldPop.subpops.get(i));
			  newSubpop.add(newPop.subpops.get(i));
			  combinedIndivs.addAll(newSubpop.get(i).individuals);
			  combinedIndivs.addAll(oldSubPops.get(i).individuals);
			  newSubpop.get(i).individuals.addAll(combinedIndivs);
		  }
		System.out.println(newPop.subpops.size() + ", " + newPop.subpops.get(0).individuals.size());
		return newPop;
	  }
}
	  
