package iccit18;

import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Scanner;

import ec.EvolutionState;
import ec.Evolve;
import ec.util.Output;
import ec.util.ParameterDatabase;

public class StartECJ {

	private static int numJobs = 2;//TODO - put it in param files
	private static EvolutionState evolState = null;
	private static String ECJ_PARAMS ;  //TODO - from config file
	private static final String NSGA3 = "nsga3";
	private static  final String PHCP = "phcp"; 
	
	private static String selectParamFile (String AlgorihtmName) {
		if (AlgorihtmName.compareToIgnoreCase(NSGA3) == 0)
			ECJ_PARAMS = "NSGA3.params";
		else if (AlgorihtmName.compareToIgnoreCase(PHCP) == 0)
			ECJ_PARAMS = "PHCP.params";
		return ECJ_PARAMS;
	}
	
	public static void main(String[] args) {
		ParameterDatabase params = null;	
		Scanner input = new Scanner(System.in);
		System.out.println("Enter Algorihtm Name nsga3/phcp?");
		String algoName = input.nextLine();
		File ecjParamFile = Paths.get(selectParamFile(algoName)).toFile().getAbsoluteFile();
	    input.close();
		try {
			 params =  new ParameterDatabase(ecjParamFile);
	     } catch (IOException e)  {
	       System.out.print("Error in creating parameter database: " +e.getMessage());
	       System.exit(1);
	     }
	        for (int job = 0; job < numJobs; job++) {
	        	
		        Output out = Evolve.buildOutput();
		        evolState = Evolve.initialize(params, job, out);
		        evolState.output.systemMessage("Job: " + job);
                evolState.job = new Object[1];                                  
                evolState.job[0] = Integer.valueOf(job);                    
                evolState.runtimeArguments = args;                              
                if (numJobs > 1){
                    String jobFilePrefix = "job." + job + ".";
                    evolState.output.setFilePrefix(jobFilePrefix);     
                    evolState.checkpointPrefix = jobFilePrefix + evolState.checkpointPrefix;  
                    }
		        evolState.run(EvolutionState.C_STARTED_FRESH);
	            Evolve.cleanup(evolState);
	        }
		}		
	
 }
