import numpy as np
from dna import DNA
from generation import Generation

class Creature:
    def __init__(self, data : dict, genome : list, dna : DNA, generation : Generation):
        # Setup Creature's variables
        self.data : dict = data
        self.genome : list = genome
        self.dna : DNA = dna
        self.generation : Generation = generation

        # Setup neuralnet (NOT FINISHED)
        self.neurons_inputs = []
        self.neurons_output = []
        self.neurons_function = []

    def update(self):
        # Update inputs
        # ...

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