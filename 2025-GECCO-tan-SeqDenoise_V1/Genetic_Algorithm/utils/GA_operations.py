from numpy.random import randint
from numpy.random import rand

import Parameters as param

# tournament selection
def selection(pop, scores, ascending=False, k=2): ### k = how many chosen to be in the tournament
    # first random selection
    selection_ix = randint(len(pop))
    # second random selection
    ix = randint(len(pop))
    
    while selection_ix == ix:
        ix = randint(len(pop))
        
    ### Silhouette Score 
    if scores[ix] > scores[selection_ix]:
        selection_ix = ix
               
    return pop[selection_ix]

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    p_random = rand(len(p1))
    for i in range(len(p_random)):
        # check for recombination
        # Uniform crossover
        if p_random[i] < r_cross:
            temp = c1[i]
            c1[i] = c2[i]
            c2[i] = temp
            
    return [c1, c2]

# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

def GA_operation(p, s):
    selected = [selection(p, s, True) for _ in range(param.N_POP)]  

    children = []

    for i in range(0, param.N_POP, 2):
        # get selected parents in pairs
        p1, p2 = selected[i], selected[i+1]

        for c in crossover(p1, p2, param.R_CROSS):

            # mutation
            mutation(c, param.R_MUT)

            # store for next generation
            children.append(c)

    # replace population
    p = p + children

    return p