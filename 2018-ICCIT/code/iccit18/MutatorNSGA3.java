package iccit18;

import ec.vector.*;
import ec.*;
import ec.multiobjective.nsga3.NSGA3MultiObjectiveFitness;
import ec.util.*;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;



public class MutatorNSGA3 extends BreedingPipeline {

  private static final long serialVersionUID = 1L;
  public static final String P_OURMUTATION = "our-mutation";

  // We have to specify a default base, even though we never use it 
  public Parameter defaultBase() { return VectorDefaults.base().push(P_OURMUTATION); }
  
  public static final int NUM_SOURCES = 1;
  // Return 1 -- we only use one source
  public int numSources() { return NUM_SOURCES; }
  
  private PayOffFunctions PF = new PayOffFunctions();
  private int popSize;
  private Map<Integer, Map<Integer[], Double[]>> interactionsOfCandidate = new HashMap<Integer, Map< Integer[], Double[]>>();
  private Map<Integer, Map<Integer[], Double[]>> interactionsOfTest = new HashMap<Integer, Map< Integer[], Double[]>>();
  private static final String CANDIDATE_FILE = "candidate.txt";
  private static final String TEST_FILE = "test.txt";
  private int currentJobNumber;
 

  
  public void setup(final EvolutionState state, final Parameter base)	{
	  super.setup(state,base);	
	  Parameter pm  = new Parameter(new String[]{"pop","subpop","0","size"}); 
	  popSize   = state.parameters.getInt(pm, null);	
	  popSize /= 2;
	  currentJobNumber = (Integer)state.job[0];
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
	
	private Map<Integer[], Double[]> getOutcomeByGenome(
			final EvolutionState state,
			Double[] ccOutcome, 
			Double[] ppOutcome, 
			IntegerVectorIndividual child, 
			IntegerVectorIndividual parent) {
		
		Map <Integer[], Double[]> tmp = new HashMap<Integer[], Double[]>();
		Integer[] tmpGenome = new Integer[child.genome.length];
		if (!ParetoDominance(ccOutcome, ppOutcome)) { //child does not Pareto dominate parent
  			for (int g = 0; g < child.genome.length; g++) {
  				child.genome[g] = parent.genome[g]; //revert the genome
  				tmpGenome[g] = parent.genome[g];
  			}
  			tmp.put(tmpGenome, ppOutcome);	
  			double [] tmp1 = new double[ppOutcome.length];
  			for (int i = 0; i < tmp1.length; i++)
  				tmp1[i] = ppOutcome[i];
  			((NSGA3MultiObjectiveFitness) parent.fitness).setObjectives(state, tmp1);
		}
  		else { //child dominates parent
  			for (int g = 0; g < child.genome.length; g++)
  				tmpGenome[g] = child.genome[g];		
  			tmp.put(tmpGenome, ccOutcome);
  			double [] tmp2 = new double[ccOutcome.length];
  			for (int i = 0; i < tmp2.length; i++)
  				tmp2[i] = ccOutcome[i];
  			((NSGA3MultiObjectiveFitness) child.fitness).setObjectives(state, tmp2);
		}
		return tmp;
	}
	
	private void writeFinalInfo(String fileName, 
			Map<Integer, Map<Integer[], Double[]>> data) {
		try  {
			
			BufferedWriter bw  = new BufferedWriter(new FileWriter(fileName));
			for (Map.Entry<Integer,Map<Integer[],Double[]>> pair: data.entrySet()) {
				int idx = pair.getKey();
				Integer[] genome = new Integer[2]; //TODO - get the genome size at setup like popsize or you can do state.subpop...
				Double[] outcome = new Double[popSize];
				bw.write(Integer.toString(idx) + " ");
				for (Map.Entry<Integer[], Double[]> innerPair : pair.getValue().entrySet()) {
					genome = innerPair.getKey();
					outcome = innerPair.getValue();
				}
				//System.out.println(idx + " " +Arrays.toString(genome) + " " +Arrays.toString(outcome));
				for (int i = 0; i < genome.length; i++)
					bw.write(Integer.toString(genome[i]) + " ");
				for (int i = 0; i < outcome.length; i++)
					if (i == outcome.length - 1)
						bw.write(Double.toString(outcome[i]));
					else 
						bw.write(Double.toString(outcome[i]) + " ");
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
		if (state.generation == state.numGenerations - 1 && subpopulation == 0) { // candidate	
			String fileNameCandidate = "job." + Integer.toString(currentJobNumber) + "." + CANDIDATE_FILE;
			writeFinalInfo(fileNameCandidate, interactionsOfCandidate);
		} else if (state.generation == state.numGenerations - 1 && subpopulation == 1) { // test
			String fileNameTest = "job." + Integer.toString(currentJobNumber) + "." + TEST_FILE;
			writeFinalInfo(fileNameTest, interactionsOfTest);
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
      System.out.println(state.population.subpops.get(1).individuals.size() + ", " +popSize + ", " +subpopulation);
      for(int q=start;q<n+start;q++) {
    	  	IntegerVectorIndividual child  = (IntegerVectorIndividual) inds.get(q);     //current individual after selection and crossover
  			IntegerVectorIndividual parent = (IntegerVectorIndividual)state.population.subpops.get(subpopulation).individuals.get(q); // old individual in the same index
  
  			for(int x=0;x<child.genome.length;x++)
  				if (state.random[thread].nextBoolean(species.mutationProbability(x))) {
  					int index = new MersenneTwister().nextInt(2);
  					if (index == 0)  child.genome[x] += 1; //new MersenneTwisterFast().nextInt(10); //TODO - make it from config file after submission
  					else   child.genome[x] -= 1; //new MersenneTwisterFast().nextInt(10);		
              }
  			//System.out.println(Arrays.toString(child.genome) + ", " + Arrays.toString(parent.genome));
  			Double [] pOutcome = new Double[popSize];
  			Double [] cOutcome = new Double[popSize];
  			for (int o = 0; o < popSize; o++) {
  				
  				if (subpopulation == 0) { // candidate
  					IntegerVectorIndividual test = (IntegerVectorIndividual)state.population.subpops.get(1).individuals.get(o);
  					pOutcome[o] = PF.compOnOne(parent, test);
  					cOutcome[o] = PF.compOnOne(child, test);		
  				 }
  				else { // test
  					IntegerVectorIndividual candidate = (IntegerVectorIndividual) state.population.subpops.get(0).individuals.get(o);
  					pOutcome[o] = PF.compOnOne(parent, candidate);
  					cOutcome[o] = PF.compOnOne(child, candidate);
  				}
  			 }
  			int numObjectives = ((NSGA3MultiObjectiveFitness)child.fitness).getNumObjectives();
  			Double [] ppOutcome = new Double[numObjectives];
  			Double [] ccOutcome = new Double[numObjectives];
  			double ob1P = 0;
  			double ob2P = 0;
  			double ob1C = 0;
  			double ob2C = 0;
  			for (int i = 0; i < pOutcome.length; i++) {
  				if (i < numObjectives/2) {
  					ob1P += pOutcome[i];
  					ob1C += cOutcome[i];
  				}
  				else {
  					ob2P += pOutcome[i];
  					ob2C += cOutcome[i];
  				}
  			}
  			ppOutcome[0] = ob1P;
  			ppOutcome[1] = ob2P;
  			ccOutcome[0] = ob1C;
  			ccOutcome[1] = ob2C;
  			
  			System.out.println(ob1P + ", " + ob2P);
  			System.out.println(ob1C + ", " +ob2C);
            
  			if (subpopulation == 0) 
  				interactionsOfCandidate.put(q, getOutcomeByGenome(state, ccOutcome, ppOutcome, child, parent));
  			else
  				interactionsOfTest.put(q, getOutcomeByGenome(state, ccOutcome, ppOutcome, child, parent));
  				
  			child.evaluated = true;
  			}
      return n;
      }
}
  
  
  

