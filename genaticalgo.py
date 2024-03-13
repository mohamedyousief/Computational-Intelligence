import random

def generate_chromosome (length):
    chromosome=[]
    for i in range(length):
        chromosome.append(random.randint(0,1))
    return chromosome


def generate_population (population_size , chromosome_length ):
    population=[]
    for i in range(population_size):
        population.append(generate_chromosome(chromosome_length))
    return population

def eveluate_fitness(population):
    fitness=[]
    for i in population:
        fitness.append(sum(i))
    return fitness

def pi(fitness):
    total_fitness = sum(fitness)
    probabilities = [fit / total_fitness for fit in fitness]
    return probabilities

def  cumulative(probabilities):
    cumulative_probs = []
    cumulative_prob = 0
    for prob in probabilities:
        cumulative_prob += prob
        cumulative_probs.append(cumulative_prob)
    return cumulative_probs

def one_point_crossover (perant1,perant2,pCross):
    if random.random()<pCross:
        cross_point=random.randint(1 , len(perant1)-1)
        child1=perant1[:cross_point]+perant2[cross_point:]
        child2=perant2[:cross_point]+perant1[cross_point:]
        return child1,child2
    else:
        return perant1,perant2
    

def bit_flip_mutation(individual, p_mut):
    mutated_individual = individual.copy()
    for i in range(len(mutated_individual)):
        if random.random() < p_mut:
            mutated_individual[i] = 1 - mutated_individual[i]
    return mutated_individual

def select_individual(cumulative_probs):
    r = random.random()
    for i, cum_prob in enumerate(cumulative_probs):
        if r <= cum_prob:
            return i
    print("Error: No individual selected!")
    return None


def genetic_algorithm(population_size, num_generations, chromosome_length, p_cross, p_mut):
    best_hist = []
    population = generate_population(population_size, chromosome_length)

    for generation in range(num_generations):
        fitness = eveluate_fitness(population)
        best_hist.append(max(fitness))
        
        elite_indices = sorted(range(len(fitness)), key=lambda k: fitness[k])[-2:]
        elite = [population[i] for i in elite_indices]

        probabilities = pi(fitness)
        cumulative_probs = cumulative(probabilities)

        new_population = elite.copy()

        for i in range((population_size - 2) // 2):
            parent1_i =select_individual(cumulative_probs)
            parent2_i =select_individual(cumulative_probs)
            parent1 = population[parent1_i]
            parent2 = population[parent2_i]
            child1,child2=one_point_crossover(parent1, parent2, p_cross)
            child1 = bit_flip_mutation(child1, p_mut)
            child2 = bit_flip_mutation(child2, p_mut)
            new_population.extend([child1, child2])
        population = new_population

    avg_fitness = sum(eveluate_fitness(population)) / population_size
    return population, best_hist, avg_fitness
 

random.seed(123) 
population_size = 20
num_generations = 100
chromosome_length = 5
p_cross = 0.6
p_mut = 0.05
population, best_hist, avg_fitness = genetic_algorithm(population_size, num_generations, chromosome_length, p_cross, p_mut)
print("Final Population:")
for chromosome in population:
    print(chromosome)
print("\nBest Fitness History:")
print(best_hist)
print("\nAverage Fitness Value:")
print(avg_fitness)