import numpy as np
import copy
import time
from lab.bytedna import ByteDNA
from lab.creature import Creature

class Generation:
    def __init__(self, genomes, bytedna : ByteDNA, world_size : int, population : int, steps_per_gen : int):
        # Setup Generation's variables
        self.genomes : list = genomes
        self.bytedna : ByteDNA = bytedna
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen
        self.map = np.zeros(shape=(world_size, world_size), dtype=np.int8)

        self.steps_data = []
        
    
    def run(self, save_steps : bool = False, debug : bool = False):
        start_time = time.time()

        # Create the creatures
        self.creatures = []
        genomes_list = self.bytedna.get_separated_genomes(self.genomes)
        for genome in genomes_list:
            x, y = self.get_empty_pos()
            data = {
                "x": x,
                "y": y
            }
            self.creatures.append(Creature(data, genome, self.bytedna, self))
        
        setup_time = time.time() - start_time
        start_time = time.time()

        # Run through the steps
        for step in range(self.steps_per_gen):
            for creature in self.creatures:
                creature.update()
            
            if save_steps == True:
                self.steps_data.append({"map": copy.deepcopy(self.map)})
        
        # Debug time (if enabled)
        steps_time = time.time() - start_time
        if debug == True:
            print(f"GEN DEBUG -> setup_time = {round(setup_time, 6)}, steps_time = {round(steps_time, 6)}")
            

    def get_selection_genomes(self, selection_criteria : list):
        result_genomes = bytearray()
        
        # Loop through all creatures and adds the creatures that match the criteria to the result list.
        for creature in self.creatures:
            data = creature.data
            survives = True

            # Put all names from criteria into a list.
            criteria_names = []
            for criterion in selection_criteria:
                if not criterion["name"] in criteria_names: criteria_names.append(criterion["name"])

            for name in criteria_names:
                matches_criterion = True
                name_criteria = [criterion for criterion in selection_criteria if criterion["name"] == name]
                for criterion in name_criteria:
                    operator = criterion["operator"]
                    value = criterion["value"]

                    # Check if creature survives by the operator that is being used
                    if operator == "=":
                        if data[name] != value: matches_criterion = False
                    elif operator == "<":
                        if data[name] >= value: matches_criterion = False
                    elif operator == ">":
                        if data[name] <= value: matches_criterion = False

                survives = matches_criterion
                if survives == False: break
            
            # Creature's genome is added to the result, IF it survives.
            if survives == True:
                result_genomes.extend(creature.genome)
        
        return result_genomes



    def get_empty_pos(self):
        # Tries 10 000 times to find an empty random pos from map.
        for i in range(10000):
            x = np.random.randint(0, self.world_size)
            y = np.random.randint(0, self.world_size)
            if self.map[x][y] == 0:
                return x, y
        
        print("no empty pos found after 10 000 iterations.")
        return -1, -1

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
