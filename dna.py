import numpy as np
import random
import time

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


    # The most important functions of DNA
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


    # Neuron / Genome managing functions
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
    
    def get_needed_neurons(self, genome : list):
        """
        Gets only the needed neurons for the creature.

        Returns
        -------
            neurons_inputs (list): Every neuron's current inputs.
            neurons_output (list): Every neuron's current output.
            neurons_function (list): Every neuron's unique function. Inner neurons have None.
            include_dictionary (dict): Boolean numpy lists. Which neurons are used? ("include_inputs", "include_outputs", "include_inners")
        """

        # Include neurons
        # Creates lists of bools, True meaning that it will be added to the neuron list.
        include_inputs = np.full(len(self.inputs), False, dtype=bool)
        include_outputs = np.full(len(self.outputs), False, dtype=bool)
        include_inners = np.full(self.inner_neurons, False, dtype=bool)

        # Includes neurons in the result.
        def include_neuron(is_source : bool, type : int, id : int):
            nonlocal include_inputs, include_outputs, include_inners
            if type == 1:
                include_inners[id] = True
            elif type == 0:
                if is_source == True:
                    include_inputs[id] = True
                else:
                    include_outputs[id] = True


        # Include all neurons that are referenced in genome
        for i in range(len(genome)):
            decoded_gene = self.decode_gene(genome[i], True)
            include_neuron(True, decoded_gene["source_type"], decoded_gene["source_id"])
            include_neuron(False, decoded_gene["sink_type"], decoded_gene["sink_id"])
        

        # Result lists
        neurons_inputs = []
        neurons_output = []
        neurons_function = []

        # Add the included neurons in their correct order to the result lists
        all_includes = [include_inputs, include_inners, include_outputs]
        all_funcs = [self.inputs, np.full(len(include_inners), None), self.outputs]
        for i in range(3):
            for j in range(len(all_includes[i])):
                if all_includes[i][j] == True:
                    neurons_inputs.append([])
                    neurons_output.append(0)
                    neurons_function.append(all_funcs[i][j])


        # Return 3 lists and a dict
        return neurons_inputs, neurons_output, neurons_function, {
            "include_inputs": include_inputs,
            "include_outputs": include_outputs,
            "include_inners": include_inners
        }

    def get_optimized_genome(self, genome : list):
        """
        Cuts out inner neurons that don't have a valid source and sink. The genes that use these useless inner neurons, are cut out.
        - A valid source is an input neuron or a different inner neuron.
        - A valid sink is an output neuron or a different inner neuron.

        Returns
        -------
            optimized_genome (list): Same data type as normal genome, but with possibly fewer genes.
        """
        
        # 2 requirements for each inner neuron.
        inner_neurons_requirements = np.full((self.inner_neurons, 2), fill_value=False, dtype=bool)
        
        # Check inner neuron requirements from every gene.
        for gene in genome:
            # Decode gene
            decoded_gene = self.decode_gene(gene, True)
            source_type = decoded_gene["source_type"]
            source_id = decoded_gene["source_id"]
            sink_type = decoded_gene["sink_type"]
            sink_id = decoded_gene["sink_id"]

            # Case -> Sink = Inner neuron
            if sink_type == 1:
                if source_type == 0 or source_id != sink_id:
                    inner_neurons_requirements[sink_id][0] = True
            
            # Case -> Source = Inner neuron
            if source_type == 1:
                if sink_type == 0 or sink_id != source_id:
                    inner_neurons_requirements[source_id][1] = True
        
        # Turn requirements into booleans, which inner neurons will be used?
        # Index in list = which inner neuron?
        # Value is True if both requirements are True.
        inner_neurons_included = []
        for requirements in inner_neurons_requirements:
            if requirements[0] == True and requirements[1] == True:
                inner_neurons_included.append(True)
            else: inner_neurons_included.append(False)
        
        # Adds only the needed genes to the result
        optimized_genome = []
        for gene in genome:
            # Decode gene
            decoded_gene = self.decode_gene(gene, True)
            source_type = decoded_gene["source_type"]
            source_id = decoded_gene["source_id"]
            sink_type = decoded_gene["sink_type"]
            sink_id = decoded_gene["sink_id"]

            # Do not include gene if a source or a sink is an inner neuron that isn't required in the brain.
            include_gene = True
            if source_type == 1 and inner_neurons_included[source_id] == False:
                include_gene = False
            elif sink_type == 1 and inner_neurons_included[sink_id] == False:
                include_gene = False
            
            # Add gene if included
            if include_gene == True: optimized_genome.append(gene)
        
        return optimized_genome
            



    def genome_to_conns(self, genome : list, include_dict : dict = None):
        def set_tweaks(length, include_list, tweaks):
            tweak = 0
            for i in range(length):
                if include_list[i] == False: tweak += 1
                tweaks[i] = tweak
            return tweak
        
        # Conns variables
        conns_source_id = []
        conns_sink_id = []
        conns_weight = []

        # Lengths
        ins = len(self.inputs)
        inners = self.inner_neurons
        outs = len(self.outputs)
        actual_ins = ins
        actual_inners = inners

        # Create the tweak lists. These values will be summed with source/sink ids.
        # Their point is to transform normal ids to ids that reference actual neurons included in the creature.
        input_tweaks = np.zeros(ins, dtype=int)
        inner_tweaks = np.zeros(inners, dtype=int)
        output_tweaks = np.zeros(outs, dtype=int)
        if include_dict != None:
            # Set the tweaks
            actual_ins -= set_tweaks(ins, include_dict["include_inputs"], input_tweaks)
            actual_inners -= set_tweaks(inners, include_dict["include_inners"], inner_tweaks)
            set_tweaks(outs, include_dict["include_outputs"], output_tweaks)
        

        # Loop through all genes and turn them into conns
        for gene in genome:
            decoded_gene = self.decode_gene(gene, True)
            source_id = decoded_gene["source_id"]
            sink_id = decoded_gene["sink_id"]

            # Tweak the source_id and sink_id
            if decoded_gene["source_type"] == 0:
                source_id -= input_tweaks[source_id]
            else:
                source_id -= inner_tweaks[source_id]

            if decoded_gene["sink_type"] == 0:
                sink_id -= output_tweaks[sink_id]
            else:
                sink_id -= inner_tweaks[sink_id]

            # Turn source- and sink id's into combined ids
            source_id += (decoded_gene["source_type"] * actual_ins)
            sink_id += actual_ins + (actual_inners * (1 - decoded_gene["sink_type"]))
            
            conns_source_id.append(source_id)
            conns_sink_id.append(sink_id)
            conns_weight.append(decoded_gene["weight"])
            #print(f"{source_id}, {sink_id}, {decoded_gene["weight"]} | reranged_sink_id = {decoded_gene['sink_id']}")
        
        return conns_source_id, conns_sink_id, conns_weight

    def average_hamming_distance(self, genomes):
        """
        Calculates the average hamming distance between the genomes.
        This can be used to see how different dna the creatures have.
        """
        start_time = time.time()

        genomes_len = len(genomes)
        diverse_bits = 0

        # Takes a bit[x] from every genome and pushes it into a list. And this is repeated for the amount of bits that a genome has.
        # After that we can compare the bits in these columns, and see how many bits are the same.
        # This is a clever solution for this problem, and it's 500x faster than the first solution I came up with.
        bit_columns = [[int(genome[gene_i][bit_i]) for genome in genomes]
                       for gene_i in range(self.genome_len) 
                       for bit_i in range(self.gene_len)]
        for bit_column in bit_columns:
            unique, counts = np.unique(bit_column, return_counts=True)
            diverse_bits += counts[np.argmin(counts)]
        
        all_bits = self.gene_len * self.genome_len * genomes_len
        result = diverse_bits / (all_bits * 0.5)
        #print(f"AVERAGE HAMMING DISTANCE DEBUG -> time = {round(time.time() - start_time, 6)}")
        return result