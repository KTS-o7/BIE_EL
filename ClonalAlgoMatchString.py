import random
import matplotlib.pyplot as plt

class Antibody:
    def __init__(self, length):
        self.sequence = [random.choice(['A', 'C', 'G', 'T']) for _ in range(length)]
    
    def mutate(self, mutation_rate):
        for i in range(len(self.sequence)):
            if random.random() < mutation_rate:
                self.sequence[i] = random.choice(['A', 'C', 'G', 'T'])
    
    def evaluate_fitness(self, target):
        return sum([1 for i in range(len(target)) if self.sequence[i] == target[i]])
    
    def crossover(self, other):
        # implement crossover here
        pass

class Population:
    def __init__(self, size, length, mutation_rate, target):
        self.size = size
        self.length = length
        self.mutation_rate = mutation_rate
        self.target = target
        self.antibodies = [Antibody(length) for _ in range(size)]
        self.best_fitness = []
    
    def select_antibodies(self):
        fitness = self.evaluate_fitness()
        sorted_antibodies = sorted(zip(self.antibodies, fitness), key=lambda x: x[1], reverse=True)
        selected_antibodies = [antibody for antibody, _ in sorted_antibodies[:self.size // 2]]
        return selected_antibodies
    
    def generate_offspring(self):
        offspring = []
        for i in range(self.size):
            parent1 = random.choice(self.antibodies)
            parent2 = random.choice(self.antibodies)
            child = Antibody(self.length)
            for j in range(self.length):
                if random.random() < 0.5:
                    child.sequence[j] = parent1.sequence[j]
                else:
                    child.sequence[j] = parent2.sequence[j]
            offspring.append(child)
        return offspring
    
    def evaluate_fitness(self):
        fitness = [antibody.evaluate_fitness(self.target) for antibody in self.antibodies]
        self.best_fitness.append(max(fitness))
        return fitness
    
    def display_convergence(self):
        plt.plot(range(len(self.best_fitness)), self.best_fitness)
        plt.title('Convergence of Clonal Algorithm')
        plt.xlabel('Iteration')
        plt.ylabel('Best Fitness')
        plt.show()

    def run(self, iterations):
        for i in range(iterations):
            selected = self.select_antibodies()
            offspring = self.generate_offspring()
            for i in range(len(offspring)):
                offspring[i].mutate(self.mutation_rate)
            self.antibodies = selected + offspring
        self.display_convergence()

# example usage
pop = Population(50, 20, 0.1, 'AGCT' * 5)
pop.run(1000)
