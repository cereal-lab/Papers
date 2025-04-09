from numpy.random import randint

from utils.objectives import fitness
import utils.config_utils as utils

### Systems
import time
import multiprocessing
from functools import partial
import random
from numpy.random import rand
import pandas as pd



class NSGA2:
    """A class to implement the NSGA-II multi-objective optimization algorithm"""

    def __init__(self, generation = 30, pop_size = 30, p_crossover = 0.5, alpha = 0.05, p_mutation = 0.5, n_lr_iter = 1000):
        """Constructor for the NSGA-II object"""
        self.generation = generation
        self.pop_size = pop_size
        self.p_crossover = p_crossover
        self.alpha = alpha
        self.p_mutation = p_mutation
        self.n_lr_iter = n_lr_iter


    def run(self, problem):
        """Runs the NSGA-II algorithm on a given problem."""

        # Extract Problem Info
        obj1 = 0 if problem['obj1'] == 'sil_score' else 1 if problem['obj1'] == 'reg_acc' else 2 
        obj2 = 0 if problem['obj2'] == 'sil_score' else 1 if problem['obj2'] == 'reg_acc' else 2 
        n_bits = problem['n_bits']


        # Preparing the df
        df = pd.read_csv(problem['file_input'])

        # Load existing cache
        # cache = utils.load_cache(problem)
        cache = {}
        cache = {int(key): value for key, value in cache.items()}

        # Dictionary to store every gen info
        gen_info = {}

        # Individual representation
        class Individual:
            def __init__(self, genotype):
                self.genotype = genotype
                self.genotype_dec = utils.convert_to_decimal(genotype)
                self.objectives = None
                self.rank = None
                self.crowding_distance = None
        
        # Print parameters
        utils.print_parameters(self, problem)

        # initial population
        pop = [randint(0, 2, n_bits).tolist() for _ in range(self.pop_size)]

        # search space
        search_space = set()

        for gen in range(self.generation+1):
            ts_before = time.time() 
            # record search space
            curGen_search_space = len(search_space)

            # calculating the fitness of each cleaning encode in parallel
            with multiprocessing.Pool(processes=15) as pool:
                combined_args = partial(fitness, df, problem, cache)
                result = pool.map(combined_args, pop)

            # Build the cache & search space
            for res in result:
                if int(res[0]) not in search_space:
                    search_space.add(int(res[0]))

                if int(res[0]) not in cache:
                    cache[int(res[0])] = res[1]
            
                # print(f"GENE: {res[0]} --- {res[1]}")
            
            # Choose the objectives 
            result = [(item[0], [item[1][obj1], item[1][obj2]]) for item in result]
            
            #####################################
            # Create a list of Individual objects
            individuals_list = [Individual(utils.convert_to_binary(genotype, problem['n_bits'])) for genotype, _ in result]

            # Set the objectives attribute for each Individual object
            for individual, (_, objectives) in zip(individuals_list, result):
                individual.objectives = objectives

            # Print the list of Individual objects
            # for individual in individuals_list:
            #     print(f"Genotype: {individual.genotype}, Genotype_DEC: {individual.genotype_dec}, Objectives: {individual.objectives}")
            #####################################
                
            # Non-dominated sorting
            fronts = fast_nondominated_sort(individuals_list)

            # Select individuals for the next generation based on crowding distance
            new_population = []
            remaining_size = self.pop_size
            i = 0

            while remaining_size > 0 and i < len(fronts) and fronts[i]:
                if len(fronts[i]) <= remaining_size:
                    new_population.extend(fronts[i])
                    remaining_size -= len(fronts[i])
                else:
                    # print("TRIGGER!!!!")
                    fronts[i] = crowding_distance_sort(fronts[i])
                    new_population.extend(fronts[i][:remaining_size])
                    remaining_size = 0

                i += 1

            pop = new_population

            # Print result
            time_usage = utils.duration_checking(ts_before)

            pareto_front = [ind for ind in pop if ind.rank == 0]
            pareto_front_dict = {ind.genotype_dec: (ind.objectives, ind.rank) for ind in pareto_front}
            pareto_front_genenotype = list(pareto_front_dict.keys())
            
            ## Calculate the average of pareto front
            # Transpose the values to get lists for each index
            transposed_values = zip(*[value[0] for value in pareto_front_dict.values()])
            # Calculate the average for each index
            average_values = [sum(column) / len(column) for column in transposed_values]
            ##

            # num_search_space = len(search_space) - curGen_search_space

            ## Record every gen info
            gen_info[gen] = [len(search_space), average_values[0], average_values[1], pareto_front_genenotype]

            print(f'Gen-{gen}, {problem["obj1"]}: {average_values[0]:.4f}, {problem["obj2"]}: {average_values[1]:.2f}, Time: {time_usage}s')
            for key, value in pareto_front_dict.items():
                print(f'                                            Gene: {key}, [{problem["obj1"]}: {value[0][0]:.4f} | {problem["obj2"]}: {value[0][1]:.2f}], Rank: {value[1]}')


            if (gen+1) > self.generation:
                # Save the updated cache
                # utils.save_cache(cache, problem)
                
                return pareto_front_dict, gen_info


            offspring = GA_operation(self, pop)

            # Convert individual genetype into list
            new_pop = []
            for i in pop:
                new_pop.append(i.genotype)    
            pop = new_pop

            # combine population with offspring
            pop += offspring

            # Remove duplicates 
            unique_pop = list(map(tuple, set(map(tuple,pop))))
            while len(unique_pop) < (self.pop_size*2):
                unique_pop.append(randint(0, 2, n_bits).tolist())
            pop = unique_pop
            ##

            # ############################## population checking
            # # Apply the function to every list inside the nested list
            # result = [utils.convert_to_decimal(sublist) for sublist in pop]
            # # Use Counter to count occurrences of each element
            # element_counts = Counter(result)
            # # Filter elements with count greater than 1 (duplicates)
            # duplicates = {element: count for element, count in element_counts.items() if count > 1}
            # # Print the count of common elements
            # print(f'                                                                                There are {len(duplicates)} numbers with duplicates.')
            # print(f'                                                                                {duplicates}')
            # ############################## population checking

        
def fast_nondominated_sort(population):
    fronts = [[]]
    dominated_count = dict()
    dominating = dict()

    for ind1 in population:
        dominated_count[ind1] = 0
        dominating[ind1] = set()

        for ind2 in population:
            if ind1 == ind2:
                continue

            if all(obj1 >= obj2 for obj1, obj2 in zip(ind1.objectives, ind2.objectives)):
                dominating[ind1].add(ind2)
            elif all(obj1 <= obj2 for obj1, obj2 in zip(ind1.objectives, ind2.objectives)):
                dominated_count[ind1] += 1

        if dominated_count[ind1] == 0:
            ind1.rank = 0
            fronts[0].append(ind1)

    i = 0
    while fronts[i]:
        next_front = []

        for ind1 in fronts[i]:
            for ind2 in dominating[ind1]:
                dominated_count[ind2] -= 1

                if dominated_count[ind2] == 0:
                    ind2.rank = i + 1
                    next_front.append(ind2)

        i += 1
        fronts.append(next_front)

    return fronts

def crowding_distance_assignment(front):
    n = len(front)
    distances = [0] * n

    for obj_index in range(len(front[0].objectives)):
        front.sort(key=lambda ind: ind.objectives[obj_index])

        distances[0] = distances[n - 1] = float('inf')

        for i in range(1, n - 1):
            distances[i] += front[i + 1].objectives[obj_index] - front[i - 1].objectives[obj_index]

    for ind, distance in zip(front, distances):
        ind.crowding_distance = distance

def crowding_distance_sort(fronts):
    sorted_population = []

    crowding_distance_assignment(fronts)
    sorted_population.extend(fronts)

    sorted_population.sort(key=lambda ind: (ind.rank, -ind.crowding_distance))

    return sorted_population

def GA_operation(self, pop):
    offspring = []
    generated_offspring = set()  # Use a set to keep track of generated offspring

    while len(offspring) < self.pop_size:
        if len(pop) >= 2:
            # Tournament selection for parent 1
            p1 = tournament_selection(pop)
            
            # Tournament selection for parent 2
            p2 = tournament_selection(pop)

        for c in crossover(p1, p2, self.p_crossover):
            mutation(c, self.p_mutation)

            # Check for duplicate offspring before adding to the list
            offspring_key = tuple(c)  # Assuming 'c' is a list or tuple
            if offspring_key not in generated_offspring:
                offspring.append(c)
                generated_offspring.add(offspring_key)

                # Break out of the loop if the desired population size is reached
                if len(offspring) == self.pop_size:
                    break
    
    return offspring

def tournament_selection(pop, tournament_size=3):
    participants = random.sample(pop, tournament_size)
    participants = crowding_distance_sort(participants)

    winner = min(participants, key=lambda ind: (ind.rank, -ind.crowding_distance))

    return winner

# crossover operation
def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.genotype.copy(), p2.genotype.copy()
    p_random = rand(len(p1.genotype))
    for i in range(len(p_random)):
        # check for recombination
        # Uniform crossover
        if p_random[i] < r_cross:
            temp = c1[i]
            c1[i] = c2[i]
            c2[i] = temp
            
    return [c1, c2]

# mutation operation
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

