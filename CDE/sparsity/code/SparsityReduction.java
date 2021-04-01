package ec.cecsecond;

import ec.ictai16.*;
import ec.simple.*;
import ec.vector.*;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Random;

import ec.*;
import ec.util.*;

public class SparsityReduction extends BreedingPipeline 
{	
	public  static final String DECA_SIM_MUTATION = "DECA-SIM-MUTATION";	
	public static final int NUM_SOURCES           = 1;
	private static final int PROBLEM_SUBPOP_INDEX = 0;
	private static final int LEARNER_SUBPOP_INDEX = 1;
	private static final int HASHTABLE_SIZE       = 10000;
	private static final int STUDENT = 100;
	private static final int PUZZLE = 10000;
	private static Individual [] childs;
	private static boolean[] evaluationStatus;
	
	private String F_SPARSITY       = "sparsity.txt";
    private int popSize;      
	private int minimumEvaluation;
	private double epsilon;
	private double [][] interaction;
	private  List <Integer> uniqueGenotypeHolder; 	
	int currentJob;
	MersenneTwisterFast mtf;
	private double probComp;
	
	File file = null;
	FileWriter fw = null;
	BufferedWriter bw =  null;
	
    public Parameter defaultBase(){ return VectorDefaults.base().push(DECA_SIM_MUTATION);	}   
	
    public int numSources(){ return NUM_SOURCES;	}

	public void setup(final EvolutionState state, final Parameter base)	
	{
		super.setup(state,base);		
		mtf = state.random[0];
		Parameter pm  = new Parameter(new String[]{"pop","subpop","0","size"});
		popSize   = state.parameters.getInt(pm, null);		
		
		Parameter pmMinEval  = new Parameter(new String[]{"eval","problem","min-eval"}); 
		minimumEvaluation = state.parameters.getInt(pmMinEval, null);
		
		Parameter pmEpsilon  = new Parameter(new String[]{"eval","problem","epsilon"});
		epsilon = state.parameters.getDouble(pmEpsilon, null);
		
		Parameter pmProbComp  = new Parameter(new String[]{"eval","problem","prob-comp"});
		probComp = state.parameters.getDouble(pmProbComp, null);
			
		uniqueGenotypeHolder = new ArrayList<Integer>();
		interaction = new double[STUDENT][PUZZLE];
		childs = new Individual[popSize] ;
	    evaluationStatus	= new boolean[popSize] ;
	    currentJob = (Integer)(state.job[0]);
	}


	private int getHash(IntegerVectorIndividual individual) 
	{
		int indLen        = individual.genome.length;
		int [] genome = new int[indLen];
		
		for (int x = 0; x < indLen; x++)
			genome[x]     = individual.genome[x];			
		return (Arrays.hashCode(genome) & 0x7FFFFFF) % HASHTABLE_SIZE;	
	}
	
	public int produce(final int min, 
			final int max, 
			final int start,
			final int subpopulation,
			final Individual[] inds,
			final EvolutionState state,
			final int thread) 
	{

		int n = sources[0].produce(min,max,start,subpopulation,inds,state,thread);
		if (!state.random[thread].nextBoolean(likelihood))
			return reproduce(n, start, subpopulation, inds, state, thread, false);  

		if (!(sources[0] instanceof BreedingPipeline))
			for(int q=start;q<n+start;q++)
				inds[q] = (Individual)(inds[q].clone());

		if (!(inds[start] instanceof IntegerVectorIndividual)) 
			state.output.fatal("DECA-SIM-MUTATION didn't get an IntegerVectorIndividual." +
					"The offending individual is in subpopulation " + subpopulation + " and it's:" + inds[start]);

		IntegerVectorSpecies species  = (IntegerVectorSpecies)(inds[start].species);       
		for(int indiv = start; indiv < n + start; indiv++)	
		{
			IntegerVectorIndividual child  = (IntegerVectorIndividual) inds[indiv];     //current individual after selection and crossover
			IntegerVectorIndividual parent = (IntegerVectorIndividual)state.population.subpops[subpopulation].individuals[indiv]; // old individual in the same index
	
			if (!uniqueGenotypeHolder.contains(getHash(parent)))
			{
				uniqueGenotypeHolder.add(getHash(parent));
			}
				
			for(int x=0;x<child.genome.length;x++) 
			{
				if (state.random[thread].nextBoolean(species.mutationProbability(x))) 
				{
					int index = mtf.nextInt(2);
				
					if (index == 0) 
					  child.genome[x] += 1;
					else   						 
					  child.genome[x] -= 1;
				} 		
			}
			
			childs[indiv] = child;
			evaluationStatus[indiv] = false;
			
			if (!uniqueGenotypeHolder.contains(getHash(child)))
			{
				uniqueGenotypeHolder.add(getHash(child));
			}		
			child.evaluated = false;
		} 
		return n;
	}
	
	private int getProbletCompleteness(int studentID, final EvolutionState state) 
	{						
		
		int probletsSize = uniqueGenotypeHolder.size();
		int probletId = -1;
		int studentIdx   = studentID;
        double minScore = 1.0; 
         
		for (int problet = 0; problet < probletsSize; problet++) 
		{								 
			double holes = 0, fills = 0, scoreCurr = 0;
			int hash = uniqueGenotypeHolder.get(problet);
			if (isInCurrentGeneration(hash, state))
			{
				for (int student = 0; student < STUDENT; student++ )  
				{				
					if (interaction[student][problet] == 0) 				
						holes = holes + 1;	
					else
						fills = fills + 1;							
				}
				
				if (fills + holes == fills) // this problet is evaluated by all the current students
					scoreCurr = 1.0; // maximum score, we will not consider this problet
				else
					scoreCurr = fills/(holes + fills);								
				
				if ((scoreCurr < minScore ) && (interaction[studentIdx][problet] == 0)) // minimum score and the student has not evaluated it yet
				{
				   minScore = scoreCurr;
				   probletId = problet; //stores the problet genotype whose score is minimum
				}
			}
		}
			
		return probletId;
	}
	
	private double getAvgMove (int probletId) 
	{
		double totalMove = 0;
		int numStudentSolved = 0;
		for (int student = 0; student < STUDENT; student++)
		{
			if (interaction[student][probletId] > 0)
			{
				totalMove += interaction[student][probletId];
				numStudentSolved += 1;
			}
		}
		numStudentSolved = (numStudentSolved == 0) ? 1 : numStudentSolved;
		return totalMove/numStudentSolved;
	}
	
	private boolean isInCurrentGeneration(int hash, final EvolutionState state)
	{
		boolean foundInParent = false;
		boolean foundInChild = false;
		
		for (int p = 0; p < popSize; p++)
		{
			IntegerVectorIndividual parent = (IntegerVectorIndividual)state.population.subpops[PROBLEM_SUBPOP_INDEX].individuals[p];
			int pHash = getHash(parent);
			if (pHash == hash)
			{
				foundInParent = true;
				break;
			}
				
			IntegerVectorIndividual child = (IntegerVectorIndividual)childs[p];
			int cHash = getHash(child);
			
			if (cHash == hash)
			{
				foundInChild = true;
				break;
			}	
		}
		return (foundInChild == false || foundInParent == false);
		
	}
	private int getProbletFatigue(int studentID, final EvolutionState state)
	{
		int probletSize =  uniqueGenotypeHolder.size();
        int studentIndex = studentID;
        int probletId = 0;
        
		if (mtf.nextDouble() <= epsilon) //Exploration 
		{	
			ArrayList<Integer> pooledProblet = new ArrayList<Integer>(); 
			
			for (int problet = 0; problet < probletSize; problet++)
			{
				int hash = uniqueGenotypeHolder.get(problet);
				if (interaction[studentIndex][problet] == 0 && isInCurrentGeneration(hash, state)) // student has not evaluated it yet and it is in current generation 
				{					
					pooledProblet.add(problet);				
				}
			}
			if (!pooledProblet.isEmpty())
				probletId = pooledProblet.get(mtf.nextInt(pooledProblet.size()));			
		}
		
		else    //Exploitation
		{
			double maxScore = -1.0;
			for (int problet = 0; problet <probletSize; problet++) 
			{
				int hash = uniqueGenotypeHolder.get(problet);
				if (interaction[studentIndex][problet] == 0 && isInCurrentGeneration(hash, state)) // the problet is not evaluated yet and in the current generation
				{
					double probletScore = getAvgMove (problet);					
					if (probletScore > maxScore) //Find out the harderst test - promising candidate here 
					{ 
						maxScore =  probletScore;
						probletId = problet;
					}
				}										
			}					 		
		  }
		return probletId;	
	}
	private int getSelectedProblet( int studentID, final EvolutionState state) 
	{
		if (mtf.nextDouble() <= probComp)   
		{
			return getProbletCompleteness(studentID, state); 
		}
		else 
		{			
			return getProbletFatigue(studentID, state); 		
		}	
	}	

private void solve(int problet, int student)
{
	interaction[student][problet] = mtf.nextInt(popSize) + 1  ; // a random number of move
}

private void checkStatus(final EvolutionState state, int hash)
{
	for (int i = 0; i < popSize; i++)
	{
	  IntegerVectorIndividual parent = (IntegerVectorIndividual)state.population.subpops[PROBLEM_SUBPOP_INDEX].individuals[i];
	  int pHash = getHash(parent);
	  IntegerVectorIndividual child = (IntegerVectorIndividual)childs[i];
	  int cHash = getHash(child);
		
	  
	  if (hash == pHash || hash == cHash)  
		{
		  int parentPos = uniqueGenotypeHolder.indexOf(pHash);
		  int childPos = uniqueGenotypeHolder.indexOf(cHash);
		  
		  List<Integer> commonEvals = new ArrayList<Integer>();
		  
		  for (int student = 0; student < STUDENT; student++)
		  {
			  if (interaction[student][parentPos] > 0 && interaction[student][childPos] > 0)
			  {
				  commonEvals.add(student); 
			  }	  
		  }
		  
		  if (commonEvals.size() < minimumEvaluation)
		  {
			  System.out.println("Still parent and child are not qualified for Pareto Comparision");
		  }
		  
		  else
		  {
			  evaluationStatus[i] = true;
			  double [] pOutcome = new double[commonEvals.size()];
			  double [] cOutcome = new double[commonEvals.size()];
			  
			  for (int j = 0; j < commonEvals.size(); j++)
			  {
				  pOutcome[j] = interaction[commonEvals.get(j)][parentPos];
				  cOutcome[j] = interaction[commonEvals.get(j)][childPos];
			  }
			  if (!ParetoDominate(cOutcome, pOutcome)) //child does not dominate. So set its genome the original
			  {
				  child.setGenome(parent.genome);
			  }
		  } 		
	   }
    }
}

private boolean ParetoDominate (double [] scoresMe, double [] scoresOther )  
{
	boolean MeDominant = false;
	for (int i = 0; i < scoresMe.length; i++)   
	{
		if (scoresMe[i] > scoresOther[i])
			MeDominant = true;
		else if (scoresMe[i] < scoresOther[i])
			return false;
	}
	return MeDominant;
}


	public void finishProducing(final EvolutionState state,
			final int subpopulation,
			final int thread)
	{
		if (subpopulation == PROBLEM_SUBPOP_INDEX)
		{:q
			while(true)
			{
				if (allAreEvaluated())
					 break;
				  int student = mtf.nextInt(STUDENT);
				  int recommendedProblet = getSelectedProblet(student, state);
				  if (recommendedProblet != -1)
				  {
				    solve(recommendedProblet, student);	
				    int myHash = uniqueGenotypeHolder.get(recommendedProblet);
				    checkStatus(state, myHash);
				  }
			}
			
			int totalCell = STUDENT*uniqueGenotypeHolder.size();
			int fill = 0, hole = 0;
			for (int i = 0; i < STUDENT; i++)
			{
				for (int j = 0; j < uniqueGenotypeHolder.size(); j++)	
					if (interaction[i][j] > 0)
						fill++;	
			}
			
			double sparsity = 1.0 - fill/(totalCell * 1.0);
			F_SPARSITY = "job." + Integer.toString(currentJob) + "."+ F_SPARSITY;	
			try
			{
			  BufferedWriter bw  = new BufferedWriter(new FileWriter(F_SPARSITY, true));
			  bw.write(Double.toString(sparsity) + " " + Integer.toString(uniqueGenotypeHolder.size()));			
			  bw.newLine();									
			  bw.close();
			}catch(IOException e)
			{
				e.printStackTrace();
			}
		}
		
		for(int x=0;x<sources.length;x++) 
			if (x==0 || sources[x]!=sources[x-1])
				sources[x].finishProducing(state,subpopulation,thread);		
	}	
	private boolean allAreEvaluated() 
	{		
		for (int i = 0; i <popSize; i++)
			if (!evaluationStatus[i]) 
				return false;		
		return true;
	} 

}


