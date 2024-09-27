from lab import Lab
from bytedna import ByteDNA
from generation import Generation
import view


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
bytedna = ByteDNA(input_funcs, output_funcs, 12, 3, 4, 100, 5, 5, 12)

# CREATE A LAB WITH A SELECTION CRITERIA (WHICH CREATURES SURVIVE)
selection_criteria = [
{
    "name": "x",
    "operator": "<",
    "value": 22
},
{
    "name": "x",
    "operator": ">",
    "value": 10
},
{
    "name": "y",
    "operator": "<",
    "value": 22
},
{
    "name": "y",
    "operator": ">",
    "value": 10
}]
lab = Lab(bytedna, selection_criteria, name="bytedna_centertest", steps_per_gen=64, population=128, world_size=32)



# PROGRAM

lab.run_generations(999)
steps_data = lab.run_generation(return_steps_data=True)
view.view_generation(steps_data)
genomes, stats = lab.load_gens()
view.view_evolution_chart(stats, lab.population)