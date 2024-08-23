import numpy as np

class DNA:
    #region Functions
    def numpy_getrandbits(self, k):
        num_bits = (k + 31) // 32  # Calculate how many 32-bit integers are needed
        random_ints = np.random.randint(0, 2**32, size=num_bits, dtype=np.uint32)
        random_bits = sum(int(x) << (32 * i) for i, x in enumerate(random_ints))
        random_int = random_bits & ((1 << k) - 1)  # Trim to k bits
        return bin(random_int)[2:].zfill(k)
    #endregion

    def __init__(self, inputs, outputs, genome_len : int, inner_neurons : int, source_id_len = 5, sink_id_len = 5, weight_len = 12):
        # Setup DNA's variables
        self.inputs = inputs
        self.outputs = outputs

        self.gene_len = source_id_len + sink_id_len + weight_len + 2
        self.genome_len = genome_len
        self.inner_neurons = inner_neurons

        self.source_id_len = source_id_len
        self.sink_id_len = sink_id_len
        self.weight_len = weight_len

        # Setup DNA points (the indexes where different parts of binary-gene starts)
        self.source_type_point = 0
        self.source_id_point = 1
        self.sink_type_point = source_id_len + 1
        self.sink_id_point = source_id_len + 2
        self.weight_point = source_id_len + sink_id_len + 2

        # Test
        print(self.random_genome())


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
        pass