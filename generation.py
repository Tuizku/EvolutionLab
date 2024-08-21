import numpy as np

class Generation:
    def __init__(self, world_size):
        # Setup Generation's variables
        self.world_size : int = world_size
        self.map = np.zeros(shape=(world_size, world_size), dtype=np.int8)

        # Setup
        
