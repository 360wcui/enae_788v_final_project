import numpy as np

class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight
        self.next = None

    def __lt__ (self, other):
        return self.weight < other.weight

    def __gt__ (self, other):
        return self.weight > other.weight

    def __eq__ (self, other):
        return self.weight == other.weight
    #
    # def __eq__(self, other):
    #     if self.weight is not other.weight:
    #         return self.weight > other.weight
    #     elif self.start is not other.start:
    #         return self.start > other.start
    #     elif self.end is not other.end:
    #         return self.end > other.end
    #     else:
    #         return 0



    def __str__(self):
       return str(self.weight) + ' ' + str(self.start.id) + ' ' + str(self.end.id)

