import time
from dna import DNA
from generation import Generation

class Lab:
    def __init__(self, dna : DNA, selection_criteria : list, world_size : int = 32, population : int = 128, steps_per_gen : int = 128):
        # Setup Lab's variables
        self.dna : DNA = dna
        self.selection_criteria : list = selection_criteria
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen

        self.gen : int = -1
        self.gens_genomes = []
        self.last_survived_genomes = None
    
    def run_generation(self, return_steps_data = False):
        self.gen += 1

        # Get the genomes for this generation
        # [Gen 0] genomes are random
        # [Gen 1+] genomes are crossovered
        gen_genomes = None
        if self.gen == 0:
            gen_genomes = self.dna.random_genomes(self.population)
        else:
            gen_genomes = self.dna.crossover(self.last_survived_genomes, self.population)
        self.gens_genomes.append(gen_genomes)
        
        # Create the new generation and run it
        generation = Generation(gen_genomes, self.dna, self.world_size, self.population, self.steps_per_gen)
        generation.run(return_steps_data)

        # Get survived creatures genomes
        self.last_survived_genomes = generation.get_selection_genomes(self.selection_criteria)

        if return_steps_data == True:
            return generation.steps_data
    
    def run_generations(self, count : int):
        start_time = time.time()

        for i in range(count):
            self.run_generation()
            print(f"[{int(time.time() - start_time)}s / gen {self.gen}] survived = {len(self.last_survived_genomes)}")