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


def bytearray_crossover(genomes : bytearray, survived, population, genome_len):
    start_time = time.time()
    
    result_genomes = bytearray()

    # Shuffle the genomes
    separated_genomes = [genomes[i:i+genome_len] for i in range(0, len(genomes), genome_len)]
    random.shuffle(genomes)

    singles = survived % 2
    if singles > 0:
        result_genomes.extend()


    print(time.time()-start_time)
    return None




# TESTING

compact_genomes = get_random_bytearray(3 * 4 * 95)

crossovered_genomes = bytearray_crossover(compact_genomes, 95, 128, 12)



#region test
# gene = get_random_bytearray(3)

# binary_string = "".join(f'{byte:08b}' for byte in gene)
# print(binary_string)

# get_bit(gene, 0)
# set_bit(gene, 0, 0)

# binary_string = "".join(f'{byte:08b}' for byte in gene)
# print(binary_string)
#endregion test