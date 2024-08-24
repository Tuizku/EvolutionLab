import numpy as np
from dna import DNA

class Creature:
    def __init__(self, data : dict, genome : list, dna : DNA, generation):
        # Setup Creature's variables
        self.data : dict = data
        self.genome : list = genome
        self.dna : DNA = dna
        self.generation = generation

        # Add creature to this point in the map
        generation.map[data["x"]][data["y"]] = 1

        # Setup neuralnet
        self.neurons_inputs, self.neurons_output, self.neurons_function = self.dna.get_all_neurons()
        self.conns_source_id, self.conns_sink_id, self.conns_weight = self.dna.genome_to_conns(genome)

    def update(self):
        # Clear inputs
        for i in range(len(self.neurons_inputs)):
            self.neurons_inputs[i] = []

        # Update inputs
        for i in range(len(self.conns_source_id)):
            source_id = self.conns_source_id[i]
            sink_id = self.conns_sink_id[i]
            weight = self.conns_weight[i]

            # Multiply source's output with conn's weight, and add this to the sink's inputs
            activation = weight * self.neurons_output[source_id]
            self.neurons_inputs[sink_id].append(activation)


        # Update outputs
        for i in range(len(self.neurons_inputs)):
            inputs = self.neurons_inputs[i]
            func = self.neurons_function[i]
            
            # Calculate activation from inputs. (inputs are already weighed)
            z = np.sum(inputs)
            activation = np.tanh(z)

            # Update the output (inner neuron logic)
            if func == None: # 
                self.neurons_output[i] = activation

            # (custom neuron logic)
            else: 
                self.neurons_output[i] = func(activation, self.data, self.generation)