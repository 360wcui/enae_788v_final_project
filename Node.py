import numpy as np
class Node:
    def __init__(self, x, y, id):
        self.x = float(x)
        self.y = float(y)
        self.id = id

    def __eq__(self, other):
        return other.id == self.id


    def __str__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y) + 'id: ' + str(self.id)
        # return str(self.id)

    def exact_eq(self, other):
        distance = np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < 1e-3

