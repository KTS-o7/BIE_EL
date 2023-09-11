import random

POPULATION_SIZE = 200
TARGET = "Hello, world!"
MUTATION_RATE = 0.01

def generate_random_string(length):
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.!") for _ in range(length)])

def calculate_fitness(string):
    score = 0
    for i in range(len(TARGET)):
        if string[i] == TARGET[i]:
            score += 1
    return score / len(TARGET)

def crossover(parent1, parent2):
    midpoint = random.randint(0, len(parent1))
    child = parent1[:midpoint] + parent2[midpoint:]
    return child

def mutate(string):
    mutated_string = ""
    for char in string:
        if random.random() < MUTATION_RATE:
            mutated_string += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.!")
        else:
            mutated_string += char
    return mutated_string

def create_initial_population():
    population = []
    for i in range(POPULATION_SIZE):
        string = generate_random_string(len(TARGET))
        population.append(string)
    return population

def evolve_population(population):
    new_population = []
    fitness_scores = [calculate_fitness(string) for string in population]
    for i in range(POPULATION_SIZE):
        parent1 = random.choices(population, weights=fitness_scores)[0]
        parent2 = random.choices(population, weights=fitness_scores)[0]
        child = crossover(parent1, parent2)
        child = mutate(child)
        new_population.append(child)
    return new_population

import pygame
import sys

WIDTH = 800
HEIGHT = 600
FONT_SIZE = 32
FONT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, FONT_SIZE)

def draw_string(string, x, y):
    text = font.render(string, True, FONT_COLOR)
    screen.blit(text, (x, y))

population = create_initial_population()
generation = 1
best_string = ""
best_fitness = 0

while True:
    screen.fill(BACKGROUND_COLOR)
    draw_string("Generation: {}".format(generation), 10, 10)

    for i, string in enumerate(population):
        fitness = calculate_fitness(string)
        if fitness > best_fitness:
            best_fitness = fitness
            best_string = string

        draw_string(string, 10, FONT_SIZE * (i + 2))
        draw_string("{:.2f}%".format(fitness * 100), WIDTH - 100, FONT_SIZE * (i + 2))

    draw_string("Best string: {}".format(best_string), 10, HEIGHT - FONT_SIZE * 2)
    draw_string("Best fitness: {:.2f}%".format(best_fitness * 100), 10, HEIGHT - FONT_SIZE)

    pygame.display.update()

    population = evolve_population(population)
    generation += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
