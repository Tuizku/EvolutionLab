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
        self.gens_data = []
        self.last_survived_genomes = None
    
    def run_generation(self, genomes = None, new_gen = True, return_steps_data = False, debug = False):
        if new_gen == True:
            self.gen += 1

        gen_data = {
            "genomes": None,
            "survived": 0,
            "diversity": 0
        }

        # Get the genomes for this generation (if genomes haven't been imported)
        # [Gen 0] genomes are random
        # [Gen 1+] genomes are crossovered
        if genomes == None:
            if self.gen == 0:
                genomes = self.dna.random_genomes(self.population)
            else:
                genomes = self.dna.crossover(self.last_survived_genomes, self.population)
        
        # Create the new generation and run it
        generation = Generation(genomes, self.dna, self.world_size, self.population, self.steps_per_gen)
        generation.run(return_steps_data, debug)

        # Get survived creatures genomes and save them to the lab. So the next gen can use these as parens.
        if new_gen == True:
            self.last_survived_genomes = generation.get_selection_genomes(self.selection_criteria)
            gen_data["genomes"] = genomes
            gen_data["survived"] = len(self.last_survived_genomes)
            gen_data["diversity"] = self.dna.average_hamming_distance(genomes)
            
            self.gens_data.append(gen_data)

        if return_steps_data == True:
            return generation.steps_data
    
    def run_generations(self, count : int):
        start_time = time.time()

        for i in range(count):
            self.run_generation()
            print(f"[{int(time.time() - start_time)}s / gen {self.gen}] survived = {len(self.last_survived_genomes)}")