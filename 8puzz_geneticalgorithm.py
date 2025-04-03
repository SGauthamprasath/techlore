import numpy as np
from enum import Enum
from random import randint

goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

class Direction(Enum):
    UP, RIGHT, DOWN, LEFT = 1, 2, 3, 4

def get_random_direction():
    return Direction(randint(1, 4))

class Puzzle:
    def __init__(self, board):
        self.puzzle = np.array(board).reshape(3, 3)

    def move(self, direction):
        x, y = np.argwhere(self.puzzle == 0)[0]
        if direction == Direction.UP and x > 0:
            self.puzzle[x, y], self.puzzle[x - 1, y] = self.puzzle[x - 1, y], self.puzzle[x, y]
        elif direction == Direction.RIGHT and y < 2:
            self.puzzle[x, y], self.puzzle[x, y + 1] = self.puzzle[x, y + 1], self.puzzle[x, y]
        elif direction == Direction.DOWN and x < 2:
            self.puzzle[x, y], self.puzzle[x + 1, y] = self.puzzle[x + 1, y], self.puzzle[x, y]
        elif direction == Direction.LEFT and y > 0:
            self.puzzle[x, y], self.puzzle[x, y - 1] = self.puzzle[x, y - 1], self.puzzle[x, y]

    def fitness(self):
        return np.sum(self.puzzle != goal)

    def _str_(self):
        return str(self.puzzle)

class Solver:
    def __init__(self, max_generations, population_size, board):
        self.max_generations = max_generations
        self.population_size = population_size
        self.board = board

    def create_chromosome(self):
        return [Direction(randint(1, 4)) for _ in range(20)]

    def initialize_population(self):
        return [self.create_chromosome() for _ in range(self.population_size)]

    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if randint(0, 1):
                chromosome[i] = Direction(randint(1, 4))

    def apply_chromosome(self, chromosome):
        puzzle = Puzzle(self.board)
        for direction in chromosome:
            puzzle.move(direction)
            if puzzle.fitness() == 0:
                return puzzle
        return puzzle

    def selection(self, population):
        return sorted(population, key=lambda p: self.apply_chromosome(p).fitness())[:3]

    def crossover(self, parent1, parent2):
        point = randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:]

    def solution(self):
        population = self.initialize_population()
        for generation in range(self.max_generations):
            population = self.selection(population)
            next_generation = []
            while len(next_generation) < self.population_size:
                parent1, parent2 = randint(0, 2), randint(0, 2)
                child = self.crossover(population[parent1], population[parent2])
                self.mutate(child)
                next_generation.append(child)
            population = next_generation
            best_puzzle = self.apply_chromosome(population[0])
            if best_puzzle.fitness() == 0:
                print(f"Solution found in generation {generation}:")
                print(best_puzzle.puzzle)
                return

initial_board = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]

print("Genetic Algorithm:\n---------------------------\n")
for i in initial_board:
    print(i)
print("---------------------------")

solver = Solver(1000, 20, initial_board)
solver.solution()
