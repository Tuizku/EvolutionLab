from lab.lab import Lab
from lab.bytedna import ByteDNA
from lab.generation import Generation
import lab.view as view
import lab_manager


# NEURON FUNCTIONS

# Input
def disUP(activation : float, data : dict, generation : Generation):
    return data["y"] / (generation.world_size - 1)
def disDOWN(activation : float, data : dict, generation : Generation):
    return (generation.world_size - 1 - data["y"]) / (generation.world_size - 1)
def disRIGHT(activation : float, data : dict, generation : Generation):
    return data["x"] / (generation.world_size - 1)
def disLEFT(activation : float, data : dict, generation : Generation):
    return (generation.world_size - 1 - data["x"]) / (generation.world_size - 1)

# Output
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

# CREATE DNA WITH THESE FUNCTIONS
input_funcs = [disUP, disDOWN, disRIGHT, disLEFT]
output_funcs = [moveUP, moveDOWN, moveRIGHT, moveLEFT]
bytedna = ByteDNA(input_funcs, output_funcs, 4, 3, 1, 100, 5, 5, 12)

# CREATE A SELECTION CRITERIA (WHICH CREATURES SURVIVE IN LAB)
selection_criteria = [
{
    "name": "x",
    "operator": "<",
    "value": 16
}]

# CREATE THE LAB INSTANCE
lab = Lab(bytedna, selection_criteria, name="left_test", steps_per_gen=64, population=128, world_size=32)


# OPEN LAB MANAGER
lab_manager.open_lab_manager(lab, bytedna)