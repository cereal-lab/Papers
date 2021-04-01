
package iccit18;

import ec.vector.*;
import ec.*;
import ec.util.*;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;



public class MutatorDominance extends BreedingPipeline {

  private static final long serialVersionUID = 1L;
  public static final String P_OURMUTATION = "our-mutation";

  // We have to specify a default base, even though we never use it 
  public Parameter defaultBase() { return VectorDefaults.base().push(P_OURMUTATION); }
  
  public static final int NUM_SOURCES = 1;
  // Return 1 -- we only use one source
  public int numSources() { return NUM_SOURCES; }
  
  private PayOffFunctions PF = new PayOffFunctions();
  private int popSize;
  private int pDominates;
  private int cDominates;
  private int nonComp;
  private int equals;
  private Map<Integer, ArrayList<Integer>> dominanceStat = new HashMap<Integer, ArrayList<Integer>>();
 
  public void setup(final EvolutionState state, final Parameter base)	{
	  super.setup(state,base);	
	  Parameter pm  = new Parameter(new String[]{"pop","subpop","0","size"}); 
	  popSize   = state.parameters.getInt(pm, null);	
	  pDominates = 0;
	  cDominates = 0;
	  equals = 0;
	  nonComp = 0;
  }
  
	private boolean ParetoDominance (Double [] scoresMe, Double [] scoresOther )  {
		boolean MeDominant = false;
		for (int i = 0; i < scoresMe.length; i++)   {
			if (scoresMe[i] > scoresOther[i])
				MeDominant = true;
			else if (scoresMe[i] < scoresOther[i])
				return false;
		}
		return MeDominant;
	}
	
	private boolean Equals(Double [] a, Double [] b) {
		for (int x = 0; x < a.length; x++)
			if(a[x] != b[x]) return false;
		return true;
	}
	
	private void writeDominanceInfo(String fileName, 
			Map<Integer, ArrayList<Integer>> data) {
		try  {
			
			BufferedWriter bw  = new BufferedWriter(new FileWriter(fileName));
			for (Map.Entry<Integer,ArrayList<Integer>> pair: data.entrySet()) {
				for (int val : pair.getValue()) 
					bw.write(Integer.toString(val) + " ");
				bw.newLine();	
			}	
			bw.close();	
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public void finishProducing(final EvolutionState state,
			final int subpopulation,
			final int thread) {
		ArrayList<Integer> tmp = new ArrayList<Integer>();
		tmp.add(0, pDominates);
		tmp.add(1, cDominates);
		tmp.add(2, nonComp);
		tmp.add(3, equals);
		dominanceStat.put(state.generation, tmp);
		if (subpopulation == 0) { // candidate	
			String fileName = "candidateDominance.txt";
			writeDominanceInfo(fileName, dominanceStat);
		}
		for(int x=0;x<sources.length;x++) 
			if (x==0 || sources[x]!=sources[x-1])
				sources[x].finishProducing(state,subpopulation,thread);
		
	}
	
  public int produce(final int min,
      final int max,
      final int subpopulation,
      final ArrayList<Individual> inds,
      final EvolutionState state,
      final int thread, HashMap<String, Object> misc) {
      int start = inds.size();
      
      int n = sources[0].produce(min,max,subpopulation,inds, state,thread, misc);
      if (!state.random[thread].nextBoolean(likelihood)) {return n; }

      if (!(inds.get(start) instanceof IntegerVectorIndividual)) 
          state.output.fatal("PhcpMutator didn't get an IntegerVectorIndividual." +
                              "The offending individual is in subpopulation " + subpopulation + 
                               " and it's:" + inds.get(start));
      IntegerVectorSpecies species = (IntegerVectorSpecies)(inds.get(start).species);
      
      for(int q=start;q<n+start;q++) {
    	  	IntegerVectorIndividual child  = (IntegerVectorIndividual) inds.get(q);     //current individual after selection and crossover
  			IntegerVectorIndividual parent = (IntegerVectorIndividual)state.population.subpops.get(subpopulation).individuals.get(q); // old individual in the same index
  
  			for(int x=0;x<child.genome.length;x++)
  				if (state.random[thread].nextBoolean(species.mutationProbability(x))) {
  					int index = new MersenneTwister().nextInt(2);
  					if (index == 0)  child.genome[x] += 1; 
  					else   child.genome[x] -= 1; 	
              }
  			Double [] pOutcome = new Double[popSize];
  			Double [] cOutcome = new Double[popSize];
  			for (int o = 0; o < popSize; o++) {
  				if (subpopulation == 0) { // candidate
  					IntegerVectorIndividual test = (IntegerVectorIndividual)state.population.subpops.get(1).individuals.get(o);
  					pOutcome[o] = PF.focusing(parent, test);
  					cOutcome[o] = PF.focusing(child, test);		
  				 }
  				else { // test
  					IntegerVectorIndividual candidate = (IntegerVectorIndividual) state.population.subpops.get(0).individuals.get(o);
  					pOutcome[o] = PF.focusing(parent, candidate);
  					cOutcome[o] = PF.focusing(child, candidate);
  				}
  			 }
  			boolean nonComparable = true;
  			boolean childBetter = false;
  			if (ParetoDominance(pOutcome, cOutcome)) { 
  				nonComparable = false;
  				pDominates++;
  			}
  			if (ParetoDominance(cOutcome, pOutcome)) {
  				childBetter = true;
  				nonComparable = false;
  				cDominates++;
  			}
  			if (Equals(pOutcome, cOutcome)) {
  				 nonComparable = false;
  				 childBetter = false;
  				 equals++;
  			 }
  			
  			if (nonComparable) 
  				nonComp++;
  			
  			if (!childBetter) 
  				for (int g = 0; g < child.genome.length; g++) 
  	  				child.genome[g] = parent.genome[g]; //revert the genome
  			child.evaluated = true;
  			}
      return n;
      }
}
  
  
  

