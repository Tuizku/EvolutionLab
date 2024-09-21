import numpy as np
import random
import time

class ByteDNA:
    def __init__(self, 
                 inputs : list, outputs : list,
                 genome_len : int, gene_bytes : int, 
                 inner_neurons : int, mutation_interval : int,
                 source_id_len : int, sink_id_len : int, weight_len : int,
                 weight_range : float = 8.0):
        """
        Creates a new ByteDNA, an essential object for the lab.

        Parameters
        ----------
            inputs (list): Neuron functions that result inputs.
            outputs (list): Neuron functions that result an action.
            genome_len (int): Gene count per genome.
            gene_bytes (int): Amount of bytes that a single gene takes.
            inner_neurons (int): Count of inner neurons.
            mutation_interval (int): Probability of a mutation per gene (value 100 = 1/100 possibility).
            source_id_len (int): Bit count in source_id (Part of a gene).
            sink_id_len (int): Bit count in sink_id (Part of a gene).
            weight_len (int): Bit count in weight (Part of a gene).
            weight_range (float): Total distance that weight can differ (value 8.0 = -4.0 - 4.0).
        """

        # Setup basic properties
        self.inputs = inputs
        self.outputs = outputs

        self.genome_len = genome_len
        self.gene_bytes = gene_bytes
        self.gene_bits = gene_bytes * 8
        self.inner_neurons = inner_neurons
        self.mutation_interval = mutation_interval
        
        self.source_id_len = source_id_len
        self.sink_id_len = sink_id_len
        self.weight_len = weight_len

        self.weight_range = weight_range


        # Decode shifts
        self.source_type_shift = self.gene_bits - 1
        self.source_id_shift = self.gene_bits - 1 - self.source_id_len
        self.sink_type_shift = self.gene_bits - 1 - self.source_id_len - 1
        self.sink_id_shift = self.gene_bits - 1 - self.source_id_len - 1 - self.sink_id_len

        # Decode masks
        self.source_type_mask = 1
        self.source_id_mask = (1 << self.source_id_len) - 1
        self.sink_type_mask = 1
        self.sink_id_mask = (1 << self.sink_id_len) - 1
        self.weight_mask = (1 << self.weight_len) - 1

    


    # Functions that generate genomes.

    def random_genomes(self, amount):
        """Creates a bytearray that includes all of the new random genomes."""

        # Create a list of single byte numbers, then turn that list into a bytearray.
        bytes_amount = self.gene_bytes * self.genome_len * amount
        random_bytes = np.random.randint(0, 255, size=bytes_amount, dtype=np.uint8)
        return bytearray(random_bytes)

    def identical_genomes(self, genome : bytearray, population : int):
        """Turns a single genome into a whole population. This can be used as a test, but it's not used in the normal usage."""
        result = bytearray()
        for i in range(population): result.extend(genome)
        return result



    # Functions that change the genomes.

    def crossover(self, genomes : bytearray, population : int):
        """
        Between genes crossover, meaning that the inputted genomes are used as parents to create the children of the next generation.

        Returns the next generation's genomes as a bytearray.
        """
        
        # Calculate how many genomes are in the bytearray.
        survived = int(round(len(genomes) / self.gene_bytes / self.genome_len))

        # Result variable
        result_genomes = bytearray()


        # Shuffle the genomes
        separated_genomes = [genomes[i : i + (self.genome_len * self.gene_bytes)] for i in range(0, len(genomes), (self.genome_len * self.gene_bytes))]
        random.shuffle(separated_genomes)

        # If there is a single in the population, send it to the result, and pop it from the survivors.
        singles = survived % 2
        if singles == 1:
            result_genomes.extend(separated_genomes[-1])
            separated_genomes.pop()

        # Calculate parents (in couples) and needed children counts
        parents_count = survived - singles
        needed_children = population - singles

        # Calculate the children amounts per couple + how many will create an additional child
        children_per_couple = (needed_children / parents_count) * 2
        default_children_per_couple = int(np.floor(children_per_couple))
        additional_childs = int(np.round((children_per_couple - default_children_per_couple) * (parents_count * 0.5)))


        # Create the children by one parent couple at a time
        for parent_i in range(0, parents_count, 2):
            parent0 = separated_genomes[parent_i]
            parent1 = separated_genomes[parent_i + 1]
            
            # Calculate how many children this couple creates
            children_count = default_children_per_couple
            if additional_childs > 0:
                children_count += 1
                additional_childs -= 1
            
            # Create the children 2 offsprings at a time
            for child_i in range(0, children_count, 2):
                crossover_point = np.random.randint(self.genome_len)
                result_genomes.extend(parent0[:crossover_point * self.gene_bytes])
                result_genomes.extend(parent1[crossover_point * self.gene_bytes:])
                if child_i + 1 < children_count: # if child_id + 1 == 3 and children_count == 3, then it only creates the first offspring
                    result_genomes.extend(parent1[:crossover_point * self.gene_bytes])
                    result_genomes.extend(parent0[crossover_point * self.gene_bytes:])
            
        
        result_genomes_count = round(len(result_genomes) / self.genome_len / self.gene_bytes)
        if result_genomes_count < population:
            print(f"dna crossover resulted a smaller population ({result_genomes_count}/{population})")

        self.mutate(result_genomes)
        return result_genomes
    
    def mutate(self, genomes : bytearray):
        """Mutates the genomes, does not return anything."""
        
        genes_in_genomes = int(len(genomes) / self.gene_bytes)

        # Calculate mutation triggers, if trigger == 0, then a mutation happens.
        mutation_triggers = np.random.randint(0, self.mutation_interval, size=genes_in_genomes)
        for i in range(genes_in_genomes):
            if mutation_triggers[i] == 0:
                #print(f"{bin(int(genomes[i * gene_bytes]))} {bin(int(genomes[i * gene_bytes + 1]))} {bin(int(genomes[i * gene_bytes + 2]))}")
                byte_id = np.random.randint(0, self.gene_bytes)
                mask = 1 << (7 - np.random.randint(0, 7))
                genomes[i * self.gene_bytes + byte_id] ^= mask



    # Functions that return something based on genomes.

    def decode_genomes(self, genomes : bytearray, rerange : bool = False):
        """
        Decodes all genomes and returns a well structured object with all data.

        Return object structure
        -----------------------
        - Genomes (list)
            - Genes (list)
                - Gene (dictionary)

        Gene keys
        ---------
        - source_type
        - source_id
        - sink_type
        - sink_id
        - weight
        """
        
        # Separates the genomes from the large bytearray.
        genome_bytes_count = self.genome_len * self.gene_bytes
        separated_genomes = [genomes[i : i + genome_bytes_count] for i in range(0, len(genomes), genome_bytes_count)]

        # Decode all genes, combine them into genomes and dump the genomes into the result.
        result = []
        for genome in separated_genomes:
            decoded_genome = []

            # Loops through every starting point of a gene in genome.
            for gene_start_i in range(0, genome_bytes_count, self.gene_bytes):
                # Combine gene's bytes and turn it into an int.
                gene = int.from_bytes(genome[gene_start_i : gene_start_i + self.gene_bytes], byteorder="big")
                
                # Decode with bit manipulation. This is not reranged, this is raw data.
                decoded_gene = {
                    "source_type":  gene    >>  self.source_type_shift  &   self.source_type_mask,
                    "source_id":    gene    >>  self.source_id_shift    &   self.source_id_mask,
                    "sink_type":    gene    >>  self.sink_type_shift    &   self.sink_type_mask,
                    "sink_id":      gene    >>  self.sink_id_shift      &   self.sink_id_mask,
                    "weight":       gene                                &   self.weight_mask
                }

                # Rerange gene
                # id's      -> 23   -> (23 / 32) * 4 -> 2.875       -> 2 (floored)
                # weight    -> 1483 -> [(1483 / 4096) * 8.0] - 4.0  -> -1.1
                if rerange == True:
                    lens = [len(self.inputs), self.inner_neurons, len(self.outputs)]
                    decoded_gene["source_id"] = int(np.floor((decoded_gene["source_id"] / (2**self.source_id_len))  * lens[decoded_gene["source_type"]]))
                    decoded_gene["sink_id"] =   int(np.floor((decoded_gene["sink_id"]   / (2**self.sink_id_len))    * lens[-1-decoded_gene["sink_type"]]))
                    decoded_gene["weight"] =                ((decoded_gene["weight"]    / (2**self.weight_len))     * self.weight_range) - (self.weight_range * 0.5)

                decoded_genome.append(decoded_gene)
            
            result.append(decoded_genome)

        return result

    # more functions...