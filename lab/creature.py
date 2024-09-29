import numpy as np
from lab.bytedna import ByteDNA

class Creature:
    def __init__(self, data : dict, genome : bytearray, bytedna : ByteDNA, generation):
        # Setup Creature's variables
        self.data : dict = data
        self.genome : bytearray = genome
        self.bytedna : ByteDNA = bytedna
        self.generation = generation

        # Add creature to this point in the map
        generation.map[data["x"]][data["y"]] = 1

        # Setup neuralnet
        optimized_genome = self.bytedna.get_optimized_genome(genome)
        self.neurons_inputs, self.neurons_output, self.neurons_function, include_dict = self.bytedna.get_needed_neurons(optimized_genome)
        self.conns_source_id, self.conns_sink_id, self.conns_weight = self.bytedna.genome_to_conns(optimized_genome, include_dict)
        

    def update(self):
        # Clear inputs
        for i in range(len(self.neurons_inputs)):
            self.neurons_inputs[i].clear()

        # Update inputs
        for i in range(len(self.conns_source_id)):
            # Multiply source's output with conn's weight, and add this to the sink's inputs
            activation = self.conns_weight[i] * self.neurons_output[self.conns_source_id[i]]
            self.neurons_inputs[self.conns_sink_id[i]].append(activation)


        # Update outputs

        # Calculate activation from inputs. (inputs are already weighed)
        activations = np.tanh([np.sum(inputs) for inputs in self.neurons_inputs])

        for i in range(len(self.neurons_inputs)):
            func = self.neurons_function[i]

            # Update the output (inner neuron logic)
            if func == None:
                self.neurons_output[i] = activations[i]

            # (custom neuron logic)
            else: 
                self.neurons_output[i] = func(activations[i], self.data, self.generation)
