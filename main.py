from lab import Lab
from dna import DNA
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
dna = DNA(input_funcs, output_funcs, 4, 1, 0.01)

# CREATE A LAB WITH A SELECTION CRITERIA (WHICH CREATURES SURVIVE)
selection_criteria = [{
    "name": "x",
    "operator": ">",
    "value": 20
},
{
    "name": "y",
    "operator": ">",
    "value": 20
}]
lab = Lab(dna, selection_criteria, steps_per_gen=64, population=128, world_size=32)



# PROGRAM

lab.run_generations(199)
steps_data = lab.run_generation(return_steps_data=True)
view.view_generation(steps_data)
view.view_evolution_chart(lab.load_gens(), lab.population, dna.genome_len)

#lab.run_generation(debug=True)

# gens_data = lab.load_gens()
# steps_data = lab.run_generation(gens_data[-1]["genomes"], False, True)
# view.view_generation(steps_data)
# view.view_evolution_chart(gens_data, lab.population, dna.genome_len)