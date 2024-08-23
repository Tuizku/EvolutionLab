import numpy as np
from dna import DNA
from creature import Creature

class Generation:
    def __init__(self, genomes, dna : DNA, world_size : int, population : int, steps_per_gen : int):
        # Setup Generation's variables
        self.genomes : list = genomes
        self.dna : DNA = dna
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen
        self.map = np.zeros(shape=(world_size, world_size), dtype=np.int8)
        
    
    def run(self):
        # Create the creatures
        creatures = []
        for genome in self.genomes:
            creatures.append(Creature(genome, self.dna, self))
        
        # Run through the steps
        # ...



    def is_pos_in_bounds(self, x, y):
        """Returns true if the position was in bounds of the map."""
        if x < 0 or x >= self.world_size or y < 0 or y >= self.world_size:
            return False
        return True

    def change_pos(self, x, y, x_change, y_change):
        """Returns true if the position was able to be changed."""
        new_x = x + x_change
        new_y = y + y_change

        # Changes position IF (1. the new pos is in bounds) AND (2. the new pos doesn't have the value 1)
        if self.is_pos_in_bounds(new_x, new_y) and self.map[new_x][new_y] != 1:
            self.map[new_x][new_y] = 1
            self.map[x][y] = 0
            return True
        else:
            return False
