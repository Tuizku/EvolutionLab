#import numpy as np
from lab import Lab
from dna import DNA
from generation import Generation



def disUP(activation : float, data : dict, generation : Generation):
    return data["y"] / (generation.world_size - 1)
def disDOWN(activation : float, data : dict, generation : Generation):
    return (generation.world_size - 1 - data["y"]) / (generation.world_size - 1)
def disRIGHT(activation : float, data : dict, generation : Generation):
    return data["x"] / (generation.world_size - 1)
def disLEFT(activation : float, data : dict, generation : Generation):
    return (generation.world_size - 1 - data["x"]) / (generation.world_size - 1)

def moveUP(activation : float, data : dict, generation : Generation):
    if activation > 0:
        moved = generation.change_pos(data["x"], data["y"], 0, -1)
        if moved: data["y"] -= 1
    return 0
def moveDOWN(activation : float, data : dict, generation : Generation):
    if activation > 0:
        moved = generation.change_pos(data["x"], data["y"], 0, 1)
        if moved: data["y"] += 1
    return 0
def moveRIGHT(activation : float, data : dict, generation : Generation):
    if activation > 0:
        moved = generation.change_pos(data["x"], data["y"], -1, 0)
        if moved: data["x"] -= 1
    return 0
def moveLEFT(activation : float, data : dict, generation : Generation):
    if activation > 0:
        moved = generation.change_pos(data["x"], data["y"], 1, 0)
        if moved: data["x"] += 1
    return 0

input_funcs = [disUP, disDOWN, disRIGHT, disLEFT]
output_funcs = [moveUP, moveDOWN, moveRIGHT, moveLEFT]

dna = DNA(input_funcs, output_funcs, 4, 1)
lab = Lab(dna)
lab.run_generation()