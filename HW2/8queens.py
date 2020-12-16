import numpy as np
import json

N = 8

def initialize():
    x = [i for i in range(N)]
    np.random.shuffle(x)
    return x

def crossover(x, y):
    #baby = x[:5] + y[5:] #- ONE CROSS POINT.
    # TWO CROSS POINT.
    i = np.random.randint(1, N) 
    j = np.random.randint(i)

    A = x.copy()
    B = y.copy()
    for n in x[j:i]:
        B.remove(n) 

    baby = B[:j] + x[j:i] + B[j:]
    return baby

def mutate(x):
    "Swap Queens."
    i = np.random.randint(N)
    j = np.random.randint(N)
    x[i], x[j] = x[j], x[i]
    return x

def fitness(member):
    attacks = 0

    # Rows
    numbers = {}
    for i in member:
        if i in numbers:
            numbers[i] += 1
        else:
            numbers[i] = 0

    for i in numbers:
        attacks += numbers[i]

    # Columns - Representation Avoids problem.

    # Diagonals going in \ direction.
    numbers = {}
    for i in range(len(member)):
        # Find the difference in column vs index.
        n = member[i] - i
        if n in numbers:
            numbers[n] += 1
        else:
            numbers[n] = 0

    for i in numbers:
        attacks += numbers[i]
    
    # Diagonals going in / direction.
    numbers = {}
    for i in range(len(member)):
        n = i + member[i]
        if n in numbers:
            numbers[n] += 1
        else:
            numbers[n] = 0

    for i in numbers:
        attacks += numbers[i]

    return attacks

def genetic_algo(MAX_TRIALS, POPSIZE):
    # Generate initial populations.
    population = [initialize() for _ in range(POPSIZE)]

    # Check if a solution has been found.
    sol_found = False

    # Create a dict for score keeping among generations.
    f_scores = {}

    for i in range(MAX_TRIALS): 
        # For each generation, initialize a few variables.
        tot_fit = 0
        scores = []
        new_population = []

        # For each member in the population, calculate fitness
            # crossover pop, and mutate. 
        for member in population:
            fit = fitness(member)
            scores.append(fit)
            if fit == 0:
                sol_found = True
            tot_fit += fit

        avg_fit = tot_fit / POPSIZE
        s_pop = [x for _,x in sorted(zip(scores, population))]

        for x in range(POPSIZE - 1):
            c_m = crossover(s_pop[x], s_pop[x+1])
            m_m = mutate(c_m)
            new_population.append(m_m)
        # Final case.
        c_m = crossover(s_pop[POPSIZE - 1], s_pop[0])
        m_m = mutate(c_m)
        new_population.append(m_m)


        f_scores[i] = [i, avg_fit, min(scores)]
        if sol_found:
            break
        population = new_population

    return f_scores


if __name__ == '__main__':
    """ 
    KNOWN SOLUTIONS
    print(fitness([4, 0, 7, 3, 1, 6, 2, 5]))
    print(fitness([2, 7, 3, 6, 0, 5, 1, 4]))
    a = [4, 0, 7, 3, 1, 6, 2, 5]
    b = [2, 7, 3, 6, 0, 5, 1, 4]
    """
    genetic_algo(20, 3)


    POP_SIZE = [5, 10, 50, 100, 500, 1000, 5000] # do we really want 1000 lol 
    MAX = [10, 100, 1000, 5000, 10000]
    #POP_SIZE = [5, 10]
    #MAX = [10, 50]
    data = {}
    for i in MAX:
        for j in POP_SIZE:
            print(i, j)
            data["{},{}".format(i, j)] = genetic_algo(i, j)
    with open('data.json', 'a') as dj:
        json.dump(data, dj, indent=4)


