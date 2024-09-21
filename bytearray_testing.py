import numpy as np
import random
import time

from dna import DNA
test_dna = DNA([0], [0], 16, 1, 0)


def get_random_bytearray(length):
    random_bytes = np.random.randint(0, 255, size=length, dtype=np.uint8)
    return bytearray(random_bytes)

def get_bit(byte_array, bit_position):
    byte_index = bit_position // 8  # Find which byte contains the bit
    bit_offset = bit_position % 8   # Find which bit in that byte we want
    
    # Access the byte and shift right by the bit offset, then mask with 1
    return (byte_array[byte_index] >> (7 - bit_offset)) & 1

def set_bit(byte_array, bit_position, value):
    byte_index = bit_position // 8  # Find which byte contains the bit
    bit_offset = bit_position % 8   # Find which bit in that byte we want
    
    # Create a mask for the bit we want to modify
    mask = 1 << (7 - bit_offset)
    
    if value == 1:
        # Set the bit to 1 using OR
        byte_array[byte_index] |= mask
    else:
        # Set the bit to 0 using AND with the negated mask
        byte_array[byte_index] &= ~mask


def bytearray_crossover(genomes : bytearray, survived, population, genome_len, gene_bytes):
    start_time = time.time()
    
    result_genomes = bytearray()

    # Shuffle the genomes
    separated_genomes = [genomes[i : i + (genome_len * gene_bytes)] for i in range(0, len(genomes), (genome_len * gene_bytes))]
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
            crossover_point = np.random.randint(genome_len)
            result_genomes.extend(parent0[:crossover_point * gene_bytes])
            result_genomes.extend(parent1[crossover_point * gene_bytes:])
            if child_i + 1 < children_count: # if child_id + 1 == 3 and children_count == 3, then it only creates the first offspring
                result_genomes.extend(parent1[:crossover_point * gene_bytes])
                result_genomes.extend(parent0[crossover_point * gene_bytes:])
        
    
    result_genomes_count = round(len(result_genomes) / genome_len / gene_bytes)
    if result_genomes_count < population:
        print(f"dna crossover resulted a smaller population ({result_genomes_count}/{population})")


    print(time.time()-start_time)
    return None

def bytearray_mutate(genomes: bytearray, gene_bytes, mutation_rate):
    start_time = time.time()

    # If mutation_rate == 0.01, then interval is 100. (In DNA, we could change rate to interval, so this conversion wouldn't be needed)
    mutation_interval = int(1 / mutation_rate)
    genes_in_genomes = int(len(genomes) / gene_bytes)

    # Calculate mutation triggers, if trigger == 0, then a mutation happens.
    mutation_triggers = np.random.randint(0, mutation_interval, size=genes_in_genomes)
    for i in range(genes_in_genomes):
        if mutation_triggers[i] == 0:
            #print(f"{bin(int(genomes[i * gene_bytes]))} {bin(int(genomes[i * gene_bytes + 1]))} {bin(int(genomes[i * gene_bytes + 2]))}")
            byte_id = np.random.randint(0, gene_bytes)
            mask = 1 << (7 - np.random.randint(0, 7))
            genomes[i * gene_bytes + byte_id] ^= mask
            
    print(time.time() - start_time)

def bytearray_decode_genomes(genomes : bytearray, genome_len, gene_bytes, gene_bits, rerange : bool = False):
    
    # !!! These will be replaced in the new dna class !!!
    source_id_len = 5
    sink_id_len = 5
    weight_len = 12
    
    
    # Separates the genomes from the large bytearray.
    genome_bytes_count = genome_len * gene_bytes
    separated_genomes = [genomes[i : i + genome_bytes_count] for i in range(0, len(genomes), genome_bytes_count)]

    # Decode all genes, combine them into genomes and dump the genomes into the result.
    result = []
    for genome in separated_genomes:
        decoded_genome = []

        # Loops through every starting point of a gene in genome.
        for gene_start_i in range(0, genome_bytes_count, gene_bytes):
            # Combine gene's bytes and turn it into an int.
            gene = int.from_bytes(genome[gene_start_i : gene_start_i + gene_bytes], byteorder="big")
            
            # Decode with bit manipulation. This is not reranged, this is raw data.
            decoded_gene = {
                "source_type": gene >> (gene_bits - 1) & 1,
                "source_id": gene >> (gene_bits - 1 - source_id_len) & ((1 << source_id_len) - 1),
                "sink_type": gene >> (gene_bits - 1 - source_id_len - 1) & 1,
                "sink_id": gene >> (gene_bits - 1 - source_id_len - 1 - sink_id_len) & ((1 << sink_id_len) - 1),
                "weight": gene & ((1 << weight_len) - 1)
            }

            # if rerange == True:
            #   rerange the gene here

            decoded_genome.append(decoded_gene)
        
        result.append(decoded_genome)
    
    return result

def bytearray_avg_hamming_distance(genomes : bytearray, population, genome_len, gene_bits):
    start_time = time.time()

    diverse_bits = 0
    int_genomes = [int.from_bytes(genomes[i * genome_len : i * genome_len + genome_len]) for i in range(population)]

    for i in range(0, population - 1):
        for j in range(1, population):
            diverse_bits += (int_genomes[i] ^ int_genomes[j]).bit_count()
    
    all_bits = gene_bits * genome_len * population
    result = diverse_bits / (all_bits * 0.5)

    print(f"time: {round(time.time() - start_time, 3)}s")
    return result



    



# TESTING
population = 128
survived_population = 256
genome_len = 4
gene_bytes = 3
gene_bits = gene_bytes * 8 # not customizable straight from this


test_id = 3
if test_id == 0:
    genomes = get_random_bytearray(gene_bytes * genome_len * survived_population)
    crossovered_genomes = bytearray_crossover(genomes, survived_population, population, genome_len, gene_bytes)
elif test_id == 1:
    for i in range(9):
        genomes = get_random_bytearray(gene_bytes * genome_len * population)
        mutated_genomes = bytearray_mutate(genomes, gene_bytes, 0.01)
elif test_id == 2:
    genomes = get_random_bytearray(gene_bytes * genome_len * survived_population)
    bytearray_decode_genomes(genomes, genome_len, gene_bytes, gene_bits, True)
    print("finished")
elif test_id == 3:
    genomes = get_random_bytearray(gene_bytes * genome_len * survived_population)
    hamming_dis = bytearray_avg_hamming_distance(genomes, population, genome_len, gene_bits)
    



#region test
# gene = get_random_bytearray(3)

# binary_string = "".join(f'{byte:08b}' for byte in gene)
# print(binary_string)

# get_bit(gene, 0)
# set_bit(gene, 0, 0)

# binary_string = "".join(f'{byte:08b}' for byte in gene)
# print(binary_string)
#endregion test