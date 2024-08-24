from dna import DNA
from generation import Generation

class Lab:
    def __init__(self, dna : DNA, world_size : int = 32, population : int = 128, steps_per_gen : int = 128):
        # Setup Lab's variables
        self.dna : DNA = dna
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen

        self.gen : int = -1
    
    def run_generation(self, return_steps_data = False):
        self.gen += 1

        # Get the genomes for this generation
        # [Gen 0] genomes are random
        # [Gen 1+] genomes are crossovered
        gen_genomes = None
        if self.gen == 0:
            gen_genomes = self.dna.random_genomes(self.population)
        else:
            print("crossover not implemented!")
            return
        
        # Create the new generation
        generation = Generation(gen_genomes, self.dna, self.world_size, self.population, self.steps_per_gen)
        generation.run(return_steps_data)

        if return_steps_data == True:
            return generation.steps_data