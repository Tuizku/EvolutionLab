import numpy as np
import random
import time


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
    separated_genomes = [genomes[i:i + (genome_len * gene_bytes)] for i in range(0, len(genomes), (genome_len * gene_bytes))]
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





# TESTING
population = 512
survived_population = 256
genome_len = 16
gene_bytes = 3


test_id = 1
if test_id == 0:
    genomes = get_random_bytearray(gene_bytes * genome_len * survived_population)
    crossovered_genomes = bytearray_crossover(genomes, survived_population, population, genome_len, gene_bytes)
elif test_id == 1:
    for i in range(9):
        genomes = get_random_bytearray(gene_bytes * genome_len * population)
        mutated_genomes = bytearray_mutate(genomes, gene_bytes, 0.01)



#region test
# gene = get_random_bytearray(3)

# binary_string = "".join(f'{byte:08b}' for byte in gene)
# print(binary_string)

# get_bit(gene, 0)
# set_bit(gene, 0, 0)

# binary_string = "".join(f'{byte:08b}' for byte in gene)
# print(binary_string)
#endregion test