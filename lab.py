from dna import DNA

class Lab:
    def __init__(self, dna : DNA, world_size : int = 32, population : int = 128, steps_per_gen : int = 128):
        # Setup Lab's variables
        self.dna : DNA = dna
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen
    
    def run_generation(self):
        pass