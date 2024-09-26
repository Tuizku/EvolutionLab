import os
import json
import time
from bytedna import ByteDNA
from generation import Generation

class Lab:
    def __init__(self, bytedna : ByteDNA, selection_criteria : list, 
                 world_size : int = 32, population : int = 128, steps_per_gen : int = 128,
                 gens_per_save : int = 100,
                 name : str = "default", 
                 path : str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")):
        
        # Setup Lab's variables.
        self.bytedna : ByteDNA = bytedna
        self.selection_criteria : list = selection_criteria
        self.world_size : int = world_size
        self.population : int = population
        self.steps_per_gen : int = steps_per_gen
        self.gens_per_save : int = gens_per_save

        # Setup Lab Generations variables.
        self.gen : int = -1
        self.last_survived_genomes = None
        self.unsaved_gens_genomes = bytearray()
        self.unsaved_gens_stats = []

        # Setup path and directories for the lab "project".
        self.path = os.path.join(path, name)
        os.makedirs(self.path, exist_ok=True)

        self.try_load_lab()
    

    def run_generation(self, genomes = None, new_gen = True, return_steps_data = False, debug = False):
        if new_gen == True:
            self.gen += 1

        gen_stats = {
            "survived": 0,
            "diversity": 0
        }

        # Get the genomes for this generation (if genomes haven't been imported)
        # [Gen 0] genomes are random
        # [Gen 1+] genomes are crossovered
        if genomes == None:
            if self.gen == 0:
                genomes = self.bytedna.random_genomes(self.population)
            else:
                genomes = self.bytedna.crossover(self.last_survived_genomes, self.population)
        
        # Create the new generation and run it
        generation = Generation(genomes, self.bytedna, self.world_size, self.population, self.steps_per_gen)
        generation.run(return_steps_data, debug)

        # Get survived creatures genomes and save them to the lab. So the next gen can use these as parens.
        if new_gen == True:
            self.last_survived_genomes = generation.get_selection_genomes(self.selection_criteria)
            
            gen_stats["survived"] = len(self.bytedna.get_separated_genome(self.last_survived_genomes))
            gen_stats["diversity"] = self.bytedna.average_hamming_distance(genomes, self.population)
            self.unsaved_gens_stats.append(gen_stats)
            self.unsaved_gens_genomes.extend(genomes)

            if len(self.unsaved_gens_stats) >= self.gens_per_save:
                self.save_gens()

        if return_steps_data == True:
            return generation.steps_data
    
    def run_generations(self, count : int):
        start_time = time.time()

        for i in range(count):
            self.run_generation()
            print(f"[{int(time.time() - start_time)}s / gen {self.gen}] survived = {round(len(self.last_survived_genomes) / (self.bytedna.genome_len * self.bytedna.gene_bytes))}")
        
        self.save_gens()
    


    def try_load_lab(self):
        gens_filepath = os.path.join(self.path, "gens.bin")
        stats_filepath = os.path.join(self.path, "stats.json")

        if os.path.isfile(gens_filepath) and os.path.isfile(stats_filepath):
            gens, stats = self.load_gens()
            self.gen = len(stats) - 1
            self.last_survived_genomes = gens[-(self.bytedna.gene_bytes * self.bytedna.genome_len * self.population):]

    def save_gens(self):
        start_time = time.time()
        gens_filepath = os.path.join(self.path, "gens.bin")
        stats_filepath = os.path.join(self.path, "stats.json")

        # Creates the files if they do not exist.
        if not os.path.isfile(gens_filepath):
            open(gens_filepath, "xb")
        if not os.path.isfile(stats_filepath):
            open(stats_filepath, "x")
        
        # Open the gens file for appending binary
        with open(gens_filepath, "ab") as file:
            file.write(self.unsaved_gens_genomes)

        # Open the stats file for reading + writing
        with open(stats_filepath, "r+") as file:
            # Load old data if there is.
            gens_stats = [] 
            content = file.read()
            if content != "":
                gens_stats = json.loads(content)

            # Extend old data with new, and write it to the beginning of the file.
            gens_stats.extend(self.unsaved_gens_stats)
            file.seek(0)
            file.write(json.dumps(gens_stats))
            file.truncate() # Clears possible old data, if write length was smaller than the original file length.
        
        self.unsaved_gens_genomes = bytearray()
        self.unsaved_gens_stats = []
        print(f"save_time = {time.time() - start_time}")

    def load_gens(self):
        # Save if there are gens not saved
        if len(self.unsaved_gens_stats) > 0:
            self.save_gens()
        
        # Load the file into an object and return it.
        
        gens_filepath = os.path.join(self.path, "gens.bin")
        stats_filepath = os.path.join(self.path, "stats.json")

        gens : bytearray = None
        stats = None
        with open(gens_filepath, "rb") as file:
            gens = file.read()
        with open(stats_filepath, "r") as file:
            stats = json.loads(file.read())
        
        return gens, stats
