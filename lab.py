import os
import json
import time
from dna import DNA
from generation import Generation

class Lab:
    def __init__(self, dna : DNA, selection_criteria : list, 
                 world_size : int = 32, population : int = 128, steps_per_gen : int = 128,
                 gens_per_save : int = 100,
                 name : str = "default", 
                 path : str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")):
        
        # Setup Lab's variables.
        self.dna : DNA = dna
        self.selection_criteria : list = selection_criteria
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen
        self.gens_per_save : int = gens_per_save

        # Setup Lab Generations variables.
        self.gen : int = -1
        self.last_survived_genomes = None
        self.unsaved_gens_data = []

        # Setup path and directories for the lab "project".
        self.path = os.path.join(path, name)
        os.makedirs(self.path, exist_ok=True)

        self.try_load_lab()
    

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
            self.unsaved_gens_data.append(gen_data)

            if len(self.unsaved_gens_data) >= self.gens_per_save:
                self.save_gens()

        if return_steps_data == True:
            return generation.steps_data
    
    def run_generations(self, count : int):
        start_time = time.time()

        for i in range(count):
            self.run_generation()
            print(f"[{int(time.time() - start_time)}s / gen {self.gen}] survived = {len(self.last_survived_genomes)}")
        
        self.save_gens()
    


    def try_load_lab(self):
        gens_path = os.path.join(self.path, "gens.json")

        if os.path.isfile(gens_path):
            gens_data = self.load_gens()
            self.gen = len(gens_data) - 1
            self.last_survived_genomes = gens_data[-1]["genomes"]

    def save_gens(self):
        start_time = time.time()
        filepath = os.path.join(self.path, "gens.json")

        # Creates the file if it doesn't exist.
        if not os.path.isfile(filepath):
            open(filepath, "x")
        
        # Open the file for reading + writing
        with open(filepath, "r+") as file:
            # Load old data if there is.
            gens = [] 
            content = file.read()
            if content != "":
                gens = json.loads(content)

            # Extend old data with new, and write it to the beginning of the file.
            gens.extend(self.unsaved_gens_data)
            file.seek(0)
            file.write(json.dumps(gens))
            file.truncate() # Clears possible old data, if write length was smaller than the original file length.
        
        self.unsaved_gens_data = []
        print(f"save_time = {time.time() - start_time}")

    def load_gens(self):
        # Save if there are gens not saved
        if len(self.unsaved_gens_data) > 0:
            self.save_gens()
        
        # Load the file into an object and return it.
        result = None
        filepath = os.path.join(self.path, "gens.json")
        with open(filepath, "r") as file:
            content = file.read()
            result = json.loads(content)
        
        return result
