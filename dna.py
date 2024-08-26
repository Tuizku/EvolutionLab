import numpy as np
import random

class DNA:
    #region Functions
    def numpy_getrandbits(self, k):
        num_bits = (k + 31) // 32  # Calculate how many 32-bit integers are needed
        random_ints = np.random.randint(0, 2**32, size=num_bits, dtype=np.uint32)
        random_bits = sum(int(x) << (32 * i) for i, x in enumerate(random_ints))
        random_int = random_bits & ((1 << k) - 1)  # Trim to k bits
        return bin(random_int)[2:].zfill(k)
    #endregion

    def __init__(self, inputs, outputs, genome_len : int, inner_neurons : int, mutation_rate : float, source_id_len = 5, sink_id_len = 5, weight_len = 12, weight_range = 8.0):
        # Setup DNA's variables
        self.inputs = inputs
        self.outputs = outputs

        self.gene_len = source_id_len + sink_id_len + weight_len + 2
        self.genome_len = genome_len
        self.inner_neurons = inner_neurons
        self.mutation_rate = mutation_rate
        self.weight_range = weight_range

        self.source_id_len = source_id_len
        self.sink_id_len = sink_id_len
        self.weight_len = weight_len

        # Setup DNA points (the indexes where different parts of binary-gene starts)
        self.source_type_point = 0
        self.source_id_point = 1
        self.sink_type_point = source_id_len + 1
        self.sink_id_point = source_id_len + 2
        self.weight_point = source_id_len + sink_id_len + 2


    def random_genome(self) -> list:
        """Returns a random genome based on dna's settings."""
        result = []
        for i in range(self.genome_len):
            result.append(self.numpy_getrandbits(self.gene_len))
        return result
    def random_genomes(self, count : int) -> list:
        """Returns multiple random genomes based on dna's settings."""
        result = []
        for i in range(count):
            result.append(self.random_genome())
        return result
    
    def crossover(self, genomes, population):
        """
        Between genes crossover.
        
        Returns all new genomes.
        """
        survived = len(genomes)
        new_genomes = []

        # Shuffle the input list, so that all genomes have the same chance to evolve.
        random.shuffle(genomes)

        # Add extra parents to the new genomes, so that all input genomes will have a couple.
        extra_parents = survived % 2
        if extra_parents > 0:
            new_genomes.extend(genomes[-extra_parents:])
            genomes = genomes[:-extra_parents]

        # Calculate parents (in couples) and needed children counts
        parents_count = survived - extra_parents
        needed_children = population - extra_parents

        # Calculate the children amounts per couple + how many will create an additional child
        children_per_couple = (needed_children / parents_count) * 2
        default_children_per_couple = int(np.floor(children_per_couple))
        additional_childs = int(np.round((children_per_couple - default_children_per_couple) * (parents_count * 0.5)))

        for parent_i in range(0, parents_count, 2):
            parent0 = genomes[parent_i]
            parent1 = genomes[parent_i + 1]
            
            # Calculate how many children this couple creates
            children_count = default_children_per_couple
            if additional_childs > 0:
                children_count += 1
                additional_childs -= 1
            
            # Create the children 2 offsprings at a time
            for child_i in range(0, children_count, 2):
                crossover_point = np.random.randint(self.genome_len)
                new_genomes.append(parent0[:crossover_point] + parent1[crossover_point:])
                if child_i + 1 < children_count: # if child_id + 1 == 3 and children_count == 3, then it only creates the first offspring
                    new_genomes.append(parent1[:crossover_point] + parent0[crossover_point:])
        
        if len(new_genomes) < population:
            print(f"dna crossover resulted a smaller population ({len(new_genomes)}/{population})")
        
        self.mutate(new_genomes)
        return new_genomes

    def mutate(self, genomes):
        """
        Mutates the population by DNA's mutation_rate. If a mutation happens in a gene, a random bit will be flipped in that gene.
        """

        # If mutation_rate == 0.01, then interval is 100.
        mutation_interval = int(1 / self.mutation_rate)

        # Every genome has the possibility of mutation
        for genome in genomes:
            # Creates the triggers for all genes in this genome. If trigger == 0, then a mutation happens in that gene.
            mutation_triggers = np.random.randint(0, mutation_interval, size=self.genome_len)

            # Checks all genes if they got a mutation, and then does the mutation if so happened.
            for i in range(self.genome_len):
                if mutation_triggers[i] == 0:
                    flip_pos = np.random.randint(self.gene_len)
                    flipped_bit = '1' if genome[i][flip_pos] == '0' else '0'
                    genome[i] = genome[i][:flip_pos] + flipped_bit + genome[i][flip_pos + 1:]


    # Play around functions
    def identical_genomes(self, genome : list, population : int):
        """Turns a single genome into a whole population. This can be used as a test, but it's not used in the normal usage."""
        genomes = [genome for i in range(population)]
        return genomes


    def decode_gene(self, gene : str, rerange : bool = False):
        result = {
            "source_type": int(gene[0 : 1], 2),
            "source_id": int(gene[1 : 1 + self.source_id_len], 2),
            "sink_type": int(gene[1 + self.source_id_len : 2 + self.source_id_len], 2),
            "sink_id": int(gene[2 + self.source_id_len : 2 + self.source_id_len + self.sink_id_len], 2),
            "weight": int(gene[-self.weight_len:], 2)
        }

        if rerange == True:
            lens = [len(self.inputs), self.inner_neurons, len(self.outputs)]
            
            result["source_id"] = int(np.floor((result["source_id"] / (2**self.source_id_len)) * lens[result["source_type"]]))
            result["sink_id"] = int(np.floor((result["sink_id"] / (2**self.sink_id_len)) * lens[-1-result["sink_type"]]))
            result["weight"] = ((result["weight"] / (2**self.weight_len)) * self.weight_range) - 4.0

        return result

    def get_all_neurons(self):
        neurons_inputs = []
        neurons_output = []
        neurons_function = []

        # Add inputs
        for input_func in self.inputs:
            neurons_inputs.append([])
            neurons_output.append(0)
            neurons_function.append(input_func)

        # Add inner neurons
        for i in range(self.inner_neurons):
            neurons_inputs.append([])
            neurons_output.append(0)
            neurons_function.append(None)
        
        # Add outputs
        for output_func in self.outputs:
            neurons_inputs.append([])
            neurons_output.append(0)
            neurons_function.append(output_func)
        
        return neurons_inputs, neurons_output, neurons_function
    
    def genome_to_conns(self, genome : list):
        # Conns variables
        conns_source_id = []
        conns_sink_id = []
        conns_weight = []

        # Lengths
        ins = len(self.inputs)
        inners = self.inner_neurons

        # Loop through all genes and turn them into conns
        for gene in genome:
            decoded_gene = self.decode_gene(gene, True)
            source_id = decoded_gene["source_id"] + (decoded_gene["source_type"] * ins)
            sink_id = ins + (inners * (1 - decoded_gene["sink_type"])) + decoded_gene["sink_id"]
            
            conns_source_id.append(source_id)
            conns_sink_id.append(sink_id)
            conns_weight.append(decoded_gene["weight"])
            #print(f"{source_id}, {sink_id}, {decoded_gene["weight"]} | reranged_sink_id = {decoded_gene['sink_id']}")
        
        return conns_source_id, conns_sink_id, conns_weight